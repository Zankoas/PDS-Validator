import os


def get_all_filenames(path):
    filenames = []
    for entry in os.listdir(path):
        subpath = path + '\\' + entry
        if os.path.isfile(subpath):
            filenames += [subpath]
        elif os.path.isdir(subpath):
            nested_files = get_all_filenames(subpath)
            filenames += nested_files
    return filenames