# coding: utf-8


class Sender(object):
    def __init__(self, app_session, config):
        self.__app_session = app_session
        self.__config = config
        self.__http_session = self.__app_session.session
        self.__host = self.__config.backend_address

    def send_login_request(self, username, password, remember_me=False):
        url = "{}/rest/login".format(self.__host)
        response = self.__http_session.post(url, data={"username": username,
                                                       "password": password,
                                                       "remember-me": str(remember_me).lower})
        return response
