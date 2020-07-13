# coding: utf-8
import enum
from core.network.timeout import Timeout
from ui.console import terminal

# -------------------------------------------- Entity Types (Enumeration) -------------------------------------------- #


class EntityTypes(enum.Enum):
    LOADCASE = "loadcase"
    SIMULATION = "simulation"
    TASK = "task"
    STYPE = "submodelType"
    SUBMODEL = "submodel"

# ---------------------------------------------- Abstract Entity Object ---------------------------------------------- #


class AbstractEntity(object):
    """
    Class containing common behaviour of main CML-Bench entities, such as loadcases, simulations, tasks
    """
    def __init__(self, app_session, identifier):
        self._app_session = app_session
        self._identifier = identifier
        self._http_session = self._app_session.session
        self._sender = self._app_session.sender
        self._handler = self._app_session.handler

        self._entity_type = None
        self._name = None
        self._parent_id = None
        self._tree_path = None
        self._tree_id = None

    def __repr__(self):
        return "Entity type: {} | Entity ID: {}".format(self.entity_type, self.identifier)

    @property
    def entity_type(self):
        return self._entity_type

    @property
    def identifier(self):
        return self._identifier

    @property
    def name(self):
        return self._name

    @property
    def parent_id(self):
        return self._parent_id

    @property
    def tree_path(self):
        return self._tree_path

    @property
    def tree_id(self):
        return self._tree_id

    def _set_entity_type(self, entity_type):
        if isinstance(entity_type, EntityTypes):
            self._entity_type = entity_type

    def _setup_attributes(self):
        if self.entity_type:
            response = self._sender.send_entity_base_info_request(self.identifier, self.entity_type.value)
            Timeout.hold_your_horses()
            self._handler.set_response(response)
            base_info = self._handler.handle_response_to_entity_base_info_request()
            self._name = base_info.get("name")
            self._parent_id = base_info.get("parent_id")
            self._tree_path = base_info.get("tree_path")
            self._tree_id = base_info.get("tree_id")

# ------------------------------------------------- Loadcase Object -------------------------------------------------- #


