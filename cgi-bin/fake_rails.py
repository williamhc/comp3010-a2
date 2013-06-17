import sys
import json
import sqlite3
from json import JSONEncoder
from os import environ


db = sqlite3.connect('q2.db')


class Router(object):

    """a silly hard-coded router to map a single controller"""
    def __init__(self):
        self.query_params = self.__get_query_params__()
        self.cookies = self.__get_cookies__()
        self.method = environ['REQUEST_METHOD']
        self.controller = self.cont_class(self.query_params, self.cookies)

    def route(self):
        c = self.controller
        response = {
            'GET': c.get,
            'POST': c.create,
            'DELETE': c.delete
        }[self.method]()
        response.respond()

    @staticmethod
    def __get_cookies__():
        if 'HTTP_COOKIE' not in environ:
            return {}
        cookies = {}
        cookie_text = environ['HTTP_COOKIE']
        for pair in cookie_text.split(';'):
            k, v = pair.split('=', 1)
            cookies[k.strip()] = v.strip()
        return cookies

    @staticmethod
    def __get_query_params__():
        if 'QUERY_STRING' in environ:
            param_str = environ['QUERY_STRING'] 
        else
            param_str = sys.stdin.read()
        data = {}
        for pair in param_str.split('&'):
            if pair and len(pair.split('=')) is 2:
                k, v = pair.split('=')
                data[k.strip()] = v.strip()
        return data


class Response(object):

    """a simple response object"""
    def __init__(self, type="text/html", body=""):
        self.headers = "Content-type: {0}\n".format(type)
        self.body = body

    def set_body(self, body):
        self.body = body

    def set_cookie(self, name, val):
        self.headers += "Set-cookie: {0}={1};\n".format(name, val)

    def respond(self):
        print self.headers
        print self.body


class Model(object):

    """a simple web model"""


class ModelEncoder(JSONEncoder):

    """a JSON encoder for my models"""
    def default(self, obj):
        if isinstance(obj, Model):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class Controller(object):

    """a base class for controllers - just a bunch of abstract methods"""

    def get(self):
        raise NotImplementedError("You must override `get` yourself.")

    def create(self):
        raise NotImplementedError("You must overrite `create` yourself.")

    def delete(self):
        raise NotImplementedError("You must override `delete` youself.")
