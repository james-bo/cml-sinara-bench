# coding: utf-8
from core.network.timeout import Timeout


class Healthcheck(object):
    def __init__(self, app_session):
        self._app_session = app_session
        self._sender = self._app_session.sender
        self._handler = self._app_session.handler

    def get_status(self):
        response = self._sender.send_healthcheck_request()
        Timeout.hold_your_horses()
        self._handler.set_response(response)
        state = self._handler.handle_response_to_healthcheck_request()
        return state
