# coding: utf-8
import enum
from core.network.timeout import Timeout


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

    def _set_entity_type(self, entity_type):
        if isinstance(entity_type, EntityTypes):
            self._entity_type = entity_type

    def _setup_attributes(self):
        if self.entity_type:
            self._setup_name()
            self._setup_parent_id()
            self._setup_tree_path()

    def _setup_name(self):
        response = self._sender.send_entity_name_request(self.identifier, self.entity_type.value)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        self._name = self._handler.handle_response_to_entity_name_request()

    def _setup_parent_id(self):
        response = self._sender.send_entity_parent_id_request(self.identifier, self.entity_type.value)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        self._parent_id = self._handler.handle_response_to_entity_parent_id_request()

    def _setup_tree_path(self):
        response = self._sender.send_entity_tree_path_request(self.identifier, self.entity_type.value)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        self._tree_path = self._handler.handle_response_to_entity_tree_path_request()


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
        :return: list of task objects, of None if some error occurred during reading tasks
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

    def add_new_sumbodels(self, *files, **params):
        if "stype" in params.keys():
            stype = SubmodelType(self._app_session, params.get("stype"))
        else:
            stype = SubmodelType(self._app_session, self._app_session.cfg.server_storage)

        if "add_to_clipboard" in params.keys():
            add_to_clipboard = "on" if bool(params.get("add_to_clipboard")) else "off"
        else:
            add_to_clipboard = "off"


        return 0


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

    def get_tree_id(self):
        response = self._sender.send_entity_tree_id_request(self.identifier, self.entity_type)
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        return self._handler.handle_response_to_entity_tree_id_request()


class Submodel(AbstractEntity):
    """
    Class for representation of the submodel entity
    """
    def __init__(self, app_session, identifier):
        super().__init__(app_session, identifier)
        self._set_entity_type(EntityTypes.SUBMODEL)
        self._setup_attributes()
