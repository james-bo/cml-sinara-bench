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


def show_warning_message(message):
    print("*** WARNING  ***\n" + message)


def show_error_message(message):
    print("*** ERROR    ***\n" + message)


def show_get_request(url):
    print("GET     > " + url)


def show_post_request(url):
    print("POST    > " + url)
