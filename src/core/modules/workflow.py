# coding: utf-8
import os
import enum
import core.bench.entities
from ui.console import terminal
from core.dao.local_data_manager import JSONDataManager
from core.network.timeout import Timeout
from core.utils.decorators import method_info

# ----------------------------------------------- Supported JSON Types ----------------------------------------------- #


class JSONTypes(enum.Enum):
    SOLVE = "Solve"
    UPDATE_TARGETS = "Update targets"
    VALUES = "Values"


# -------------------------------------------- Supported JSON Properties --------------------------------------------- #


class JSONProps(enum.Enum):
    # TODO: change name of property "bench_id" to "curr_simulation_id"
    #       change name of property "object_id" to "vertex_id"
    #       change name of property "task_id" to "curr_task_id"
    #       change name of property "task_status" to "curr_task_status"
    #       change name of property "storyboard" to "storyboard_id"
    #       change name of property "current_values" to "values"
    #       add property "loadcase_id"

    VERTEX_ID = "vertex_id"
    # VERTEX_ID = "object_id"
    LOADCASE_ID = "loadcase_id"
    BASE_SIMULATION_ID = "base_simulation_id"
    CURR_SIMULATION_ID = "curr_simulation_id"
    # CURR_SIMULATION_ID = "bench_id"
    CURR_TASK_ID = "curr_task_id"
    # CURR_TASK_ID = "task_id"
    VERTEX_STATUS = "curr_task_status"
    # VERTEX_STATUS = "task_status"
    SOLVER = "solver"
    STORYBOARD = "storyboard_id"
    # STORYBOARD = "storyboard"
    SUBMODELS = "submodels"
    RESULTS = "results"
    PARENTS = "parents"
    TARGETS = "targets"
    VALUES = "values"
    # VALUES = "current_values"

# --------------------------------------------------- Graph Vertex --------------------------------------------------- #


