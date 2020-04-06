# coding: utf-8
import requests
from core.network.sender import Sender
from core.network.handler import Handler
from core.modules.authorization import Authorization


class AppSession(object):
    def __init__(self, **kwargs):
        if "cfg" in kwargs.keys():
            self.__configuration_information = kwargs.get("cfg")
            self.__http_session = requests.Session()
            self.__sender = Sender(self, self.cfg)
            self.__handler = Handler(self)
        else:
            raise ValueError("No configuration information available")

    @property
    def cfg(self):
        return self.__configuration_information

    @property
    def session(self):
        return self.__http_session

    @property
    def sender(self):
        return self.__sender

    @property
    def handler(self):
        return self.__handler

    def execute(self):
        try:
            authorization = Authorization(self)
            authorization.cml_bench_sign_in()
        except Exception as e:
            import traceback
            print(e)
            print(traceback.format_exc())
        else:
            pass
        finally:
            self.__http_session.close()
