# coding: utf-8
import enum
import os
from core.utils import cfgreader


class ConfigurationInformationStatus(enum.Enum):
    NO_CONFIG_FILE_ERROR = {"code": -2,
                            "description": "Configuration file does not exists"}
    READING_ERROR = {"code": -1,
                     "description": "Error during reading configuration file"}
    SUCCESS = {"code": 0,
               "description": "Valid configuration file"}
    NO_SERVER_URL_ERROR = {"code": 1,
                           "description": "Configuration file does not contain information about server address"}
    NO_LOCAL_STORAGE_ERROR = {"code": 2,
                              "description": "Configuration file does not contain information about local storage"}
    NO_SERVER_STORAGE_ERROR = {"code": 3,
                               "description": "Configuration file does not contain information about server storage"}


class ConfigurationInformation(object):

    def __init__(self, path_to_config_file):
        if os.path.isfile(path_to_config_file):
            self.__info = cfgreader.read_application_config(path_to_config_file)
            self.__file_exists = True
        else:
            self.__info = None
            self.__file_exists = False
        self.__necessary_keys = ["backend address",
                                 "local storage",
                                 "server storage"]

    @property
    def full_information(self):
        return self.__info

    @property
    def backend_address(self):
        return self.__info.get(self.__necessary_keys[0])

    @property
    def local_storage(self):
        return self.__info.get(self.__necessary_keys[1])

    @property
    def server_storage(self):
        return self.__info.get(self.__necessary_keys[2])

    @property
    def status_code(self):
        return self.__check_configuration_information().value.get("code")

    @property
    def status_description(self):
        return self.__check_configuration_information().value.get("description")

    def __check_configuration_information(self):
        if not self.__file_exists:
            return ConfigurationInformationStatus.NO_CONFIG_FILE_ERROR
        if not (self.__info and isinstance(self.__info, dict)):
            return ConfigurationInformationStatus.READING_ERROR
        if self.__necessary_keys[0] not in self.__info.keys():
            return ConfigurationInformationStatus.NO_SERVER_URL_ERROR
        if self.__necessary_keys[1] not in self.__info.keys():
            return ConfigurationInformationStatus.NO_LOCAL_STORAGE_ERROR
        if self.__necessary_keys[2] not in self.__info.keys():
            return ConfigurationInformationStatus.NO_SERVER_STORAGE_ERROR
        return ConfigurationInformationStatus.SUCCESS
