# coding: utf-8


def read_application_config(cfg_name):
    """
    Method reads application configuration file
    :param cfg_name: Path to file
    :return: Dictionary with pairs key-value
    """
    info = {}
    with open(cfg_name, mode='r') as cfg:
        line = cfg.readline()
        current_line_number = 1
        while line:
            if line.strip()[0] != '#':
                if line.count(':') < 1:
                    raise ValueError("Improperly formatted configuration file. Missing separator in line {}."
                                     .format(current_line_number))
                else:
                    key = line.split(':')[0].strip().lower()
                    value = ':'.join([s.strip().lower() for s in line.split(':')[1:]])
                    info[key] = value
            line = cfg.readline()
            current_line_number += 1
    return info
