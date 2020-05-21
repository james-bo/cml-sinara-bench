# coding: utf-8
from ui.console import terminal


class Sender(object):
    def __init__(self, app_session):
        self.__app_session = app_session
        self.__http_session = self.__app_session.session
        self.__host = self.__app_session.cfg.backend_address

# Authorization requests

    def send_login_request(self, username, password, remember_me=False):
        url = "{}/rest/login".format(self.__host)
        response = self.__http_session.post(url, data={"username": username,
                                                       "password": password,
                                                       "remember-me": str(remember_me).lower})
        return response

# Common entities requests

    def send_entity_base_info_request(self, entity_id, entity_type):
        url = "{}/rest/{}/{}".format(self.__host, entity_type, entity_id)
        terminal.show_get_request(url)
        response = self.__http_session.get(url)
        return response

# Loadcase requests

    def send_loadcase_simulations_request(self, entity_id, max_number=10):
        url = "{}/rest/loadcase/{}/simulation/list".format(self.__host, entity_id)
        response = self.__http_session.post(url,
                                            json={"filters": {},
                                                  "sort": [],
                                                  "pageable": {"size": max_number,
                                                               "page": 1}})
        return response

# Simulation requests

    def send_clone_simulation_request(self, entity_id, add_to_clipboard=False, dmu_id=None):
        url = "{}/rest/simulation/{}/clone".format(self.__host, entity_id)
        response = self.__http_session.post(url,
                                            json={"addToClipboard": add_to_clipboard,
                                                  "dmuID": dmu_id})
        return response

    def send_simulation_tasks_request(self, entity_id, max_number=10):
        url = "{}/rest/simulation/{}/tasks/list".format(self.__host, entity_id)
        response = self.__http_session.post(url,
                                            json={"filters": {},
                                                  "sort": [{"direction": "DESC",
                                                            "field": "modificationDate"}],
                                                  "pageable": {"size": max_number,
                                                               "page": 1}})
        return response

    def send_simulation_submodels_request(self, entity_id):
        url = "{}/rest/simulation/{}/submodel".format(self.__host, entity_id)
        response = self.__http_session.get(url)
        return response

    def send_simulation_submodels_update_request(self, entity_id, sumbodels):
        url = "{}/rest/simulation/{}/submodel".format(self.__host, entity_id)
        response = self.__http_session.post(url,
                                            json=[*sumbodels])
        return response

    def send_simulation_files_request(self, entity_id, max_number=100):
        url = "{}/rest/simulation/{}/file/list".format(self.__host, entity_id)
        response = self.__http_session.post(url,
                                            json={"filters": {"list": [{"name": "path",
                                                                        "value": "Bench"}]},
                                                  "sort": [],
                                                  "pageable": {"size": max_number,
                                                               "page": 1}})
        return response

    def send_task_defaults_request(self, entity_id):
        url = "{}/rest/simulation/{}/task/".format(self.__host, entity_id)
        response = self.__http_session.get(url)
        return response

    def send_download_file_request(self, entity_id, file_id):
        url = "{}/rest/simulation/{}/file/{}/export?_".format(self.__host, entity_id, file_id)
        response = self.__http_session.get(url)
        return response

    def send_run_request(self, **parameters):
        url = "{}/rest/task/".format(self.__host)
        response = self.__http_session.post(url, json=parameters)
        return response

# Task requests

    def send_task_status_request(self, entity_id):
        from core.bench.entities import EntityTypes
        return self.send_entity_base_info_request(entity_id, EntityTypes.TASK)

# Submodel requests

    def send_upload_submodel_request(self, file, stype_tree_id, add_to_clipboard="off"):
        url = "{}/rest/submodel".format(self.__host)
        with open(file, mode="rb") as f:
            response = self.__http_session.post(url,
                                                data={"pid": stype_tree_id,
                                                      "addToClipboard": add_to_clipboard},
                                                files={"file": f})
        return response

    def send_stype_submodels_request(self, entity_path, max_number=1000):
        url = "{}/rest/submodel/list".format(self.__host)
        response = self.__http_session.post(url,
                                            json={"filters": {"list": [{"name": "path",
                                                                        "value": entity_path}]},
                                                  "sort": [],
                                                  "pageable": {"size": max_number,
                                                               "page": 1}})
        return response

    def send_delete_submodel_from_server_request(self, entity_id):
        url = "{}/rest/submodel/{}".format(self.__host, entity_id)
        response = self.__http_session.delete(url)
        return response
