# coding: utf-8
import os
import inspect
from core.modules.cfginfo import ConfigurationInformation
from ui.console import terminal, argparser
import sys
from core.main.appsession import AppSession
from core.utils.exception_manager import handle_unexpected_exception


def main():
    root_path = os.path.abspath(
                    os.path.dirname(
                        inspect.getsourcefile(lambda: 0)))
    terminal.show_info_message("Root directory : {}".format(root_path))

    config_path = os.path.abspath(os.path.join(root_path, "cfg", "config.cfg"))
    config_info = ConfigurationInformation(config_path)
    terminal.show_info_message(f"Backend address: {config_info.backend_address}")
    terminal.show_info_message(f"Local storage  : {config_info.local_storage}")
    terminal.show_info_message(f"Server storage : {config_info.server_storage}")

    code = 0

    credentials_file = None
    json_file = None
    save_results = False
    arguments = argparser.get_arguments()
    if arguments:
        key = arguments.k
        if key:
            credentials_file = os.path.abspath(os.path.join(root_path, "cfg", "credentials"))

        json = arguments.j
        if json:
            json_file = os.path.abspath(json)
        else:
            terminal.show_error_message("No JSON file selected!")
            sys.exit(1)

        values_dir = arguments.v
        if values_dir:
            save_results = os.path.abspath(values_dir)
        else:
            save_results = None

        add_dsp = arguments.d
        if add_dsp:
            terminal.Output.set_type(2)

    # TODO: add -r key for restart
    #       after script run, write `lck` file with current time and host name
    #       after AppSession run, append AppSession UID to `lck` file
    #       if -r key is present, try to read `lck` file, get data from it, compare UIDs

    if config_info.status_code != 0:
        terminal.show_error_message(config_info.status_description)
        return config_info.status_code
    else:
        try:
            app_session = AppSession(root=root_path,
                                     cfg=config_info,
                                     credentials=credentials_file,
                                     json=json_file,
                                     res=save_results)
            app_session.execute()
        except Exception as e:
            handle_unexpected_exception(e)
            return -666

    return 0


def terminate(code):
    if code == 0:
        terminal.show_info_message("Success")
    else:
        terminal.show_error_message("Failed with code {}", code)
    sys.exit(code)


if __name__ == "__main__":
    status = main()
    terminate(status)
