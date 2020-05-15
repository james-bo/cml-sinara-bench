# coding: utf-8
import core.bench.entities
from ui.console import terminal
from core.dao.local_data_manager import JSONDataManager
from core.network.timeout import Timeout


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

        # S|Type to upload submodels
        self.__stype = core.bench.entities.SubmodelType(self.app_session, self.app_session.cfg.server_storage)

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
    def current_simulation(self, current_simulation):
        self.__current_simulation = current_simulation
        self.__bench_id = current_simulation.identifier

    @property
    def current_task(self):
        return self.__current_task

    @current_task.setter
    def current_task(self, current_task):
        self.__current_task = current_task
        self.__task_status = current_task.get_status

    @property
    def status(self):
        return self.__task_status

    @status.setter
    def status(self, status):
        if status == self.__current_task.get_status():
            self.__task_status = status

    @property
    def submodels(self):
        return [self.app_session.cfg.local_storage + "/" + f for f in self.__submodels]

    @property
    def stype(self):
        return self.__stype

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

    WALK_INTERVAL = 60  # 1 minute

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

    @property
    def graph(self):
        return self.__graph

    def execute_all_tasks(self):
        """
        Main method of workflow. Run all simulations in graph vertices.
        :return:
        """

        def status_based_behaviour(vertex):
            """
            Define main loop behaviour while walking through vertex basing on vertex status
            :param vertex: vertex in workflow graph
            :return terminate_loop: magic integer value:
                                    -1: error occurred and main loop shall be stopped
                                     0: current simulation is not done yet, continue
                                     1: current simulation is done
            """
            assert isinstance(vertex, Vertex)
            terminal.show_info_message("Processing vertex with ID: {}".format(vertex.object_id))
            # if status is "New",
            #   - clone base simulation
            #   - upload submodels
            #   - run cloned (current vertex) simulation
            #   - update vertex status from simulation task status
            if vertex.status == "New":
                terminal.show_info_message("Vertex status: {}".format(vertex.status))
                terminal.show_info_message("Vertex base simulation ID: {}".format(vertex.base_simulation.identifier))
                base_simulation = vertex.base_simulation
                terminal.show_info_message("Trying to clone base simulation...")
                current_simulation = base_simulation.clone()
                vertex.current_simulation = current_simulation
                if current_simulation:
                    # if cloned successfully, upload submodels
                    terminal.show_info_message("Cloned simulation ID: {}".format(vertex.current_simulation.identifier))
                    terminal.show_info_message("Uploading submodels for current simulation...")
                    stype = vertex.stype
                    uploaded_submodels = stype.upload_new_submodel(*vertex.submodels)
                    uploaded_submodels_ids = [submodel.identifier for submodel in uploaded_submodels]
                    _ = current_simulation.add_new_sumbodels(uploaded_submodels_ids)
                    terminal.show_info_message("{} submodels added for current simulations".format(
                        len(uploaded_submodels_ids)))
                    # start with default parameters
                    terminal.show_info_message("Trying to run current simulation...")
                    current_task = current_simulation.run()
                    vertex.current_task = current_task
                    if current_task:
                        # if task created successfully, get status
                        terminal.show_info_message("Created task ID: {}".format(vertex.current_task.identifier))
                        vertex.status = current_task.get_status()
                        return 0
                    terminal.show_error_message("Task has not been created.")
                    return -1
                terminal.show_error_message("Simulation has not been cloned.")
                return -1
            # if status is "Finished",
            #   - nothing to do with vertex
            #   - save status; when all vertices will have the same status, loop can be stopped
            elif vertex.status == "Finished":
                terminal.show_info_message("Vertex status: {}".format(vertex.status))
                return 1
            # if status is "Failed",
            #   - terminate main loop
            elif vertex.status == "Failed":
                terminal.show_warning_message("Vertex status: {}".format(vertex.status))
                return -1
            # if status is unknown,
            #   - update vertex status from simulation task status
            else:
                terminal.show_info_message("Updating vertex status...")
                current_task = vertex.current_task
                if current_task:
                    current_status = current_task.get_status()
                    vertex.status = current_status
                terminal.show_info_message("Vertex status: {}".format(vertex.status))
                return 0

        stop_main_loop = False

        # initiate list for saving loop results
        rs = [0 for _ in range(len(self.graph.vertices))]

        # main loop - while all tasks are done or some failure occurred
        while not stop_main_loop:

            # iterate over dictionary of all workflow graph vertices {id -> Vertex}
            for i, v in enumerate(self.graph.vertices.values()):

                # check vertex links
                # if links list is empty, vertex is at root level and it's simulation can be started
                if len(v.links == 0):
                    terminal.show_info_message("Vertex {} has no linked vertices".format(v.object_id))
                    r = status_based_behaviour(v)
                    rs[i] = r
                    if r == -1:
                        terminal.show_error_message("Failed while processing vertex {}".format(v.object_id))
                        stop_main_loop = True
                        break

                # else, if links list is not empty,
                else:
                    terminal.show_info_message("Vertex {} has {} linked vertices".format(v.object_id, len(v.links)))
                    terminal.show_info_message("Checking status of linked vertices...")
                    # check status of all linked vertices
                    if all(l.status == "Finished" for l in v.links):
                        # if all parent vertices successfully finished,
                        # current vertex can run
                        terminal.show_info_message("All linked vertices successfully finished")
                        r = status_based_behaviour(v)
                        rs[i] = r
                        if r == -1:
                            terminal.show_error_message("Failed while processing vertex {}".format(v.object_id))
                            stop_main_loop = True
                            break
                    else:
                        terminal.show_info_message("Some linked vertices is not finished yet...")

            stop_main_loop = all(item == 1 for item in rs) or any(item == -1 for item in rs)
            if not stop_main_loop:
                Timeout.pause(WorkFlow.WALK_INTERVAL)