class Vertex(object):
    def __init__(self, app_session, data):
        self.__app_session = app_session
        assert isinstance(data, dict)

        # ----------------------------- All possible parameters written in graph vertex ------------------------------ #

        # • Vertex ID (`object_id` in JSON)
        self.__vertex_id = None

        # • Base (Reference) simulation (`bases_simulation_id` is its identifier)
        self.__base_simulation = None

        # • Current simulation (`bench_id` is current simulation identifier)
        self.__current_simulation = None

        # • Current task (`task_id` in JSON)
        self.__current_task = None

        # • Vertex status
        self.__vertex_status = None

        # • Non-default solver for current task
        self.__solver = None

        # • Non-default storyboard for current task
        self.__storyboard = None

        # • Submodels of current simulation (names of files in local storage)
        self.__submodels = None

        # • Result files of current simulation (for downloading; names of files in server storage)
        self.__results = None

        # • Parent vertices IDs (that must be successfully finished before starting the current one)
        self.__parents = None

        # • Parent vertices (as objects)
        self.__links = []

        # • Targets of current loadcase (defined as parent of base simulation)
        self.__targets = None

        # • Key results of current simulation
        self.__values = None

        # • S|Type for current loadcase (basically defied in configuration file)
        self.__stype = core.bench.entities.SubmodelType(self.app_session, self.app_session.cfg.server_storage)

        # ------------------------------------ Fill fields with values from JSON ------------------------------------- #
        if JSONProps.VERTEX_ID.value in data.keys():
            self.__vertex_id = data.get(JSONProps.VERTEX_ID.value)

        if JSONProps.BASE_SIMULATION_ID.value in data.keys():
            base_sim_id = data.get(JSONProps.BASE_SIMULATION_ID.value)
            if base_sim_id is not None:
                self.__base_simulation = core.bench.entities.Simulation(self.app_session, base_sim_id)
            else:
                terminal.show_error_message("Base (Reference) simulation is not defined in JSON file")

        if JSONProps.CURR_SIMULATION_ID.value in data.keys():
            curr_sim_id = data.get(JSONProps.CURR_SIMULATION_ID.value)
            if curr_sim_id is not None:
                self.__current_simulation = core.bench.entities.Simulation(self.app_session, curr_sim_id)

        if JSONProps.CURR_TASK_ID.value in data.keys():
            curr_task_id = data.get(JSONProps.CURR_TASK_ID.value)
            if curr_task_id is not None:
                self.__current_task = core.bench.entities.Task(self.app_session, curr_task_id)
                if self.__current_task not in self.__current_simulation.get_tasks():
                    terminal.show_error_message("Defined task does not belong to defined simulation")

        if JSONProps.VERTEX_STATUS.value in data.keys():
            vertex_status = data.get(JSONProps.VERTEX_STATUS.value)
            if vertex_status is not None:
                self.__vertex_status = vertex_status
                if vertex_status != "New" and self.__current_task.get_status() != vertex_status:
                    terminal.show_error_message("Defined status does not match existing task status")

        if JSONProps.SOLVER.value in data.keys():
            task_solver = data.get(JSONProps.SOLVER.value)
            if task_solver is not None:
                self.__solver = task_solver

        if JSONProps.STORYBOARD.value in data.keys():
            task_stb = data.get(JSONProps.STORYBOARD.value)
            if task_stb is not None:
                self.__storyboard = task_stb

        if JSONProps.SUBMODELS.value in data.keys():
            curr_sim_subs = data.get(JSONProps.SUBMODELS.value)
            if curr_sim_subs is not None:
                self.__submodels = curr_sim_subs

        if JSONProps.RESULTS.value in data.keys():
            curr_sim_res = data.get(JSONProps.RESULTS.value)
            if curr_sim_res is not None:
                self.__results = curr_sim_res

        if JSONProps.PARENTS.value in data.keys():
            vertex_parents_ids = data.get(JSONProps.PARENTS.value)
            if vertex_parents_ids is not None:
                self.__parents = vertex_parents_ids

        if JSONProps.TARGETS.value in data.keys():
            curr_sim_targets = data.get(JSONProps.TARGETS.value)
            if curr_sim_targets is not None:
                self.__targets = curr_sim_targets

        if JSONProps.VALUES.value in data.keys():
            curr_sim_values = data.get(JSONProps.VALUES.value)
            if curr_sim_values is not None:
                self.__values = curr_sim_values

    # ---------------------------------------------- Vertex Properties ----------------------------------------------- #

    @property
    def app_session(self):
        """
        :return: Current application session, for usage of configuration, sender, handler and create entities
        """
        return self.__app_session

    @property
    def identifier(self):
        """
        :return: Vertex ID
        """
        return self.__vertex_id

    @property
    def base_simulation(self):
        """
        :return: Base (Reference) simulation object
        """
        return self.__base_simulation

    @property
    def current_simulation(self):
        """
        :return: Current simulation object
        """
        return self.__current_simulation

    @current_simulation.setter
    def current_simulation(self, current_simulation):
        """
        Current simulation setter
        :param current_simulation: Current simulation object
        """
        assert isinstance(current_simulation, core.bench.entities.Simulation)
        self.__current_simulation = current_simulation

    @property
    def current_task(self):
        """
        :return: Current task object
        """
        return self.__current_task

    @current_task.setter
    def current_task(self, current_task):
        """
        Current task setter. Changes vertex status
        :param current_task: Current task object
        """
        assert isinstance(current_task, core.bench.entities.Task)
        self.__current_task = current_task
        self.__vertex_status = current_task.get_status

    @property
    def status(self):
        """
        :return: Vertex status (for most cases equal to current task status)
        """
        return self.__vertex_status

    @status.setter
    def status(self, status):
        """
        Vertex status setter. Checks equality to current task status
        :param status: Vertex status
        """
        if status == self.__current_task.get_status():
            self.__vertex_status = status

    @property
    def solver(self):
        """
        :return: Current task solver
        """
        return self.__solver

    @property
    def storyboard(self):
        """
        :return: Current task storyboard
        """
        return self.__storyboard

    @property
    def submodels(self):
        """
        :return: List of full paths to submodels files in local storage
        """
        return [self.app_session.cfg.local_storage + "/" + f for f in self.__submodels]

    @property
    def results(self):
        """
        :return: List of results files of current simulation
        """
        return self.__results

    @property
    def parents(self):
        """
        :return: List of parent vertices IDs
        """
        return self.__parents

    @property
    def links(self):
        """
        Links zwo, drei, vier
        :return: List of parent vertices objects
        """
        return self.__links

    @property
    def targets(self):
        """
        :return: List of current simulation targets.
                 List elements are dictionaries with keys:
                 - `name`
                 - `value`
                 - `condition`
                 - `dimension`
                 - `tolerance`
                 - `description`
        """
        return self.__targets

    @property
    def values(self):
        """
        :return: List of current simulation values.
                 List elements are dictionaries with keys:
                 - `name`
                 - `value`
                 - `dimension`
                 - `description`
        """
        return self.__values

    @property
    def stype(self):
        """
        :return: S|Type object
        """
        return self.__stype

    # ------------------------------------------------ Vertex Methods ------------------------------------------------ #

    def __repr__(self):
        self_id = self.identifier
        base_id = self.base_simulation.identifier if self.base_simulation else "-"
        curr_id = self.current_simulation.identifier if self.current_simulation else "-"
        return "\nVertex ID               : {}\nBase simulation         : {}\nCurrent simulation      : {}".format(
            self_id, base_id, curr_id
        )

    def add_link(self, vertex):
        assert isinstance(vertex, Vertex)
        self.__links.append(vertex)

