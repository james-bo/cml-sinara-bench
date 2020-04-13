# coding: utf-8


class Sender(object):
    def __init__(self, app_session):
        self.__app_session = app_session
        self.__http_session = self.__app_session.session
        self.__host = self.__app_session.cfg.backend_address

    def send_login_request(self, username, password, remember_me=False):
        url = "{}/rest/login".format(self.__host)
        response = self.__http_session.post(url, data={"username": username,
                                                       "password": password,
                                                       "remember-me": str(remember_me).lower})
        return response

    def _send_entity_base_info_request(self, entity_id, entity_type):
        url = "{}/rest/{}/{}".format(self.__host, entity_type, entity_id)
        response = self.__http_session.get(url)
        return response

    def send_entity_name_request(self, entity_id, entity_type):
        return self._send_entity_base_info_request(entity_id, entity_type)

    def send_entity_parent_id_request(self, entity_id, entity_type):
        return self._send_entity_base_info_request(entity_id, entity_type)

    def send_entity_tree_path_request(self, entity_id, entity_type):
        return self._send_entity_base_info_request(entity_id, entity_type)

    def send_clone_simulation_request(self, entity_id, add_to_clipboard=False, dmu_id=None):
        url = "{}/rest/simulation/{}/clone".format(self.__host, entity_id)
        response = self.__http_session.post(url,
                                            json={"addToClipboard": add_to_clipboard,
                                                  "dmuID": dmu_id})
        return response
