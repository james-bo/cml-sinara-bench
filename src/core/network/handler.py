# coding: utf-8
from ui.console import terminal


class Handler(object):
    def __init__(self, app_session, response=None):
        self.__response = response
        self.__app_session = app_session
        self.__http_session = self.__app_session.session

    def set_response(self, response):
        self.__response = response

# Authorization requests

    def handle_response_to_login_request(self):
        """
        Handles response to login request
        :return: True if connection has been established, False otherwise
        """
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict):
            user = response_json.get("login")
            if user:
                terminal.show_info_message("Successfully connected as {}!".format(user))
                return True
        terminal.show_error_message("Failed to connect!")
        return False

# Common entities requests

    def handle_response_to_entity_base_info_request(self):
        """
        Handles response to basic information about CML-Bench entity: name, parent ID, path in tree, tree ID
        :return: dictionary with keys `name`, `parent_id`, `tree_path`, `tree_id`
        """
        response_json = self.__response.json()
        info = {"name": None,
                "parent_id": None,
                "tree_path": None,
                "tree_id": None}

        if response_json and isinstance(response_json, dict):
            name = response_json.get("name")
            info["name"] = name

            links = response_json.get("links")
            if links and isinstance(links, list):
                if len(links) > 0 and isinstance(links[0], dict):
                    path = links[0].get("path")
                    if path and isinstance(path, list):
                        if len(path) > 0:
                            this = path[-1]
                            if this and isinstance(this, dict):
                                this_tree_id = this.get("id")
                                info["tree_id"] = this_tree_id
                        if len(path) > 1:
                            parent = path[-2]
                            if parent and isinstance(parent, dict):
                                parent_id = parent.get("objectId")
                                info["parent_id"] = parent_id
                    path_names = links[0].get("pathNames")
                    info["tree_path"] = path_names
            else:
                path = response_json.get("path")
                if path and isinstance(path, list):
                    if len(path) > 1:
                        parent = path[-2]
                        if parent and isinstance(parent, dict):
                            parent_id = parent.get("objectId")
                            info["parent_id"] = parent_id
                else:
                    parent_id = response_json.get("parentId")
                    info["parent_id"] = parent_id
                path_names = response_json.get("pathNames")
                info["tree_path"] = path_names

        return info

# Loadcase requests

    def handle_response_to_loadcase_simulations_request(self):
        """
        Handles response to loadcase simulations request
        :return: list containing IDs of loadcase simulations, or None, if some error occurred
        """
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

# Simulation requests

    def handle_response_to_clone_simulation_request(self):
        """
        Handles response to clone simulation request
        :return: ID of cloned simulation, or None, if some error occurred
        """
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict):
            simulation_id = response_json.get("id")
            if simulation_id:
                return simulation_id
        terminal.show_error_message("Failed to clone simulation.")
        return None

    def handle_response_to_simulation_tasks_request(self):
        """
        Handles response to simulation tasks request
        :return: list containing IDs of simulation tasks, or None, if some error occurred
        """
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
        """
        Handles response to simulation submodels request
        :return: list containing IDs of simulation submodels, or None, if some error occurred
        """
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

    def handle_response_to_simulation_files_request(self):
        """
        Handles response to simulation files request
        :return: list of dictionaries with keys `id`, `name`, representing simulation files,
                 or None, if some error occurred
        """
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict):
            list_of_files = []
            content = response_json.get("content")
            if content and isinstance(content, list):
                for item in content:
                    if item and isinstance(item, dict):
                        file_id = item.get("id")
                        file_name = item.get("name")
                        if file_id and file_name:
                            list_of_files.append({"id": file_id, "name": file_name})
                return list_of_files
        terminal.show_error_message("There were some errors during reading simulation files!")
        return None

    def handle_response_to_task_defaults_request(self):
        """
        Handles response to default task parameters request
        :return: dictionary with request json parameters to run new task, or None, if some error occurred
        """
        response = self.__response
        response_json_list = response.json()
        if isinstance(response_json_list, list) and response_json_list:
            defaults_json = response_json_list[0]
            if defaults_json and isinstance(defaults_json, dict):
                return defaults_json
        if response.status_code == 200 and not response_json_list:
            terminal.show_error_message("Simulation defaults for task were not found!")
            return None
        terminal.show_error_message("There were some errors during reading task defaults of this simulation!")
        return None

    def handle_response_to_download_file_request(self):
        """
        Handles response to download file requeest
        :return: response content (binary data) or None, response status code is not 200
        """
        response = self.__response
        if response.status_code == 200:
            return response.content
        return None

    def handle_response_to_run_request(self):
        """
        Handles response to run request
        :return: task ID if new task was created, or None otherwise
        """
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict) and ("id" in response_json):
            task_identifier = response_json.get("id")
            return task_identifier
        if response_json and isinstance(response_json, dict) and ("message" in response_json):
            message = response_json.get("message")
            terminal.show_error_message("Couldn't send simulation to run: \"{}!\"".format(message))
            return None
        terminal.show_error_message("There were some errors during sending simulation to run!")
        return None

