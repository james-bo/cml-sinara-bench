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
                if path:
                    if isinstance(path, list):
                        if len(path) > 1:
                            parent = path[-2]
                            if isinstance(parent, dict):
                                parent_id = parent.get("objectId")
                                return parent_id
                else:
                    parent_id = response_json.get("parentId")
                    if parent_id:
                        return parent_id
        terminal.show_error_message("There were some errors during reading entity parent id.")
        return None

    def handle_response_to_entity_tree_id_request(self):
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict):
            links = response_json.get("links")
            if links:
                if isinstance(links, list):
                    if len(links) > 0 and isinstance(links[0], dict):
                        path = links[0].get("path")
                        if isinstance(path, list):
                            if len(path) > 1:
                                this = path[-1]
                                if isinstance(this, dict):
                                    this_tree_id = this.get("id")
                                    return this_tree_id
        terminal.show_error_message("There were some errors during reading entity tree id.")
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

    def handle_response_to_loadcase_simulations_request(self):
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict):
            list_of_simulations = []
            content = response_json.get("content")
            if content:
                for item in content:
                    if item and isinstance(item, dict):
                        simulation_id = item.get("id")
                        if simulation_id:
                            list_of_simulations.append(simulation_id)
                return list_of_simulations
            terminal.show_warning_message("No simulations read from loadcase!")
            return []
        terminal.show_error_message("There were some errors during reading loadcase simulations!")
        return None

    def handle_response_to_task_status_response(self):
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict):
            task_status = response_json.get("status")
            if task_status:
                return task_status
        terminal.show_error_message("Failed to get task status.")
        return None

    def handle_response_to_simulation_tasks_request(self):
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict):
            list_of_tasks = []
            content = response_json.get("content")
            if content:
                for item in content:
                    if item and isinstance(item, dict):
                        task_id = item.get("id")
                        if task_id:
                            list_of_tasks.append(task_id)
                return list_of_tasks
            terminal.show_warning_message("No tasks read from simulation!")
            return []
        terminal.show_error_message("There were some errors during reading simulation tasks!")
        return None

    def handle_response_to_simulation_submodels_request(self):
        response_json = self.__response.json()
        list_of_submodels = []
        if response_json and isinstance(response_json, list):
            for item in response_json:
                if item and isinstance(item, dict):
                    item_id = item.get("id")
                    if item_id:
                        list_of_submodels.append(item_id)
            return list_of_submodels
        terminal.show_error_message("There were some errors during reading simulation submodels!")
        return None

    def handle_response_to_upload_submodel_request(self):
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict):
            status = response_json.get("status")
            if status == "success":
                submodels = response_json.get("set")
                if submodels and isinstance(submodels, list):
                    if len(submodels) > 1:
                        if isinstance(submodels[0], dict):
                            submodel_id = submodels[0].get("id")
                            return submodel_id
        terminal.show_error_message("There were some errors during uploading new submodel!")
        return None

