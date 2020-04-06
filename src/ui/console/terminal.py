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
    print("INFO    : " + message)


def show_warning_message(message):
    print("WARNING : " + message)


def show_error_message(message):
    print("ERROR   : " + message)
