# coding: utf-8
import core.bench.entities
from ui.console import terminal
from core.dao.local_data_manager import LocalDataManager


class CMLBenchManager(object):
    def __init__(self, app_session, search_id):
        self.__app_session = app_session
        self.__search_id = search_id

    @property
    def app_session(self):
        return self.__app_session

    @property
    def search_id(self):
        return self.__search_id

    def search_for_simulation(self):
        terminal.show_info_message("Searching for simulation with ID {}".format(self.search_id))
        simulation = core.bench.entities.Simulation(self.app_session, self.search_id)
        if simulation.name:
            return simulation
        return None

    def clone_simulation(self):
        terminal.show_info_message("Trying to clone simulation with ID {}".format(self.search_id))
        reference_simulation = self.search_for_simulation()
        if reference_simulation:
            cloned_simulation_id = reference_simulation.clone()
            terminal.show_info_message("Cloned simulation ID: {}".format(cloned_simulation_id))
        return terminal.show_error_message("Failed to clone simulation")

    def get_list_of_submodels_to_be_uploaded(self):
        terminal.show_info_message("Trying to get list of sumbodels for simulation with ID {}".format(self.search_id))
        data_manager = LocalDataManager(self.app_session)
        simulation = self.search_for_simulation()
        list_of_sumbodels = data_manager.get_submodels_list_from_database(simulation.get_parent_loadcase().tree_path)
        terminal.show_info_message("List of files to be uploaded: {}".format(str(list_of_sumbodels)))
        return list_of_sumbodels

    def get_list_of_existing_sumbodels(self):
        terminal.show_info_message("Trying to get list of existing submodels of simulation with ID {}".format(
            self.search_id))
        simulation = self.search_for_simulation()
        list_of_submodels = simulation.get_list_of_submodels()
        terminal.show_info_message("List of existing submodels: {}".format(str(list_of_submodels)))
        return list_of_submodels
