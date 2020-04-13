# coding: utf-8
import requests
from core.network.sender import Sender
from core.network.handler import Handler
from core.modules.authorization import Authorization
from core.modules.cml_bench_manager import CMLBenchManager


class AppSession(object):
    def __init__(self, **kwargs):
        if "cfg" in kwargs.keys():
            self.__configuration_information = kwargs.get("cfg")
            self.__http_session = requests.Session()
            self.__sender = Sender(self)
            self.__handler = Handler(self)
        else:
            raise ValueError("No configuration information available")
        if "credentials" in kwargs.keys():
            self.__key_file = kwargs.get("credentials")
        else:
            self.__key_file = None
        self.__sid = 1234

    @property
    def sid(self):
        return self.__sid

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

    @property
    def key_file_path(self):
        return self.__key_file

    def execute(self):
        try:
            authorization = Authorization(self)
            status = authorization.cml_bench_sign_in()

            if status:
                search_id = 683992
                cml_bench_manager = CMLBenchManager(self, search_id)
                cml_bench_manager.get_list_of_submodels()

        except Exception as e:
            import traceback
            print(e)
            print(traceback.format_exc())
        else:
            pass
        finally:
            self.__http_session.close()
