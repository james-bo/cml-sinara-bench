# coding: utf-8
from ui.console import terminal


class Authorization(object):
    def __init__(self, app_session):
        self.__app_session = app_session
        self.__http_session = self.__app_session.session
        self.__sender = self.__app_session.sender
        self.__handler = self.__app_session.handler
        self.__username = ""
        self.__password = ""

    def cml_bench_sign_in(self):
        """
        Establish active connection to CML-Bench
        :return: connection status (True or False)
        """
        self.__username = terminal.request_string_input("Username")
        self.__password = terminal.request_hidden_input("Password")

        login_response = self.__sender.send_login_request(self.__username, self.__password, False)
        self.__handler.set_response(login_response)
        connection_status = self.__handler.handle_response_to_login_request()
        if not connection_status:
            self.__username = ''
            self.__password = ''
        return connection_status
