#!/usr/bin/python

from fake_rails import Respononse, Router, Model, ModelEncoder, Controller, db

class User(Model)

  "a user model"
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
    json = json.dumps(users, cls=ModelEncoder)
    response = Response(type'application/json')
    response.set_body('')

