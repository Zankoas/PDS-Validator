import os


def get_all_filenames(path):
    for entry in os.listdir(path):
        subpath = path + '\\' + entry
        if os.path.isfile(subpath):
            yield subpath
        elif os.path.isdir(subpath):
            nested_file = get_all_filenames(subpath)
            yield nested_file
