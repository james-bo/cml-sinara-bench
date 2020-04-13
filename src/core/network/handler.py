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

    def handle_response_to_entity_name_request(self):
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict):
            name = response_json.get("name")
            if name:
                return name
        terminal.show_error_message("Failed to get entity name!")
        return None

    def handle_response_to_entity_parent_id_request(self):
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict):
            links = response_json.get("links")
            if links:
                if isinstance(links, list):
                    if len(links) > 0 and isinstance(links[0], dict):
                        path = links[0].get("path")
                        if isinstance(path, list):
                            if len(path) > 1:
                                parent = path[-2]
                                if isinstance(parent, dict):
                                    parent_id = parent.get("objectId")
                                    return parent_id
            else:
                path = response_json.get("path")
                if isinstance(path, list):
                    if len(path) > 1:
                        parent = path[-2]
                        if isinstance(parent, dict):
                            parent_id = parent.get("objectId")
                            return parent_id
        terminal.show_error_message("There were some errors during reading entity parent id.")
        return None

    def handle_response_to_entity_tree_path_request(self):
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict):
            links = response_json.get("links")
            if links:
                if isinstance(links, list):
                    if len(links) > 0 and isinstance(links[0], dict):
                        path_names = links[0].get("pathNames")
                        if path_names:
                            return path_names
            else:
                path_names = response_json.get("pathNames")
                if path_names:
                    return path_names
        terminal.show_error_message("There were some errors during reading entity tree path.")
        return None

    def handle_response_to_clone_simulation_request(self):
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict):
            simulation_id = response_json.get("id")
            if simulation_id:
                return simulation_id
        terminal.show_error_message("Failed to clone simulation.")
        return None
