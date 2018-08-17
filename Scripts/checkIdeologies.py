import os

from Scripts.generateScopes import generate_scopes
from Scripts.generateScopeIndicesByType import generate_scope_indices_by_type
from Scripts.generateTopLevelScopeIndices import generate_top_level_scope_indices
from Scripts.openFile import open_file
from Scripts.scope import Scope
from Scripts.timedFunction import timed_function


@timed_function
def check_ideologies(path, output_file):
    ideology_names = find_ideology_names_in_path(path)

    for reference in find_next_reference_to_ideologies(path):
        if reference.body not in ideology_names:
            output_file.write("Ideology " + reference.body + " not defined at " + str(reference.index) + ' in ' + reference.filename + '\n')


def find_ideology_names_in_path(path):
    ideology_names = []
    for scope in find_next_ideology_scope(path):
        ideology_names += [ideology_name for ideology_name in find_next_ideology_name(scope)]
    return ideology_names


def find_next_reference_to_ideologies(path):
    subpaths = ['\\common', '\\events', '\\history']
    scope = 'has_government'
    for subpath in subpaths:
        for dirpath, dirs, filenames in os.walk(path + subpath):
            for filename in filenames:
                string = open_file(dirpath + filename).read()
                for index, name, reference in generate_scopes(string, generate_scope_indices_by_type, scope):
                    yield Scope(dirpath + filename, index, reference)


def find_next_ideology_name(ideology_scope):
    for starting_index, name, body in generate_scopes(ideology_scope.body, generate_top_level_scope_indices):
        starting_index += ideology_scope.index - 1
        yield name


def find_next_ideology_scope(path):
    subpath = '\\common\\ideologies'
    scope = 'ideologies'
    full_path = path + subpath

    for filename in os.walk(full_path):
        string = open_file(filename).read()
        for start_line, name, body in generate_scopes(string, generate_scope_indices_by_type, scope):
            yield Scope(filename, start_line, body)
