# coding: utf-8
import getpass
import colorama


colorama.init()


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
    print(f"{colorama.Fore.CYAN}{message}{colorama.Style.RESET_ALL}")


def show_info_dict(message, dictionary):
    assert isinstance(dictionary, dict)
    print(f"{colorama.Fore.CYAN}{message}{colorama.Style.RESET_ALL}")
    for k in dictionary:
        print(f"{colorama.Fore.CYAN}{str(k)} -> {str(dictionary.get(k))}{colorama.Style.RESET_ALL}")


def show_info_objects(message, objects):
    print(f"{colorama.Fore.CYAN}{message}{colorama.Style.RESET_ALL}")
    for obj in objects:
        print(f"{colorama.Fore.CYAN}{str(obj)}{colorama.Style.RESET_ALL}")


def show_warning_message(message):
    print(f"{colorama.Fore.YELLOW}{message}{colorama.Style.RESET_ALL}")


def show_error_message(message):
    print(f"{colorama.Fore.RED}{message}{colorama.Style.RESET_ALL}")


def show_get_request(url):
    print(f"{colorama.Fore.GREEN}GET     > {url}{colorama.Style.RESET_ALL}")


def show_post_request(url):
    print(f"{colorama.Fore.GREEN}POST    > {url}{colorama.Style.RESET_ALL}")


def method_info(func, obj_id, *args, **kwargs):
    print(f"{colorama.Fore.MAGENTA}", end='')
    print(f"Object ID: {obj_id}")
    print(f"Function called: {func.__qualname__}")
    print("Input args: ")
    for arg in args:
        print(f"... {str(arg)}")
    print("Input kwargs: ")
    for kwarg in kwargs:
        print(f"... {str(kwarg)} -> {str(kwargs.get(kwarg))}")
    print(f"{colorama.Style.RESET_ALL}")
