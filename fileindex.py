import os

import filemeta
from client_default import defaultpath


def walk_files(list_files, list_folders, directory):
    for name in os.listdir(directory):
        path = os.path.join(directory, name).replace('\\', '/')
        if os.path.isfile(path):
            list_files.append(path)
        if os.path.isdir(path):
            list_folders.append(path)
            walk_files(list_files, list_folders, path)


def get_index(directory=defaultpath):
    meta_data_dict = dict()
    list_files = []
    list_folders = []
    walk_files(list_files, list_folders, directory)
    for filename in list_files:
        meta_data_dict.setdefault(filename, filemeta.filemeta(filename))
    return meta_data_dict, list_folders
