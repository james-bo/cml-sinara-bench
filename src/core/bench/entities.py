# coding: utf-8
import enum
from core.network.timeout import Timeout
from ui.console import terminal


class EntityTypes(enum.Enum):
    LOADCASE = "loadcase"
    SIMULATION = "simulation"
    TASK = "task"
    STYPE = "submodelType"
    SUBMODEL = "submodel"


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


class Loadcase(AbstractEntity):
    """
    Class for representation of the loadcase entity
    """
    def __init__(self, app_session, identifier):
        super().__init__(app_session, identifier)
        self._set_entity_type(EntityTypes.LOADCASE)
        self._setup_attributes()

    def get_list_of_simulations(self):
        """
        Method for getting a list of simulations, belonging to the loadcase
        :return: list of simulation objects, or None if some error occurred during reading simulations
        """
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


class Simulation(AbstractEntity):
    """
    Class for representation of the simulation entity
    """
    def __init__(self, app_session, identifier):
        super().__init__(app_session, identifier)
        self._set_entity_type(EntityTypes.SIMULATION)
        self._setup_attributes()

    def clone(self):
        """
        Method for creating a new simulation, based on the current one
        :return: id of the new simulation, or None if failed to clone simulation
        """
        response = self._sender.send_clone_simulation_request(self.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        return self._handler.handle_response_to_clone_simulation_request()

    def get_parent_loadcase(self):
        """
        Method for getting a parent loadcase
        :return: loadcase object
        """
        return Loadcase(self._app_session, self.parent_id)

    def get_list_of_tasks(self):
        """
        Method for getting a list of tasks, belonging to the simulation
        :return: list of task objects, or None if some error occurred during reading tasks
        """
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

    def get_list_of_submodels(self):
        """
        Method for getting a list of submodels, belonging to the simulation
        :return: list of submodels, or None if some error occurred during reading submodels
        """
        response = self._sender.send_simulation_submodels_request(self.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        simulation_submodels_list = self._handler.handle_response_to_simulation_submodels_request()
        if simulation_submodels_list:
            submodels = []
            for submodel_id in simulation_submodels_list:
                submodels.append(Submodel(self._app_session, submodel_id))
            return submodels
        return None

    def get_list_of_files(self):
        response = self._sender.send_simulation_files_request(self.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        simulation_files_list_of_dicts = self._handler.handle_response_to_simulation_files_request()
        return simulation_files_list_of_dicts

    def download_files(self, files):
        """
        Method for donwloading files which belong to the simulation
        :return: list of dicts representing successfully downloaded files {id: 12, name: "file.txt"}
        """
        list_of_downloaded_files = []
        for file in files:
            response = self._sender.send_download_file_request(self.identifier, file["id"])
            Timeout.hold_your_horses()
            self._handler.set_response(response)
            file_content = self._handler.handle_response_to_download_file_request()
            if file_content and isinstance(file_content, bytes):
                with open(self._app_session.cfg.local_storage + "\\" + file["name"], mode="wb") as f:
                    f.write(file_content)
                list_of_downloaded_files.append(file)
        return list_of_downloaded_files

    def add_new_sumbodels(self, new_submodel_ids):
        # First, get list of current submodels
        response = self._sender.send_simulation_submodels_request(self.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        simulation_submodels_list = self._handler.handle_response_to_simulation_submodels_request()
        if not simulation_submodels_list:
            simulation_submodels_list = []
        # Append new submodel to the list of existing submodels
        simulation_submodels_list.extend(new_submodel_ids)
        # Send request to update simulation submodels (that's how it works in CML-Bench)
        response = self._sender.send_simulation_submodels_update_request(self.identifier, simulation_submodels_list)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        simulation_submodels_list = self._handler.handle_response_to_simulation_submodels_request()
        if simulation_submodels_list:
            submodels = []
            for submodel_id in simulation_submodels_list:
                submodels.append(Submodel(self._app_session, submodel_id))
            return submodels
        return None

    def get_simulation_task_defaults(self):
        """
        Method for obtaining default paremeters for run/post-processing task
        :return:
        """
        response = self._sender.send_task_defaults_request(self.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        task_startup_defaults = self._handler.handle_response_to_task_defaults_request()
        return task_startup_defaults

    def run(self, **parameters):
        """
        Run or post-process current simulation
        :param parameters: keywords for identify run or post-processor commands
                           "exec" - type of solver or post-processor to be run
                           "stb" - storyboard id for "exec = VBA"
        :return: ID of created Task or None if error occurred
        """
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
            params = self.get_simulation_task_defaults()

        response = self._sender.send_run_request(**params)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        task_id = self._handler.handle_response_to_run_request()
        if task_id:
            return Task(self._app_session, task_id)
        return None


class Task(AbstractEntity):
    """
    Class for representation of the task entity
    """
    def __init__(self, app_session, identifier):
        super().__init__(app_session, identifier)
        self._set_entity_type(EntityTypes.TASK)
        self._setup_attributes()

    def get_status(self):
        response = self._sender.send_task_status_request(self.identifier)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        return self._handler.handle_response_to_task_status_response()


class SubmodelType(AbstractEntity):
    """
    Class for representation of the s|type entity
    """
    def __init__(self, app_session, identifier):
        super().__init__(app_session, identifier)
        self._set_entity_type(EntityTypes.STYPE)
        self._setup_attributes()

    def get_list_of_submodels(self):
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

    def upload_new_submodel(self, *files, **params):
        if "stype" in params.keys():
            stype = SubmodelType(self._app_session, params.get("stype"))
        else:
            stype = SubmodelType(self._app_session, self._app_session.cfg.server_storage)

        if "add_to_clipboard" in params.keys():
            add_to_clipboard = "on" if bool(params.get("add_to_clipboard")) else "off"
        else:
            add_to_clipboard = "off"

        submodels = []
        for file in files:
            response = self._sender.send_upload_submodel_request(file, stype.tree_id, add_to_clipboard)
            Timeout.hold_your_horses()
            self._handler.set_response(response)
            sumbodel_id = self._handler.handle_response_to_upload_submodel_request()
            if sumbodel_id:
                submodels.append(Submodel(self._app_session, sumbodel_id))

        return submodels


class Submodel(AbstractEntity):
    """
    Class for representation of the submodel entity
    """
    def __init__(self, app_session, identifier):
        super().__init__(app_session, identifier)
        self._set_entity_type(EntityTypes.SUBMODEL)
        self._setup_attributes()
