# coding: utf-8
import enum


class EntityTypes(enum.Enum):
    LOADCASE = "loadcase"
    SIMULATION = "simulation"


class AbstractEntity(object):
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
        self._handler.set_response(response)
        self._name = self._handler.handle_response_to_entity_name_request()

    def _setup_parent_id(self):
        response = self._sender.send_entity_parent_id_request(self.identifier, self.entity_type.value)
        self._handler.set_response(response)
        self._parent_id = self._handler.handle_response_to_entity_parent_id_request()

    def _setup_tree_path(self):
        response = self._sender.send_entity_tree_path_request(self.identifier, self.entity_type.value)
        self._handler.set_response(response)
        self._tree_path = self._handler.handle_response_to_entity_tree_path_request()


class Loadcase(AbstractEntity):
    def __init__(self, app_session, identifier):
        super().__init__(app_session, identifier)
        self._set_entity_type(EntityTypes.LOADCASE)
        self._setup_attributes()


class Simulation(AbstractEntity):
    def __init__(self, app_session, identifier):
        super().__init__(app_session, identifier)
        self._set_entity_type(EntityTypes.SIMULATION)
        self._setup_attributes()

    def clone(self):
        response = self._sender.send_clone_simulation_request(self.identifier)
        self._handler.set_response(response)
        return self._handler.handle_response_to_clone_simulation_request()

    def get_parent_loadcase(self):
        return Loadcase(self._app_session, self.parent_id)
