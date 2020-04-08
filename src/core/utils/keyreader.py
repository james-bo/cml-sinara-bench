# coding: utf-8


def read_credentials_from_file(key_file):
    info = {}
    with open(key_file, mode='r') as kf:
        line = kf.readline()
        current_line_number = 1
        while line:
            if line.strip()[0] != '#':
                if line.count(':') < 1:
                    raise ValueError("Improperly formatted credentials file. Missing separator in line {}."
                                     .format(current_line_number))
                else:
                    key = line.split(':')[0].strip()
                    value = ':'.join([s.strip() for s in line.split(':')[1:]])
                    info[key] = value
            line = kf.readline()
            current_line_number += 1
    return info
