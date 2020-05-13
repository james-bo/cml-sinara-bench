# coding: utf-8
import core.bench.entities
from ui.console import terminal
from core.dao.local_data_manager import JSONDataManager


class Vertex(object):
    def __init__(self, app_session, data):
        self.__app_session = app_session
        assert isinstance(data, dict)

        # Vertex ID = Object ID in JSON file
        self.__object_id = data.get("object_id")

        # Current Simulation ID in CML-Bench
        self.__bench_id = data.get("bench_id")
        if self.__bench_id:
            self.__current_simulation = core.bench.entities.Simulation(self.app_session, self.__bench_id)
        else:
            self.__current_simulation = None

        # Base (Reference) Simulation ID in CML-Bench
        self.__base_simulation_id = data.get("base_simulation_id")
        if self.__base_simulation_id:
            self.__base_simulation = core.bench.entities.Simulation(self.app_session, self.__base_simulation_id)
        else:
            terminal.show_error_message("Base simulation is not defined")
            self.__base_simulation = None

        # Current Task ID in CML-Bench
        self.__task_id = data.get("task_id")
        if self.__task_id:
            self.__current_task = core.bench.entities.Task(self.app_session, self.__task_id)
            if self.__current_task not in self.__current_simulation.get_list_of_tasks():
                terminal.show_error_message("Defined task does not belong to defined simulation")
        else:
            self.__current_task = None

        # Current Task status in CML-Bench
        self.__task_status = data.get("task_status")
        if self.__current_task or self.__task_status != "New":
            if self.__task_status != self.__current_task.get_status():
                terminal.show_error_message("Defined status does not match existing task status")

        # Deprecated field
        self.__trimmed_path = data.get("trimmed_path")

        # List of submodel files for current simulation
        self.__submodels = data.get("submodels")

        # List of results file for current simulation
        self.__results = data.get("results")

        # List of parent vertices IDs (which status must be 'ok' for starting current simulation)
        self.__parent_objects_ids = data.get("parents")

        # Deprecated field
        self.__children_object_ids = data.get("children")

        # List of parent vertices (objects)
        self.__links = []

    @property
    def app_session(self):
        return self.__app_session

    @property
    def object_id(self):
        return self.__object_id

    @property
    def parents_ids(self):
        return self.__parent_objects_ids

    @property
    def links(self):
        """
        zwo, drei, vier
        """
        return self.__links

    @property
    def base_simulation(self):
        return self.__base_simulation

    @property
    def current_simulation(self):
        return self.__current_simulation

    @current_simulation.setter
    def current_simulation(self, current_simulation_id):
        self.__current_simulation = core.bench.entities.Simulation(self.app_session, current_simulation_id)
        self.__bench_id = current_simulation_id

    def __repr__(self):
        self_id = self.object_id
        base_id = self.base_simulation.identifier if self.base_simulation else "-"
        curr_id = self.current_simulation.identifier if self.current_simulation else "-"
        return "\nVertex ID               : {}\nBase simulation         : {}\nCurrent simulation      : {}".format(
            self_id, base_id, curr_id
        )

    def add_link(self, vertex):
        assert isinstance(vertex, Vertex)
        self.__links.append(vertex)


class Graph(object):
    def __init__(self, app_session):
        """
        Python graph implementation:
        https://www.python-course.eu/graphs_python.php
        https://medium.com/youstart-labs/implement-graphs-in-python-like-a-pro-63bc220b45a0
        https://runestone.academy/runestone/books/published/pythonds/Graphs/Implementation.html
        https://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python

        Vertices of the workflow graph: objects containing simulations
        Dictionary container: vertex_id -> Vertex object
        Edges of the workflow graph: links from each simulation to its parents, which are needed to start current
        simulation
        List container: [(vertex_from, vertex_to), ...]
        """
        self.__app_session = app_session
        self.__vertices = {}
        self.__edges = []

    @property
    def app_session(self):
        return self.__app_session

    @property
    def vertices(self):
        return self.__vertices

    @property
    def edges(self):
        return self.__edges

    def add_vertex(self, data):
        """
        Method adds vertices one by one from given data
        :param data: dictionary of input objects
        :return:
        """
        assert isinstance(data, dict)
        vertex = Vertex(self.app_session, data)
        key = data.get("object_id")
        self.__vertices[key] = vertex

    def build_graph_edges(self):
        """
        Methods adds links between vertices based on vertex data
        :return:
        """
        for vertex in self.vertices.values():
            for parent_id in vertex.parents_ids:
                parent_vertex = self.vertices.get(parent_id)
                if parent_vertex:
                    self.__edges.append((vertex, parent_vertex))
                    vertex.add_link(parent_vertex)


class WorkFlow(object):

    __instance = None

    @classmethod
    def get_instance(cls, *args):
        if not cls.__instance:
            cls.__instance = WorkFlow(*args)
        return cls.__instance

    def __init__(self, app_session):
        if not WorkFlow.__instance:

            terminal.show_info_message("Workflow initialization...")
            self.__app_session = app_session
            self.__graph = Graph(self.app_session)
            self.__json_data_manager = JSONDataManager(self.app_session)
            self.__json_data = self.__json_data_manager.get_json_data()

            terminal.show_info_message("Application session: {}".format(self.app_session.sid))

            for data in self.__json_data.values():
                self.__graph.add_vertex(data)

            terminal.show_info_message("Workflow graph vertices: {}".format(self.__graph.vertices.values()))

            self.__graph.build_graph_edges()

            terminal.show_info_message("Workflow graph edges: {}".format(self.__graph.edges))

        else:

            terminal.show_info_message("Workflow already exists.")
            # FIXME lovely piece of code. Establish access to instance variables
            _ = self.get_instance(app_session)

    @property
    def app_session(self):
        return self.__app_session

    def execute_all_tasks(self):
        pass
        # loop while status not ok or not failed
        # for every vertex
        # clone simulation
        # run cloned simulation
        # if task status not ok - fail with error
