import os

from Scripts.generateScopes import generate_scopes
from Scripts.openFile import open_file
from Scripts.scope import Scope
from Scripts.timedFunction import timed_function


@timed_function
def check_ideologies(path, output_file):
    ideology_names = find_ideology_names_in_path(path)

    for reference in find_next_reference_to_ideologies(path):
        if reference.body not in ideology_names:
            output_file.write("Ideology " + reference.body + " not defined at " + str(reference.starting_line) + ' in ' + reference.filename + '\n')


def find_ideology_names_in_path(path):
    ideology_names = []
    for scope in find_next_ideology_scope(path):
        ideology_names += [ideology_name for ideology_name in find_next_ideology_name(scope)]
    return ideology_names


def find_ideology_name(ideology):
    body = ideology.body.strip(' \n\t\r')
    words = body.split(' ')
    ideology_name = words[0]
    return ideology_name


def find_next_reference_to_ideologies(path):
    subpaths = ['\\common', '\\events', '\\history']
    scope = 'has_government'
    for subpath in subpaths:
        for dirpath, dirs, filename in os.walk(path + subpath):
            string = open_file(dirpath + filename).read()
            for index, reference in ScopeExtractorByType(scope).get_next_scope(string):
                body_after_has_government = reference[reference.index('has_government') + 17:]
                reference_name = body_after_has_government.split(' ')[0].strip('\n\t\r}')
                yield Scope(dirpath + filename, index, reference_name)


def find_next_ideology_name(ideology_scope):
    for starting_index, name, body in generate_scopes(ideology_scope.body):
        starting_index += ideology_scope.index - 1
        yield name


def find_next_ideology_scope(path):
    subpath = '\\common\\ideologies'
    scope = 'ideologies'
    full_path = path + subpath

    for filename in os.walk(full_path):
        string = open_file(filename).read()
        for start_line, body in ScopeExtractor(scope).get_next_scope(string):
            yield Scope(filename, start_line, body)
