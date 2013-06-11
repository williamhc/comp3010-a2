#!/usr/bin/python


def render_html(partial_name, msg=""):
    add_message(msg)
    path = "../q2/{0}".format(partial_name)
    partial = open(path).read()
    globals()['html'] = TEMPLATE.format(messages, partial)


def add_message(msg):
    globals()['messages'] += msg


# globals aren't great but... meh
TEMPLATE = open("../template.html").read()
headers = "Content-type: text/html\n"
messages = ""
html = ""


def main():
    render_html("task_list.html")
    print headers
    print html

main()