# Task requests

    def handle_response_to_task_status_response(self):
        """
        Handles response to task status request
        :return: current task status, or None, if some error occurred
        """
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict):
            task_status = response_json.get("status")
            if task_status:
                return task_status
        terminal.show_error_message("Failed to get task status.")
        return None

# Submodel requests

    def handle_response_to_upload_submodel_request(self):
        """
        Handles response to upload submodel request
        :return: uploaded submodel ID, or list of duplicates IDs, or None, of some error occurred
        """
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict):
            status = response_json.get("status")
            if status == "success":
                submodels = response_json.get("set")
                if submodels and isinstance(submodels, list):
                    if len(submodels) > 0:
                        if isinstance(submodels[0], dict):
                            submodel_id = submodels[0].get("id")
                            return submodel_id
            if status == "warning":
                duplicates = response_json.get("duplicates")
                if duplicates and isinstance(duplicates, list):
                    terminal.show_warning_message("There are duplicate submodels on server!")
                    if len(duplicates) > 0:
                        if isinstance(duplicates[0], dict):
                            created_object = duplicates[0].get("createdObject")
                            # Bench by default gets duplicates over all of its storage thus
                            # getting parent id, and filtering all submodels which belong to the parent directory
                            created_object_pid = created_object.get("pid")
                            duplicate_objects = duplicates[0].get("duplicateObjects")
                            if duplicate_objects and isinstance(duplicates, list):
                                duplicates_id = []
                                for submodel in duplicate_objects[1:]:  # duplicate_objects[0] is original submodel
                                    submodel_pid = submodel.get("pid")
                                    if submodel_pid == created_object_pid:
                                        submodel_id = submodel.get("id")
                                        duplicates_id.append(submodel_id)
                                created_object_id = created_object.get("id")
                                duplicates_id.append(created_object_id)
                                return duplicates_id
        terminal.show_error_message("There were some errors during uploading new submodel!")
        return None

    def handle_response_to_stype_submodels_requests(self):
        """
        Handles response to s|type submodels request
        :return: list of submodel IDs, containing in current s|type, or None, if some error occurred
        """
        response_json = self.__response.json()
        if response_json and isinstance(response_json, dict):
            list_of_submodels = []
            content = response_json.get("content")
            if content and isinstance(content, list):
                for item in content:
                    if item and isinstance(item, dict):
                        submodel_id = item.get("id")
                        if submodel_id:
                            list_of_submodels.append(submodel_id)
                return list_of_submodels
        terminal.show_error_message("There were some errors during reading s|type submodels!")
        return None

    def handle_response_to_delete_submodel_from_server_request(self):
        """
        Handles response to delete submodel from server request
        :return: deleted submodel ID, if successfully deleted, or None otherwise
        """
        response = self.__response

        if response.status_code == 200:
            response_json = self.__response.json()
            deleted_submodel_identifier = response_json.get("id")
            if deleted_submodel_identifier:
                return deleted_submodel_identifier

        if response.status_code == 409:
            response_json = self.__response.json()
            if response_json and isinstance(response_json, dict):
                message = response_json.get("message")
                terminal.show_error_message("There were conflicts during deleting submodel from server: \"{}\"".format(
                    message))
                return None

        if response.status_code == 403:
            response_json = self.__response.json()
            if response_json and isinstance(response_json, dict):
                message = response_json.get("message")
                terminal.show_error_message("There were conflicts during deleting submodel from server: \"{}\"".format(
                    message))
                return None

        # print(response)
        terminal.show_error_message("There were some errors during deleting submodel from server!")
        return None
