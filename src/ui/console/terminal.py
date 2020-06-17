# coding: utf-8
import getpass


def request_string_input(message=None):
    if message:
        return input(message + ": ")
    else:
        return input()


def request_hidden_input(message=None):
    if message:
        return getpass.getpass(message + ": ")
    else:
        return getpass.getpass()


def show_info_message(message):
    print("*** INFO     ***\n" + message)


def show_info_dict(message, dictionary):
    assert isinstance(dictionary, dict)
    print("*** INFO     ***\n" + message)
    for k in dictionary:
        print(str(k) + " -> " + str(dictionary.get(k)))


def show_info_objects(message, objects):
    print("*** INFO     ***\n" + message)
    for obj in objects:
        print(str(obj))


def show_warning_message(message):
    print("*** WARNING  ***\n" + message)


def show_error_message(message):
    print("*** ERROR    ***\n" + message)


def show_get_request(url):
    print("GET     > " + url)


def show_post_request(url):
    print("POST    > " + url)


def method_info(func, obj_id, *args, **kwargs):
    print("*** DEBUG    ***")
    print("Object ID: ", obj_id)
    print("Function called: ", func.__qualname__)
    print("Input args: ")
    for arg in args:
        print("... " + str(arg))
    print("Input kwargs: ")
    for kwarg in kwargs:
        print("... " + str(kwarg) + " -> " + str(kwargs.get(kwarg)))
