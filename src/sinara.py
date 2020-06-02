# coding: utf-8
import os
import inspect
from core.modules.cfginfo import ConfigurationInformation
from ui.console import terminal, argparser
import sys
import traceback
from core.main.appsession import AppSession


def main():
    root_path = os.path.abspath(
                    os.path.dirname(
                        inspect.getsourcefile(lambda: 0)))
    terminal.show_info_message("Root directory: {}".format(root_path))

    config_path = os.path.abspath(os.path.join(root_path, "cfg", "config.cfg"))
    config_info = ConfigurationInformation(config_path)

    info = ""
    trace = ""
    code = 0

    credentials_file = None
    arguments = argparser.get_arguments()
    if arguments:
        key = arguments.k
        if key:
            credentials_file = os.path.abspath(os.path.join(root_path, "cfg", "credentials"))

        json = arguments.j
        if json:
            json_file = os.path.abspath(json)
        else:
            raise ValueError("No JSON file selected!")

    # TODO: add -r key for restart
    #       after script run, write `lck` file with current time and host name
    #       after AppSession run, append AppSession UID to `lck` file
    #       if -r key is present, try to read `lck` file, get data from it, compare UIDs

    if config_info.status_code != 0:
        terminal.show_error_message(config_info.status_description)
        sys.exit(config_info.status_code)
    else:
        try:
            app_session = AppSession(cfg=config_info, credentials=credentials_file, json=json_file)
            app_session.execute()
        except Exception as e:
            info = str(e)
            trace = traceback.format_exc()
            code = -100
        else:
            info = "Finished."
            code = 0
        finally:
            print(info)
            if trace:
                print(trace)
            sys.exit(code)


if __name__ == "__main__":
    main()
