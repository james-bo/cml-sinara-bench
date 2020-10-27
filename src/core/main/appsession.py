# coding: utf-8
import requests
import uuid
from core.network.sender import Sender
from core.network.handler import Handler
from core.modules.healthcheck import Healthcheck
from core.modules.authorization import Authorization
from core.modules.workflow import WorkFlow
from ui.console import terminal
from core.utils.decorators import method_info
from core.utils.exception_manager import handle_unexpected_exception


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

        if "json" in kwargs.keys():
            self.__json_file = kwargs.get("json")
        else:
            raise ValueError("No JSON file selected")

        if "res" in kwargs.keys():
            self.__save_results_path = kwargs.get("res")
        else:
            self.__save_results_path = None

        if "root" in kwargs.keys():
            self.__root_path = kwargs.get("root")
        else:
            raise ValueError("No root path selected")

        self.__sid = uuid.uuid1()

    @property
    def sid(self):
        return str(self.__sid)

    @property
    def cfg(self):
        return self.__configuration_information

    @property
    def root(self):
        return self.__root_path

    @property
    def json(self):
        return self.__json_file

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
    def credentials(self):
        return self.__key_file

    @property
    def results_path(self):
        return self.__save_results_path

    @method_info
    def execute(self):
        try:
            healthcheck = Healthcheck(self)
            state = healthcheck.get_status()
            if state is not None:
                terminal.show_healthcheck_info(version=state[0], status=state[1])
            else:
                raise ValueError("Healthcheck failed")

            authorization = Authorization(self)
            status = authorization.cml_bench_sign_in()

            if status:
                workflow = WorkFlow(self)
                # God bless this script
                workflow.process_json()
        except Exception as e:
            raise Exception(e)
        finally:
            self.__http_session.close()
