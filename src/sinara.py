# coding: utf-8
from os.path import abspath, dirname, join
from inspect import getsourcefile
from core.modules import cfginfo
from ui.console import terminal
from sys import exit
import traceback
from core.main.appsession import AppSession


def main():
    config_path = abspath(join(abspath(dirname(getsourcefile(lambda: 0))), "config.cfg"))
    config_info = cfginfo.ConfigurationInformation(config_path)

    info = ""
    trace = ""
    code = 0

    if config_info.status_code != 0:
        terminal.show_error_message(config_info.status_description)
        exit(config_info.status_code)
    else:
        try:
            appsession = AppSession(cfg=config_info)
            appsession.execute()
        except Exception as e:
            info = str(e)
            trace = traceback.format_exc()
            code = -100
        else:
            info = "Correct termination"
            code = 0
        finally:
            print(info)
            if trace:
                print(trace)
            exit(code)


if __name__ == "__main__":
    main()
