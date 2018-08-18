import os


def generate_filenames(path, subpaths):
    if subpaths is str:
        subpaths = [subpaths]
    for subpath in subpaths:
        for dirpath, dirs, filenames in os.walk(path + subpath):
            yield from filenames


def find_all_filenames(path, subpaths):
    filenames = [filename for filename in generate_filenames(path, subpaths)]
    return filenames
