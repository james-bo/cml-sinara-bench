# coding: utf-8


class Sender(object):
    def __init__(self, app_session):
        self.__app_session = app_session
        self.__http_session = self.__app_session.session
        self.__host = self.__app_session.cfg.backend_address

    def send_login_request(self, username, password, remember_me=False):
        url = "{}/rest/login".format(self.__host)
        response = self.__http_session.post(url, data={"username": username,
                                                       "password": password,
                                                       "remember-me": str(remember_me).lower})
        return response

    def _send_entity_base_info_request(self, entity_id, entity_type):
        url = "{}/rest/{}/{}".format(self.__host, entity_type, entity_id)
        response = self.__http_session.get(url)
        return response

    def send_entity_name_request(self, entity_id, entity_type):
        return self._send_entity_base_info_request(entity_id, entity_type)

    def send_entity_parent_id_request(self, entity_id, entity_type):
        return self._send_entity_base_info_request(entity_id, entity_type)

    def send_entity_tree_path_request(self, entity_id, entity_type):
        return self._send_entity_base_info_request(entity_id, entity_type)

    def send_entity_tree_id_request(self, entity_id, entity_type):
        return self._send_entity_base_info_request(entity_id, entity_type)

    def send_clone_simulation_request(self, entity_id, add_to_clipboard=False, dmu_id=None):
        url = "{}/rest/simulation/{}/clone".format(self.__host, entity_id)
        response = self.__http_session.post(url,
                                            json={"addToClipboard": add_to_clipboard,
                                                  "dmuID": dmu_id})
        return response

    def send_loadcase_simulations_request(self, entity_id, max_number=10):
        url = "{}/rest/loadcase/{}/simulation/list".format(self.__host, entity_id)
        response = self.__http_session.post(url,
                                            json={"filters": {},
                                                  "sort": [],
                                                  "pageable": {"size": max_number,
                                                               "page": 1}})
        return response

    def send_task_status_request(self, entity_id):
        from core.bench.entities import EntityTypes
        return self._send_entity_base_info_request(entity_id, EntityTypes.TASK)

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

    def send_upload_submodel_request(self, file, stype, add_to_clipboard="off"):
        url = "{}/rest/submodel".format(self.__host)
        with open(file, mode="rb") as f:
            response = self.__http_session.post(url,
                                                data={"file": f,
                                                      "pid": stype,
                                                      "addToClipboard": add_to_clipboard})
        return response