class Loadcase(AbstractEntity):
    """
    Class for representation of the loadcase entity
    """
    def __init__(self, app_session, identifier):
        super().__init__(app_session, identifier)
        self._set_entity_type(EntityTypes.LOADCASE)
        self._setup_attributes()

    def get_simulations(self):
        """
        :return: list of simulations which belong to current loadcase,
                 or None, if some error occurred during reading simulations
        """
        terminal.show_info_objects(self.get_simulations, self.identifier)

        response = self._sender.send_loadcase_simulations_request(self.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        simulation_ids_list = self._handler.handle_response_to_loadcase_simulations_request()
        if simulation_ids_list:
            simulations = []
            for simulation_id in simulation_ids_list:
                simulations.append(Simulation(self._app_session, simulation_id))
            return simulations
        return None

    def get_targets(self):
        """
        :return: list of targets which belong to current loadcase,
                 or None, if some error occurred during reading targets
        """
        terminal.method_info(self.get_targets, self.identifier)

        response = self._sender.send_loadcase_targets_request(self.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        targets_data_list = self._handler.handle_response_to_loadcase_targets_request()
        if targets_data_list:
            targets = []
            for target_data in targets_data_list:
                targets.append(Target(target_data))
            return targets
        return None

    def add_target(self, name, value, condition, dimension, tolerance=None, description=None):
        """
        Adds new target to loadcase.
        If target with same name already exists, deletes old target and adds new.
        :param name: target name
        :param value: target value
        :param condition: target condition: 1 - >, 2 - <, 3 - +/-
        :param dimension: target dimension
        :param tolerance: tolerance for condition
        :param description: description for target
        :return: target object
        """
        terminal.method_info(self.add_target, self.identifier, name, value, condition, dimension,
                             tolerance=tolerance, description=description)

        if condition == 1:
            condition_name = ">"
        elif condition == 2:
            condition_name = "<"
        elif condition == 3:
            condition_name = "+/-"
        else:
            terminal.show_error_message("Unsupported condition for new target: {}".format(condition))
            return None

        if condition != 3:
            tolerance = None

        if tolerance is None:
            has_tolerance = False
        else:
            has_tolerance = True

        payload = {"conditionId": condition,
                   "conditionName": condition_name,
                   "description": description,
                   "dimension": dimension,
                   "hasTolerance": has_tolerance,
                   "hierarchy": {"id": self.identifier,
                                 "objectType": {"displayName": "Loadcase",
                                                "iconSkin": "icon-loadcase",
                                                "isLeaf": False,
                                                "name": "loadcase",
                                                "subType": None,
                                                "tooltip": "Loadcase"},
                                 "parent": None},
                   "name": name,
                   "objectType": {"displayName": "Target value",
                                  "name": "targetValue",
                                  "subType": None,
                                  "tooltip": "Target value"},
                   "tolerance": tolerance,
                   "value": value}
        response = self._sender.send_add_loadcase_target_request(self.identifier, payload)
        Timeout.hold_your_horses()

        # if no target with that name exists, create new
        # else, need to find ID of target by name
        # delete it
        # and create new
        if response.status_code == 400:
            terminal.show_warning_message(response.json().get("message"))
            existing_targets = self.get_targets()
            for t in existing_targets:
                if t.name == name:
                    tid = self.delete_target(t)
                    if tid is not None:
                        terminal.show_info_message("Old target successfully removed")
                    else:
                        terminal.show_error_message("Failed removing old target")
                        return None
                    break
            response = self._sender.send_add_loadcase_target_request(self.identifier, payload)

        if response.status_code != 200:
            terminal.show_error_message("Failed adding new target")
            terminal.show_error_message(f"Response: {response.status_code}")
            return None

        terminal.show_info_message("Adding new target...")
        self._handler.set_response(response)
        target_data = self._handler.handle_response_to_add_loadcase_target_request()

        if target_data:
            return Target(target_data)
        return None

    def delete_target(self, target):
        """
        Removes target from loadcase
        :param target: Target object
        :return: removed target ID or None, if some error occurred
        """
        terminal.method_info(self.delete_target, self.identifier, target)

        assert isinstance(target, Target)
        response = self._sender.send_remove_loadcase_target_request(self.identifier, target.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        target_id = self._handler.handle_response_to_remove_loadcase_target_request()
        return target_id

# ------------------------------------------------- Loadcase Target -------------------------------------------------- #


class Target(object):
    """
    Class for representation of the target entity
    """
    def __init__(self, data):
        assert isinstance(data, dict)
        self.__identifier = data.get("id")
        self.__name = data.get("name")
        self.__value = data.get("value")
        self.__condition = data.get("conditionId")
        self.__dimension = data.get("dimension")

    @property
    def identifier(self):
        return self.__identifier

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @property
    def condition(self):
        return self.__condition

    @property
    def dimension(self):
        return self.__dimension

# ---------------------------------------------- Simulation Key Result ----------------------------------------------- #


class Value(object):
    """
    Class for representation of the key result entity
    """
    def __init__(self, data):
        self.__key_result_id = data.get("id")
        self.__key_result_name = data.get("name")
        self.__key_result_value = data.get("value")
        self.__key_result_dimension = data.get("dimension")
        self.__key_result_description = data.get("description")
        self.__key_result_parent_id = data.get("parent")

    @property
    def identifier(self):
        return self.__key_result_id

    @property
    def name(self):
        return self.__key_result_name

    @property
    def value(self):
        return self.__key_result_value

    @property
    def dimension(self):
        return self.__key_result_dimension

    @property
    def description(self):
        return self.__key_result_description

    @property
    def parent(self):
        return self.__key_result_parent_id

# ------------------------------------------------ Simulation Object ------------------------------------------------- #


class Simulation(AbstractEntity):
    """
    Class for representation of the simulation entity
    """
    def __init__(self, app_session, identifier):
        super().__init__(app_session, identifier)
        self._set_entity_type(EntityTypes.SIMULATION)
        self._setup_attributes()

    def get_loadcase(self):
        """
        :return: parent loadcase of current simulation
        """
        terminal.method_info(self.get_loadcase, self.identifier)

        return Loadcase(self._app_session, self.parent_id)

    def get_tasks(self):
        """
        :return: return list of tasks which belong to current simulation,
                 or None, if some error occurred during reading tasks
        """
        terminal.method_info(self.get_tasks, self.identifier)

        response = self._sender.send_simulation_tasks_request(self.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        simulation_tasks_list = self._handler.handle_response_to_simulation_tasks_request()
        if simulation_tasks_list:
            tasks = []
            for task_id in simulation_tasks_list:
                tasks.append(Task(self._app_session, task_id))
            return tasks
        return None

    def get_files(self):
        """
        :return: return list of dictionaries like {id: fileName},
                 where fileName is a file belongs to current simulation,
                 or None, if some error occurred during reading files
        """
        terminal.method_info(self.get_files, self.identifier)

        response = self._sender.send_simulation_files_request(self.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        simulation_files_list_of_dicts = self._handler.handle_response_to_simulation_files_request()
        return simulation_files_list_of_dicts

    def get_values(self):
        """
        :return: return list of Values, or None, if some error occurred during reading
        """
        terminal.method_info(self.get_values, self.identifier)

        response = self._sender.send_simulation_values_request(self.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        simulation_values_data = self._handler.handle_response_to_simulation_values_request()
        values = []
        if simulation_values_data:
            for item_data in simulation_values_data:
                values.append(Value(item_data))
            return values
        return None

    def download_files(self, *files):
        """
        Download chosen files to local directory
        :param files: files to be downloaded
        :return: return list of successfully downloaded files
        """
        terminal.method_info(self.download_files, self.identifier, *files)

        list_of_downloaded_files = []
        simulation_files = self.get_files()
        list_of_simulation_file_ids = [item.get("id") for item in simulation_files]
        list_of_simulation_file_names = [item.get("name") for item in simulation_files]

        for file in files:
            # check if fileName is in simulation files
            if file in list_of_simulation_file_names:
                file_id = list_of_simulation_file_ids[list_of_simulation_file_names.index(file)]

                response = self._sender.send_download_file_request(self.identifier, file_id)
                Timeout.hold_your_horses()
                self._handler.set_response(response)
                file_content = self._handler.handle_response_to_download_file_request()
                if file_content and isinstance(file_content, bytes):
                    with open(self._app_session.cfg.local_storage + "\\" + file, mode="wb") as f:
                        f.write(file_content)
                    list_of_downloaded_files.append(file)
            else:
                terminal.show_warning_message("Selected file \"{}\" not in simulation files".format(file))
        return list_of_downloaded_files

    def clone(self):
        """
        Clone current simulation
        :return: return new simulation, or None, if some error occurred
        """
        terminal.method_info(self.clone, self.identifier)

        response = self._sender.send_clone_simulation_request(self.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        cloned_simulation_id = self._handler.handle_response_to_clone_simulation_request()
        if cloned_simulation_id:
            return Simulation(self._app_session, cloned_simulation_id)
        return None

    def get_submodels(self):
        """
        :return: return list of current simulation submodels, or None, if some error occurred
        """
        terminal.method_info(self.get_submodels, self.identifier)

        response = self._sender.send_simulation_submodels_request(self.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        simulation_submodels_ids = self._handler.handle_response_to_simulation_submodels_request()
        if simulation_submodels_ids:
            submodels = []
            for submodel_id in simulation_submodels_ids:
                submodels.append(Submodel(self._app_session, submodel_id))
            return submodels
        return None

    def add_submodels(self, *submodels):
        """
        Add new submodels to list of simulation submodels
        :param submodels: submodels to be added into current simulation
        :return: list of ALL simulation submodels
        """
        terminal.method_info(self.add_submodels, self.identifier, *submodels)

        assert all(isinstance(item, Submodel) for item in submodels)

        # First, get list of current submodels
        simulation_submodels = self.get_submodels()
        if not simulation_submodels:
            simulation_submodels = []

        # Append new submodels to the list of existing submodels
        simulation_submodels.extend(submodels)

        # List of IDs of all updated submodels
        simulation_submodels_ids = [submodel.identifier for submodel in simulation_submodels]

        # Send request to update simulation submodels (that's how it works in CML-Bench)
        response = self._sender.send_simulation_submodels_update_request(self.identifier, simulation_submodels_ids)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        updated_simulation_submodels_ids = self._handler.handle_response_to_simulation_submodels_request()
        if updated_simulation_submodels_ids:
            submodels = []
            for submodel_id in updated_simulation_submodels_ids:
                submodels.append(Submodel(self._app_session, submodel_id))
            return submodels
        return None

    def run(self, **parameters):
        """
        Run or post-process current simulation
        :param parameters: keywords for identify run or post-processor commands
                           "exec" - type of solver or post-processor to be run
                           "stb"  - storyboard id for "exec = VBA"
                           "bsi"  - base simulation ID
        :return: created Task or None if error occurred
        """
        terminal.method_info(self.run, self.identifier, **parameters)

        params = {}
        if "exec" in parameters.keys():
            executable = parameters.get("exec")
            if executable == "Nastran 2017":
                params = {
                          "parentType": {"name": "simulation"},
                          "solverName": "Nastran 2017",
                          "solvingType": "Solving",
                          "parentId": self.identifier
                         }
            if executable == "VBA":
                if "stb" in parameters.keys():
                    storyboard_id = parameters.get("stb")
                    params = {
                              "parentType": {"name": "simulation"},
                              "postprocessorName": "Microsoft Office Postprocessing",
                              "type": "postprocessing",
                              "parentId": self.identifier,
                              "storyboardId": storyboard_id
                             }
                else:
                    terminal.show_error_message("No storyboard selected. Cannot execute post-processor")
        else:
            if "bsi" in parameters.keys():
                base_simulation_id = parameters.get("bsi")
                received_params = self.__get_defaults(base_simulation_id)
            else:
                received_params = self.__get_defaults()

            if received_params is None:
                terminal.show_error_message("Failed to run simulation")
                return None

            # Modify `parentId` and `parentName` keys
            # __get_defaults() may return these parameters from another simulation
            # remove unnecessary parameters
            params["objectType"] = received_params.get("objectType")
            params["parentName"] = self.name
            params["owner"] = received_params.get("owner")
            params["ownerId"] = received_params.get("ownerId")
            params["id"] = received_params.get("id")
            params["numOfCores"] = received_params.get("numOfCores")
            params["memory"] = received_params.get("memory")
            params["storyboard"] = received_params.get("storyboard")
            params["storyboardId"] = received_params.get("storyboardId")
            params["solverName"] = received_params.get("solverName")
            params["solverDisplayName"] = received_params.get("solverDisplayName")
            params["clusterName"] = received_params.get("clusterName")
            params["solverGroup"] = received_params.get("solverGroup")
            params["type"] = received_params.get("type")
            params["typeDisplayName"] = received_params.get("typeDisplayName")
            params["solvingType"] = received_params.get("solvingType")
            params["notified"] = received_params.get("notified")
            params["startupArguments"] = received_params.get("startupArguments")
            params["autoCreateReport"] = received_params.get("autoCreateReport")
            params["withPostprocessing"] = received_params.get("withPostprocessing")
            params["postprocessorName"] = received_params.get("postprocessorName")
            params["parentType"] = received_params.get("parentType")
            params["parentId"] = self.identifier
            params["cluster"] = received_params.get("cluster")
            params["clusterId"] = received_params.get("clusterId")
            params["expectedSolvingTime"] = received_params.get("expectedSolvingTime")

        # terminal.show_info_dict("Run request payload parameters:", params)

        response = self._sender.send_run_request(params)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        task_id = self._handler.handle_response_to_run_request()
        if task_id:
            return Task(self._app_session, task_id)
        return None

    def __get_defaults(self, base_simulation_id=None):
        """
        Obtain default parameters for run/post-process task
        :param base_simulation_id: ID of base simulation for getting defaults
        :return: dictionary containing default task running parameters such as solver, cluster, etc.
        """
        terminal.method_info(self.__get_defaults, self.identifier, base_simulation_id=base_simulation_id)

        if base_simulation_id:
            response = self._sender.send_task_defaults_request(base_simulation_id)
        else:
            response = self._sender.send_task_defaults_request(self.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        task_startup_defaults = self._handler.handle_response_to_task_defaults_request()
        return task_startup_defaults

# --------------------------------------------------- Task Object ---------------------------------------------------- #


class Task(AbstractEntity):
    """
    Class for representation of the task entity
    """
    def __init__(self, app_session, identifier):
        super().__init__(app_session, identifier)
        self._set_entity_type(EntityTypes.TASK)
        self._setup_attributes()

    def get_status(self):
        """
        :return: current task status, or None, if error occurred
        """
        response = self._sender.send_task_info_request(self.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        task_status = self._handler.handle_response_to_task_status_response()
        return task_status

    def get_time_estimation(self):
        """
        :return: tuple of string representation of end waiting and end solving time, or (None, None) if error occurred
        """
        response = self._sender.send_task_info_request(self.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        task_end_waiting, task_end_solving = self._handler.handle_response_to_task_estimations_response()
        return task_end_waiting, task_end_solving

# -------------------------------------------------- S|Type Object --------------------------------------------------- #


class SubmodelType(AbstractEntity):
    """
    Class for representation of the s|type entity
    """
    def __init__(self, app_session, identifier):
        super().__init__(app_session, identifier)
        self._set_entity_type(EntityTypes.STYPE)
        self._setup_attributes()

    def get_submodels(self):
        """
        :return: list of existing submodels in current s|type, or None, if some error occurred
        """
        response = self._sender.send_stype_submodels_request(self.tree_path)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        stype_submodels_list = self._handler.handle_response_to_stype_submodels_requests()
        if stype_submodels_list:
            submodels = []
            for submodel_id in stype_submodels_list:
                submodels.append(Submodel(self._app_session, submodel_id))
            return submodels
        return None

    def upload_submodel(self, *files, **params):
        """
        :param files: paths to files to be uploaded into current s|type
        :param params: response parameters;
                       `stype` - ID of s|type for uploading submodels; optional; default is current s|type
                       `add_to_clipboard` - optional boolean parameter; default is False
        :return: list of uploaded submodels
        """
        # FIXME wtf??? create instance of SubmodelType inside its method
        if "stype" in params.keys():
            stype = SubmodelType(self._app_session, params.get("stype"))
        else:
            # stype = SubmodelType(self._app_session, self._app_session.cfg.server_storage)
            stype = self

        if "add_to_clipboard" in params.keys():
            add_to_clipboard = "on" if bool(params.get("add_to_clipboard")) else "off"
        else:
            add_to_clipboard = "off"

        submodels = []
        for file in files:
            response = self._sender.send_upload_submodel_request(file, stype.tree_id, add_to_clipboard)
            Timeout.hold_your_horses()
            self._handler.set_response(response)
            submodel_id_result = self._handler.handle_response_to_upload_submodel_request()
            if submodel_id_result and not isinstance(submodel_id_result, list):
                submodels.append(Submodel(self._app_session, submodel_id_result))
            if submodel_id_result and isinstance(submodel_id_result, list):
                # there are duplicates, hence deleting all but original
                for submodel_id in submodel_id_result:
                    response = self._sender.send_delete_submodel_from_server_request(submodel_id)
                    Timeout.hold_your_horses()
                    self._handler.set_response(response)
                    _ = self._handler.handle_response_to_delete_submodel_from_server_request()
                    terminal.show_warning_message("Duplicates was deleted")
        return submodels

# ------------------------------------------------- Submodel Object -------------------------------------------------- #


class Submodel(AbstractEntity):
    """
    Class for representation of the submodel entity
    """
    def __init__(self, app_session, identifier):
        super().__init__(app_session, identifier)
        self._set_entity_type(EntityTypes.SUBMODEL)
        self._setup_attributes()