# -------------------------------------------------- Workflow Graph -------------------------------------------------- #


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
        key = data.get(JSONProps.VERTEX_ID.value)
        self.__vertices[key] = vertex

    def build_graph_edges(self):
        """
        Methods adds links between vertices based on vertex data
        :return:
        """
        for vertex in self.vertices.values():
            for parent_id in vertex.parents:
                parent_vertex = self.vertices.get(parent_id)
                if parent_vertex:
                    self.__edges.append((vertex, parent_vertex))
                    vertex.add_link(parent_vertex)

# ----------------------------------------------------- Workflow ----------------------------------------------------- #


class WorkFlow(object):

    WALK_INTERVAL = 10  # 10 seconds

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
            self.__json_data_manager = JSONDataManager(self.app_session.json)
            self.__json_behaviour = self.__json_data_manager.get_behaviour()
            self.__json_data = self.__json_data_manager.get_json_data()

            terminal.show_info_message("Application session: {}".format(self.app_session.sid))

            # TODO:
            #   Different logic which depends on JSON `Behaviour` field
            #   - If `Behaviour` = `Solve`,
            #     build workflow graph (add vertices, build edges),
            #     `execute_all_tasks()` method can be called
            #   - If `Behaviour` = `Update targets`,
            #     only add vertices, determine CML-Bench loadcase from `bench_id` or `base_simulation_id`,
            #     create or update (?) loadcase targets
            #   - If `Behaviour` = `Dump`,
            #     whole application must be run with `-r` key
            #   - If `Behaviour` = `Values`,
            #     JSON cannot be passed as input file

            if self.__json_behaviour == JSONTypes.SOLVE.value:
                terminal.show_info_message("JSON behaviour: Solving. Building workflow graph...")
                for data in self.__json_data.values():
                    self.__graph.add_vertex(data)

                s = ""
                vals = []
                for v in self.graph.vertices.values():
                    s += terminal.get_blank() + "{}\n"
                    vals.append(v)
                terminal.show_info_message("Workflow graph vertices:\n" + s, *vals)
                # terminal.show_info_objects("Workflow graph vertices: ", list(self.graph.vertices.values()))

                self.__graph.build_graph_edges()

                s = ""
                vals = []
                for v in self.graph.edges:
                    s += terminal.get_blank() + "{}\n"
                    vals.append(v)
                terminal.show_info_message("Workflow graph edges:\n" + s, *vals)
                # terminal.show_info_objects("Workflow graph edges: ", list(self.graph.edges))

            elif self.__json_behaviour == JSONTypes.UPDATE_TARGETS.value:
                terminal.show_info_message("JSON behaviour: Update targets.")
                for data in self.__json_data.values():
                    self.__graph.add_vertex(data)

            else:
                raise TypeError("Unsupported JSON behaviour")

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

    @property
    def json_type(self):
        return self.__json_behaviour

    @method_info
    def process_json(self):
        """
        Processing input JSON file
        :return:
        """
        if self.json_type == JSONTypes.SOLVE.value:
            self._run_all_tasks()
            if self.app_session.results_path is not None:
                # try to create directory
                dir_path = os.path.abspath(self.app_session.results_path)
                terminal.show_info_message(f"Trying to save key results to: {dir_path}")
                try:
                    os.makedirs(dir_path)
                except FileExistsError:
                    terminal.show_warning_message("Folder already exists")
                # collect values
                terminal.show_info_message("Collecting results...")
                data = self._collect_values()
                # save data
                terminal.show_info_message("Saving results...")
                file = os.path.join(dir_path, "Results.json")
                JSONDataManager.dump_data(data, file)
        elif self.json_type == JSONTypes.UPDATE_TARGETS.value:
            self._change_targets()
        else:
            terminal.show_warning_message(f"Cannot process JSON with behaviour: {self.json_type}")

    @method_info
    def _run_all_tasks(self):
        """
        Processing input JSON with behaviour `Solve`
        Run all simulations in graph vertices.
        :return:
        """

        if self.json_type != JSONTypes.SOLVE.value:
            raise ValueError("Method `run_all_tasks()` can not be called for JSON of type `{}`".format(self.json_type))

        @method_info
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
            terminal.show_info_message(f"Processing vertex with ID: {vertex.identifier}")

            # if status is "New",
            #   - clone base simulation
            #   - upload submodels
            #   - run cloned (current vertex) simulation
            #   - update vertex status from simulation task status
            if vertex.status == "New":
                terminal.show_info_message(f"Vertex status: {vertex.status}")
                terminal.show_info_message(f"Vertex base simulation ID: {vertex.base_simulation.identifier}")
                base_simulation = vertex.base_simulation
                terminal.show_info_message("Trying to clone base simulation...")
                current_simulation = base_simulation.clone()
                vertex.current_simulation = current_simulation
                if current_simulation:
                    # if cloned successfully, upload submodels
                    terminal.show_info_message("Cloned simulation ID: {}", vertex.current_simulation.identifier)
                    terminal.show_info_message("Uploading submodels for current simulation...")
                    stype = vertex.stype
                    uploaded_submodels = stype.upload_submodel(*vertex.submodels)
                    # uploaded_submodels_ids = [submodel.identifier for submodel in uploaded_submodels]
                    terminal.show_info_message("Erasing current (cloned) simulation submodels...")
                    status = current_simulation.erase_submodels()
                    if status:
                        terminal.show_info_message("Done")
                    else:
                        terminal.show_error_message("Failed")
                    _ = current_simulation.add_submodels(*uploaded_submodels)
                    terminal.show_info_message("{} submodels added for current simulations", len(uploaded_submodels))
                    # start with default parameters
                    terminal.show_info_message("Trying to run current simulation...")
                    # obtain default parameters to run tasks from base simulation
                    current_task = current_simulation.run(bsi=base_simulation.identifier)
                    vertex.current_task = current_task
                    if current_task:
                        # if task created successfully, get status
                        terminal.show_info_message(f"Created task ID: {vertex.current_task.identifier}")
                        vertex.status = current_task.get_status()
                        return 0
                    terminal.show_error_message("Task has not been created.")
                    return -1
                terminal.show_error_message("Simulation has not been cloned.")
                return -1

            # if status is "Finished",
            #   - download vertex results
            #   - save status; when all vertices will have the same status, loop can be stopped
            elif vertex.status == "Finished":
                terminal.show_info_message("Vertex status: {}", vertex.status)
                if len(vertex.results) == 0:
                    terminal.show_info_message("No results selected for download")
                else:
                    terminal.show_info_message("Downloading results...")
                    current_simulation = vertex.current_simulation
                    lst = current_simulation.download_files(*vertex.results)
                    terminal.show_info_message("Successfully downloaded {} files", len(lst))
                return 1

            # if status is "Failed",
            #   - terminate main loop
            elif vertex.status in ["Failed", "failed", "Error", "error"]:
                terminal.show_warning_message("Vertex status: {}", vertex.status)
                return -1

            # if status is unknown,
            #   - update vertex status from simulation task status
            else:
                terminal.show_info_message("Updating vertex status...")
                current_task = vertex.current_task
                if current_task:
                    current_status = current_task.get_status()
                    vertex.status = current_status
                    task_end_waiting, task_end_solving = current_task.get_time_estimation()
                    terminal.show_info_message("Current task estimated end waiting time: {}", task_end_waiting)
                    terminal.show_info_message("Current task estimated end solving time: {}", task_end_solving)
                terminal.show_info_message("Vertex status: {}", vertex.status)
                return 0

        # --- main section --- main section --- main section --- main section --- main section --- main section ---
        stop_main_loop = False

        # list of graph vertices to iterate over it with possibility to modify it
        vertices = list(self.graph.vertices.values())
        assert all(isinstance(v, Vertex) for v in vertices)

        # initialize dictionary for saving loop results
        rs = {key: 0 for key in [v.identifier for v in vertices]}

        # terminal.show_info_dict("Initial state of results storage", rs)

        s = ""
        vals = []
        for k, v in rs.items():
            s += terminal.get_blank() + "{} → {}\n"
            vals.append(k)
            vals.append(v)

        terminal.show_info_message("Initial state of results storage:\n" + s, *vals)

        # main loop - while all tasks are done or some failure occurred
        while not stop_main_loop:

            # iterate over all workflow graph vertices
            # remove vertices wish status = "Finished"
            # modify original list, no list copies, only one pass: traditional solution is to iterate backwards
            for i in reversed(range(len(vertices))):
                v = vertices[i]

                # check vertex links
                # if links list is empty, vertex is at root level and it's simulation can be started
                if len(v.links) == 0:
                    terminal.show_info_message("Vertex {} has no linked vertices", v.identifier)
                    r = status_based_behaviour(v)
                    terminal.show_info_message("Current vertex result status: {}", r)
                    rs[v.identifier] = r
                    # terminal.show_info_message(f"Current state of the list of vertices results status: {str(rs)}")
                    if r == -1:
                        terminal.show_error_message("Failed while processing vertex {}", v.identifier)
                        # stop_main_loop = True
                        break
                    if r == 1:
                        terminal.show_info_message("Vertex {} is done", v.identifier)
                        del vertices[i]

                # else, if links list is not empty,
                else:
                    terminal.show_info_message("Vertex {} has {} linked vertices", v.identifier, len(v.links))
                    terminal.show_info_message("Checking status of linked vertices...")

                    # check status of all linked vertices
                    if all(l.status == "Finished" for l in v.links):
                        # if all parent vertices successfully finished,
                        # current vertex can run
                        terminal.show_info_message("All linked vertices successfully finished")
                        r = status_based_behaviour(v)
                        terminal.show_info_message("Current vertex result status: {}", r)
                        rs[v.identifier] = r
                        # terminal.show_info_message(f"Current state of the list of vertices results status: {str(rs)}")
                        if r == -1:
                            terminal.show_error_message("Failed while processing vertex {}", v.identifier)
                            # stop_main_loop = True
                            break
                        if r == 1:
                            terminal.show_info_message("Vertex {} is done", v.identifier)
                            del vertices[i]
                    else:
                        terminal.show_info_message("Some linked vertices is not finished yet...")

            stop_main_loop = all(item == 1 for item in rs.values()) or any(item == -1 for item in rs.values())

            # terminal.show_info_message(f"List of vertices results status: {str(rs)}")
            # terminal.show_info_dict("Current state of results storage", rs)

            s = ""
            vals = []
            for k, v in rs.items():
                s += terminal.get_blank() + "{} → {}\n"
                vals.append(k)
                vals.append(v)

            terminal.show_info_message("Initial state of results storage:\n" + s, *vals)

            if not stop_main_loop:
                terminal.show_info_message(f"Waiting for the next loop ... [{WorkFlow.WALK_INTERVAL} sec]")
                Timeout.pause(WorkFlow.WALK_INTERVAL)
            else:
                terminal.show_info_message("Terminating main loop ...")

    @method_info
    def _change_targets(self):
        """
        Processing input JSON with behaviour `Update targets`
        Send requests to add new targets
        :return:
        """

        if self.json_type != JSONTypes.UPDATE_TARGETS.value:
            raise ValueError("Method `change_targets()` can not be called for JSON of type `{}`".format(self.json_type))

        # Walk over each vertices
        # Vertex contains information about base simulation
        # Obtain Loadcase ID from base simulation
        # Add new targets to this loadcase
        vertices = list(self.graph.vertices.values())
        assert all(isinstance(v, Vertex) for v in vertices)

        for v in vertices:
            base_simulation = v.base_simulation
            parent_loadcase = base_simulation.get_loadcase()
            targets = v.targets
            for t in targets:
                ans = parent_loadcase.add_target(t.get("name"),
                                                 t.get("value"),
                                                 t.get("condition"),
                                                 t.get("dimension"),
                                                 t.get("tolerance"),
                                                 t.get("description"))
                if ans is not None:
                    terminal.show_info_message("Successfully added target {} to loadcase {}".format(
                        ans.identifier,
                        parent_loadcase.identifier
                    ))
                else:
                    terminal.show_error_message("Failed to add target to loadcase {}".format(
                        parent_loadcase.identifier
                    ))

    @method_info
    def _collect_values(self):
        """
        Collect all available key results from all current simulations
        Vertex status must be `Finished`
        :return: dictionary with input JSON-like internal structure
        """
        output_data = {"Root": {"Behaviour": JSONTypes.VALUES.value,
                                "LCs": []}}

        vertices = list(self.graph.vertices.values())
        assert all(isinstance(v, Vertex) for v in vertices)

        for v in vertices:
            if v.status != "Finished":
                terminal.show_error_message(f"Vertex {v.identifier} status is not \"Finished\"," +
                                            f"could not collect key results")
                continue

            values = v.current_simulation.get_values()
            current_values = [{"name": val.name,
                               "value": val.value,
                               "dimension": val.dimension,
                               "description": val.description} for val in values]

            output_data["Root"]["LCs"].append({JSONProps.VERTEX_ID.value: v.identifier,
                                               JSONProps.LOADCASE_ID.value: v.base_simulation.get_loadcase().identifier,
                                               JSONProps.VALUES.value: current_values})
        return output_data

    def _create_dump(self):
        pass
