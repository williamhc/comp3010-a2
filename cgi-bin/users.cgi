#!/usr/bin/python

import json
from fake_rails import Response, Router, Model, ModelEncoder, Controller, db


class User(Model):

    """a user model"""
    def __init__(self, username, selected):
        self.username = username
        self.selected = selected


class UserController(Controller):

    """an executor for dealing with user models"""
    def __init__(self, query_params, cookies):
        self.query_params = query_params
        self.cookies = cookies

    def get(self):
        cursor = db.cursor()
        query = "SELECT DISTINCT user from tasks"
        results = cursor.execute(query).fetchall()
        selected = self.cookies['user'] if 'user' in self.cookies else None
        users = [User(row[0], row[0] == selected) for row in results]
        json_body = json.dumps(users, cls=ModelEncoder)
        return Response(type='application/json', body=json_body)


class UserRouter(Router):

    """a router for users only"""
    cont_class = UserController

if __name__ == '__main__':
    UserRouter().route()
    db.commit()
    db.close()
