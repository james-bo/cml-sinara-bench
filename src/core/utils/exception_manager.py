# coding: utf-8

import traceback
from ui.console import terminal
from core.utils.decorators import method_info


@method_info
def handle_unexpected_exception(exception):
    if isinstance(exception, Exception):
        terminal.show_error_message("Unexpected exception occurred")
        tb = traceback.format_exception(etype=type(exception),
                                        value=exception,
                                        tb=exception.__traceback__)
        terminal.show_trace_message("{}", "".join(tb))
        terminal.show_error_message("Terminating application")


@method_info
def handle_raised_exception(exception):
    if isinstance(exception, Exception):
        terminal.show_error_message("Error occurred")
        tb = traceback.format_exception(etype=type(exception),
                                        value=exception,
                                        tb=None)
        terminal.show_trace_message("{}", "".join(tb))
