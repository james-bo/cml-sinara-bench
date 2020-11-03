# coding: utf-8
from ui.console import terminal
from core.utils.decorators import method_info


class Sender(object):
    def __init__(self, app_session):
        self.__app_session = app_session
        self.__http_session = self.__app_session.session
        self.__host = self.__app_session.cfg.backend_address

# ----------------------------------------------- Healthcheck requests ----------------------------------------------- #

    @method_info
    def send_healthcheck_request(self):
        url = f"{self.__host}/cml-bench/rest/version"
        response = self.__http_session.get(url)
        return response

# ---------------------------------------------- Authorization requests ---------------------------------------------- #

    @method_info
    def send_login_request(self, username, password, remember_me=False):
        url = f"{self.__host}/rest/login"
        response = self.__http_session.post(url, data={"username": username,
                                                       "password": password,
                                                       "remember-me": str(remember_me).lower})
        return response

# --------------------------------------------- Common entities requests --------------------------------------------- #

    @method_info
    def send_entity_base_info_request(self, entity_id, entity_type):
        url = f"{self.__host}/rest/{entity_type}/{entity_id}"
        terminal.show_get_request(url)
        response = self.__http_session.get(url)
        return response

# ------------------------------------------------ Loadcase requests ------------------------------------------------- #

    @method_info
    def send_loadcase_simulations_request(self, entity_id, max_number=10):
        url = f"{self.__host}/rest/loadcase/{entity_id}/simulation/list"
        terminal.show_post_request(url)
        response = self.__http_session.post(url,
                                            json={"filters": {},
                                                  "sort": [],
                                                  "pageable": {"size": max_number,
                                                               "page": 1}})
        return response

    @method_info
    def send_loadcase_targets_request(self, entity_id, max_number=10):
        url = f"{self.__host}/rest/loadcase/{entity_id}/targetValue/list"
        terminal.show_post_request(url)
        response = self.__http_session.post(url,
                                            json={"filters": {},
                                                  "sort": [],
                                                  "pageable": {"size": max_number,
                                                               "page": 1}})
        return response

    @method_info
    def send_add_loadcase_target_request(self, entity_id, payload):
        url = f"{self.__host}/rest/loadcase/{entity_id}/targetValue"
        terminal.show_post_request(url)
        response = self.__http_session.post(url,
                                            json=payload)
        return response

    @method_info
    def send_remove_loadcase_target_request(self, entity_id, payload):
        url = f"{self.__host}/rest/loadcase/{entity_id}/targetValue?ids={payload}"
        terminal.show_delete_request(url)
        response = self.__http_session.delete(url)
        return response

# ----------------------------------------------- Simulation requests ------------------------------------------------ #

    @method_info
    def send_modify_simulation_request(self, entity_id, payload):
        url = f"{self.__host}/rest/simulation/{entity_id}"
        terminal.show_put_request(url)
        response = self.__http_session.put(url, json=payload)
        return response

    @method_info
    def send_clone_simulation_request(self, entity_id, add_to_clipboard=False, dmu_id=None):
        url = f"{self.__host}/rest/simulation/{entity_id}/clone"
        terminal.show_post_request(url)
        response = self.__http_session.post(url,
                                            json={"addToClipboard": add_to_clipboard,
                                                  "dmuID": dmu_id})
        return response

    @method_info
    def send_simulation_tasks_request(self, entity_id, max_number=10):
        url = f"{self.__host}/rest/simulation/{entity_id}/tasks/list"
        terminal.show_post_request(url)
        response = self.__http_session.post(url,
                                            json={"filters": {},
                                                  "sort": [{"direction": "DESC",
                                                            "field": "modificationDate"}],
                                                  "pageable": {"size": max_number,
                                                               "page": 1}})
        return response

    @method_info
    def send_simulation_submodels_request(self, entity_id):
        url = f"{self.__host}/rest/simulation/{entity_id}/submodel"
        terminal.show_get_request(url)
        response = self.__http_session.get(url)
        return response

    @method_info
    def send_simulation_submodels_update_request(self, entity_id, sumbodels):
        url = f"{self.__host}/rest/simulation/{entity_id}/submodel"
        terminal.show_post_request(url)
        response = self.__http_session.post(url,
                                            json=[*sumbodels])
        return response

    @method_info
    def send_simulation_files_request(self, entity_id, max_number=100):
        url = f"{self.__host}/rest/simulation/{entity_id}/file/list"
        terminal.show_post_request(url)
        response = self.__http_session.post(url,
                                            json={"filters": {"list": [{"name": "path",
                                                                        "value": "Bench"}]},
                                                  "sort": [],
                                                  "pageable": {"size": max_number,
                                                               "page": 1}})
        return response

    @method_info
    def send_task_defaults_request(self, entity_id):
        url = f"{self.__host}/rest/simulation/{entity_id}/task/"
        terminal.show_get_request(url)
        response = self.__http_session.get(url)
        return response

    @method_info
    def send_download_file_request(self, entity_id, file_id):
        url = f"{self.__host}/rest/simulation/{entity_id}/file/{file_id}/export?_"
        terminal.show_get_request(url)
        response = self.__http_session.get(url)
        return response

    @method_info
    def send_run_request(self, parameters):
        url = f"{self.__host}/rest/task/"
        terminal.show_post_request(url)
        response = self.__http_session.post(url, json=parameters)
        return response

    @method_info
    def send_simulation_values_request(self, entity_id, max_number=10):
        url = f"{self.__host}/rest/simulation/{entity_id}/keyResult/list"
        terminal.show_post_request(url)
        response = self.__http_session.post(url, json={"filters": {"list": [{"name": "type",
                                                                             "value": "value"}]},
                                                       "sort": [],
                                                       "pageable": {"size": max_number,
                                                                    "page": 1}})
        return response

    @method_info
    def send_simulation_value_request(self, simulation_id, value_id):
        url = f"{self.__host}/rest/simulation/{simulation_id}/keyResult/{value_id}"
        terminal.show_get_request(url)
        response = self.__http_session.get(url)
        return response

# -------------------------------------------------- Task requests --------------------------------------------------- #

    @method_info
    def send_task_info_request(self, entity_id):
        from core.bench.entities import EntityTypes
        return self.send_entity_base_info_request(entity_id, EntityTypes.TASK.value)

# ------------------------------------------------ Submodel requests ------------------------------------------------- #

    @method_info
    def send_upload_submodel_request(self, file, stype_tree_id, add_to_clipboard="off"):
        url = f"{self.__host}/rest/submodel"
        terminal.show_post_request(url)
        with open(file, mode="rb") as f:
            response = self.__http_session.post(url,
                                                data={"pid": stype_tree_id,
                                                      "addToClipboard": add_to_clipboard},
                                                files={"file": f})
        return response

    @method_info
    def send_stype_submodels_request(self, entity_path, max_number=1000):
        url = f"{self.__host}/rest/submodel/list"
        terminal.show_post_request(url)
        response = self.__http_session.post(url,
                                            json={"filters": {"list": [{"name": "path",
                                                                        "value": entity_path}]},
                                                  "sort": [],
                                                  "pageable": {"size": max_number,
                                                               "page": 1}})
        return response

    @method_info
    def send_delete_submodel_from_server_request(self, entity_id):
        url = f"{self.__host}/rest/submodel/{entity_id}"
        terminal.show_delete_request(url)
        response = self.__http_session.delete(url)
        return response
