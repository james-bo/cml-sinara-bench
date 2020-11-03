# coding: utf-8
import getpass
import colorama
import datetime
import re


colorama.init()


class Output:
    REQUESTS = False
    FULL = False

    @classmethod
    def set_type(cls, value):
        if isinstance(value, int):
            if value == 1:
                cls.REQUESTS = True
                cls.FULL = False
                return
            if value == 2:
                cls.REQUESTS = True
                cls.FULL = True
                return
        cls.FULL = False
        cls.REQUESTS = False


class Identifiers:
    MAX_LENGTH = 8
    INFO = "{name:<{length}}".format(name="info".upper(), length=MAX_LENGTH)
    WARNING = "{name:<{length}}".format(name="warning".upper(), length=MAX_LENGTH)
    ERROR = "{name:<{length}}".format(name="error".upper(), length=MAX_LENGTH)
    DEBUG = "{name:<{length}}".format(name="debug".upper(), length=MAX_LENGTH)
    NETWORK = "{name:<{length}}".format(name="network".upper(), length=MAX_LENGTH)
    STACKTRACE = "{name:<{length}}".format(name="stack".upper(), length=MAX_LENGTH)


class MessageProperties:
    def __init__(self):
        self.__main_color = None
        self.__value_color = None
        self.__identifier = None

    @property
    def main_color(self):
        return self.__main_color

    @property
    def value_color(self):
        return self.__value_color

    @property
    def identifier(self):
        return self.__identifier

    def set_values(self, m_type):
        if m_type in ["info"]:
            self.__main_color = colorama.Fore.GREEN
            self.__value_color = colorama.Fore.LIGHTGREEN_EX
            self.__identifier = Identifiers.INFO
        elif m_type in ["warning"]:
            self.__main_color = colorama.Fore.YELLOW
            self.__value_color = colorama.Fore.LIGHTYELLOW_EX
            self.__identifier = Identifiers.WARNING
        elif m_type in ["error"]:
            self.__main_color = colorama.Fore.RED
            self.__value_color = colorama.Fore.LIGHTRED_EX
            self.__identifier = Identifiers.ERROR
        elif m_type in ["debug"]:
            self.__main_color = colorama.Fore.CYAN
            self.__value_color = colorama.Fore.LIGHTCYAN_EX
            self.__identifier = Identifiers.DEBUG
        elif m_type in ["trace"]:
            self.__main_color = colorama.Fore.MAGENTA
            self.__value_color = colorama.Fore.MAGENTA
            self.__identifier = Identifiers.STACKTRACE
        elif m_type in ["network"]:
            self.__main_color = colorama.Fore.BLUE
            self.__value_color = colorama.Fore.LIGHTBLUE_EX
            self.__identifier = Identifiers.NETWORK
        else:
            self.__main_color = colorama.Fore.RESET
            self.__value_color = colorama.Fore.RESET
            self.__identifier = " " * Identifiers.MAX_LENGTH


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


def show_healthcheck_info(version, status):
    print(f"{colorama.Fore.CYAN}CML-Bench Version: {colorama.Style.RESET_ALL}"
          f"{colorama.Fore.LIGHTCYAN_EX}{version}{colorama.Style.RESET_ALL}")
    if status == "success":
        color = colorama.Fore.LIGHTGREEN_EX
    else:
        color = colorama.Fore.LIGHTRED_EX
    print(f"{colorama.Fore.CYAN}Status           : {colorama.Style.RESET_ALL}{color}{status}{colorama.Style.RESET_ALL}")


def show_info_message(message, *values):
    __colored_message("info", message, *values)


def show_warning_message(message, *values):
    __colored_message("warning", message, *values)


def show_error_message(message, *values):
    __colored_message("error", message, *values)


def show_debug_message(message, *values):
    if Output.FULL:
        __colored_message("debug", message, *values)


def show_trace_message(message, *values):
    __colored_message("trace", message, *values)


def show_get_request(url):
    if Output.REQUESTS:
        __colored_message("network", "GET    > {}", url)


def show_post_request(url):
    if Output.REQUESTS:
        __colored_message("network", "POST   > {}", url)


def show_put_request(url):
    if Output.REQUESTS:
        __colored_message("network", "PUT    > {}", url)


def show_delete_request(url):
    if Output.REQUESTS:
        __colored_message("network", "DELETE > {}", url)


def get_blank():
    tmp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    return " " * (len(tmp) + Identifiers.MAX_LENGTH + 5)


def __colored_message(message_type, message, *values):
    properties = MessageProperties()
    properties.set_values(message_type)

    prog = re.compile(r"{}", re.X)
    result = prog.findall(message)

    if len(result) != len(values):
        if Output.FULL:
            print(__get_internal_simple_message("The number of placeholders does not match the number of parameters",
                                                colorama.Fore.MAGENTA,
                                                "DEBUG   "))
        print(__get_internal_simple_message(message, properties.main_color, properties.identifier))
    else:
        updated_parameters = [f"{properties.value_color}{v}{colorama.Style.RESET_ALL}{properties.main_color}"
                              for v in values]
        updated_message = __get_internal_simple_message(message, properties.main_color, properties.identifier)
        print(str(updated_message).format(*updated_parameters))


def __get_internal_simple_message(message, main_color, identifier):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    prefix = f"[{identifier}| {timestamp}] "
    return f"{main_color}{prefix}{message.strip()}{colorama.Style.RESET_ALL}"
