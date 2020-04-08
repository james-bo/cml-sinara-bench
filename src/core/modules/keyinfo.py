# coding: utf-8
from core.utils import keyreader
import os
import enum


class KeyFileInformationStatus(enum.Enum):
    NO_CREDENTIALS_ERROR = {"code": -2,
                            "description": "Key file does not exist"}
    READING_ERROR = {"code": -1,
                     "description": "Error during reading key file"}
    SUCCESS = {"code": 0,
               "description": "Valid configuration file"}
    NO_USERNAME_ERROR = {"code": 1,
                         "description": "Configuration file does not contain username"}
    NO_PASSWORD_ERROR = {"code": 2,
                         "description": "Configuration file does not contain password"}


class KeyFileInformation(object):
    def __init__(self, path_to_key_file):
        if os.path.isfile(path_to_key_file):
            self.__info = keyreader.read_credentials_from_file(path_to_key_file)
            self.__file_exists = True
        else:
            self.__info = None
            self.__file_exists = False
        self.__necessary_keys = ["username", "password"]

    @property
    def full_information(self):
        return self.__info

    @property
    def username(self):
        return self.__info.get(self.__necessary_keys[0])

    @property
    def password(self):
        return self.__info.get(self.__necessary_keys[1])

    @property
    def status_code(self):
        return self.__check_key_file_information().value.get("code")

    @property
    def status_description(self):
        return self.__check_key_file_information().value.get("description")

    def __check_key_file_information(self):
        if not self.__file_exists:
            return KeyFileInformationStatus.NO_CREDENTIALS_ERROR
        if not (self.__info and isinstance(self.__info, dict)):
            return KeyFileInformationStatus.READING_ERROR
        if self.__necessary_keys[0] not in self.__info.keys():
            return KeyFileInformationStatus.NO_USERNAME_ERROR
        if self.__necessary_keys[1] not in self.__info.keys():
            return KeyFileInformationStatus.NO_PASSWORD_ERROR
        return KeyFileInformationStatus.SUCCESS
