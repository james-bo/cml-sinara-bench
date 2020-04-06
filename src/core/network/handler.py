# coding: utf-8
from ui.console import terminal


class Handler(object):
    def __init__(self, app_session, response=None):
        self.__response = response
        self.__app_session = app_session
        self.__http_session = self.__app_session.session

    def set_response(self, response):
        self.__response = response

    def handle_response_to_login_request(self):
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict):
            user = response_json.get("login")
            if user:
                terminal.show_info_message("Successfully connected as {}!".format(user))
                return True
        terminal.show_error_message("Failed to connect!")
        return False
