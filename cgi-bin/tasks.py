#!/usr/bin/python

import json
from fake_rails import Response, Router, Model, ModelEncoder, Controller, db


class Task(Model):

    """a task with a user and a priority"""
    def __init__(self, user=None, priority=None, title=None, description=None):
        self.user = user
        self.priority = priority
        self.title = title
        self.description = description

    @staticmethod
    def keys():
        return 'user', 'priority', 'title', 'description'

    def values(self):
        return self.user, self.priority, self.title, self.description

    def save(self):
        values = self.values()
        query = "INSERT INTO tasks {0} VALUES (?, ?, ?, ?)".format(self.keys())
        cursor = db.cursor()
        cursor.execute(query, values)
        return self

    def delete(self):
        kvs = zip(self.keys(), self.values())
        filters = ["{0}=?".format(key, val) for key, val in kvs if val]
        query = "DELETE FROM tasks WHERE {0}".format(", ".join(filters))
        cursor = db.cursor()
        cursor.execute(query, [val for val in self.values() if val])


class TasksController(Controller):

    """an executor for dealing with Task models"""
    def __init__(self, query_params, cookies):
        self.cursor = db
        self.query_params = query_params
        self.cookies = cookies

    def get(self):
        response = Response(type="application/json")
        cursor = db.cursor()
        query = "SELECT * FROM tasks"
        user = None

        if 'user' in self.query_params:
            user = self.query_params['user']
            response.set_cookie('user', user)
        elif 'user' in self.cookies:
            user = self.cookies['user']

        if user:
            query += " WHERE user=?"
            cursor.execute(query, (user, ))
        else:
            cursor.execute(query)
        tasks = [Task(*row) for row in cursor.fetchall()]
        response.set_body(json.dumps(tasks, cls=ModelEncoder))
        return response

    def create(self):
        new_task = Task(**self.query_params).save()
        body = json.dumps(new_task, cls=ModelEncoder)
        return Response(type="application/json", body=body)

    def delete(self):
        Task(**self.query_params).delete()
        return Response(type="application/json", body="DELETED")


class TasksRouter(Router):

    """a router for tasks only"""
    cont_class = TasksController

if __name__ == '__main__':
    from os import environ; environ['REQUEST_METHOD'] = 'POST'
    TasksRouter().route()
    db.commit()
    db.close()
