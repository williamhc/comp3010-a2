#!/usr/bin/python

from os import environ
import sys
import sqlite3



def render_html(partial_name, msg=""):
    add_message(msg)
    path = "../q1/{0}".format(partial_name)
    partial = open(path).read()
    globals()['html'] = TEMPLATE.format(messages, partial)


def add_message(msg):
    globals()['messages'] += msg


def set_cookie(name, value):
    cookie_line = "Set-cookie: {0}={1};\n".format(name, value)
    globals()['headers'] += cookie_line


def get_cookies():
    if 'HTTP_COOKIE' not in environ:
        return None
    cookie_text = environ['HTTP_COOKIE']
    cookies = {}
    for pair in cookie_text.split(';'):
        k, v = pair.split('=', 1)
        cookies[k.strip()] = v.strip()
    return cookies


def get_form_data():
    message_body = sys.stdin.read()
    data = {}
    for pair in message_body.split('&'):
        if pair and len(pair.split('=')) is 2:
            k, v = pair.split('=')
            data[k.strip()] = v.strip()
    return data


def authenticate_user(cookies):
    username = cookies['username']
    password = cookies['password']

    cursor = db.cursor()
    query = "SELECT * FROM users WHERE username=? AND password=?"
    params = (username, password,)
    cursor.execute(query, params)

    if cursor.fetchone():
        render_html("welcome.html", msg="Welcome, <strong>{0}</strong>!".format(username))
    else:
        render_html("error.html")


def signup_user(form):
    username = form['username']
    password = form['password']

    cursor = db.cursor()
    query = "INSERT INTO users VALUES (?, ?)"
    params = (username, password,)
    cursor.execute(query, params)
    set_cookie('username', username)
    set_cookie('password', password)

    render_html("welcome.html", msg="Welcome, <strong>{0}</strong>!".format(username))


# globals aren't great but... meh
TEMPLATE = open("../q1/template.html").read()
headers = "Content-type: text/html\n"
messages = ""
html = ""


def main():
    cookies = get_cookies()
    form = get_form_data()
    if cookies and 'username' in cookies and 'password' in cookies:
        authenticate_user(cookies)
    elif form:
        signup_user(form)
    else:
        render_html("form.html")
    print headers
    print html


db = sqlite3.connect('users.db')
main()
db.commit()
db.close()

