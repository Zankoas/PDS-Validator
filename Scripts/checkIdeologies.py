from Scripts.generateFilenames import generate_filenames
from Scripts.generateScopeIndicesByType import generate_scope_indices_by_type
from Scripts.generateScopes import generate_scopes
from Scripts.generateTopLevelScopeIndices import generate_top_level_scope_indices
from Scripts.openFile import open_file
from Scripts.scope import ScopeWithFilename
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
        ideology_names += [ideology_name.name for ideology_name in find_next_ideology_name(scope)]
    return ideology_names


def find_next_reference_to_ideologies(path):
    subpaths = ['\\common', '\\events', '\\history']
    scope = 'has_government'
    for filename in generate_filenames(path, subpaths):
        string = open_file(filename).read()
        for scope in generate_scopes(string, generate_scope_indices_by_type, scope):
            yield ScopeWithFilename(filename, scope)


def find_next_ideology_name(ideology_scope):
    for scope in generate_scopes(ideology_scope.body, generate_top_level_scope_indices):
        scope.index += ideology_scope.index - 1
        yield scope


def find_next_ideology_scope(path):
    subpath = '\\common\\ideologies'
    scope = 'ideologies'
    for filename in generate_filenames(path, subpath):
        string = open_file(filename).read()
        yield from generate_scopes(string, generate_scope_indices_by_type, scope)
