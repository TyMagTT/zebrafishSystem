import json
from os.path import splitext


def open_file(path):
    extension = splitext(path)[1]
    if extension != '.json':
        raise ValueError
    with open(path) as file_handle:
        setting_list = json.load(file_handle)
    return setting_list
