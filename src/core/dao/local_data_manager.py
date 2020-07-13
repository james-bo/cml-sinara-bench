# coding: utf-8
import json
import core.modules.workflow


class JSONDataManager(object):
    """
    Getting information form JSON input file
    """
    def __init__(self, json_file):
        self.__json = json_file

    def get_behaviour(self):
        """
        Method returns a string representing desired behaviour
        :return: Type of behaviour, according to JSON file
                - `Solve` -- build workflow graph and run all tasks
                - `Update targets` -- only create|update target values, do not run any task
        """
        with open(self.__json, mode='r') as jf:
            data = json.load(jf)
        root = data.get("Root")
        if root:
            beh = root.get("Behaviour")
            if beh:
                return beh
        return None

    def get_json_data(self):
        """
        Method returns a dictionary containing structured input data information
        {object_id: {object}}
        :return: dictionary if success or None otherwise
        """
        res = {}
        with open(self.__json, mode='r') as jf:
            data = json.load(jf)
        root = data.get("Root")
        if root:
            lcs = root.get("LCs")
            if lcs:
                assert isinstance(lcs, list)
                for item in lcs:
                    assert isinstance(item, dict)
                    key = item.get(core.modules.workflow.JSONProps.VERTEX_ID.value)
                    val = item
                    res[key] = val
                return res
        return None

    @staticmethod
    def dump_data(data, file):
        """
        Writes specified data into .json file
        :param data: data to be serialized
        :param file: path to file
        :return:
        """
        with open(file, mode="w") as f:
            json.dump(data, f, indent=4)
