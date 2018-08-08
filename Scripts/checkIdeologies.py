import time
from Scripts.scopeExtractor import ScopeExtractorByType, ScopeExtractorByScopeLevel
from Scripts.getAllFilenames import get_all_filenames
from Scripts.openFile import open_file
from Scripts.scope import Scope

def check_ideologies(path, output_file):
    t0 = time.time()

    ideology_names = find_ideology_names_in_path(path)

    for reference in find_next_reference_to_ideologies(path):
        if reference.body not in ideology_names:
            output_file.write("Ideology " + reference.body + " not defined at " + str(reference.starting_line) + ' in ' + reference.filename + '\n')

    t0 = time.time() - t0
    print("Time taken for ideology reference script: " + (t0*1000).__str__() + " ms")


def find_ideology_names_in_path(path):
    ideology_names = []
    for scope in find_next_ideology_scope(path):
        for ideology in find_next_ideology(scope):
            ideology_names += [find_ideology_name(ideology)]
    return ideology_names


def find_ideology_name(ideology):
    body = ideology.body.strip(' \n\t\r')
    words = body.split(' ')
    ideology_name = words[0]
    return ideology_name


def find_next_reference_to_ideologies(path):
    subpaths = ['\\common', '\\events', '\\history']
    scope = 'has_government'
    ideology_reference_finder = ScopeExtractorByType(scope)
    for subpath in subpaths:
        for filename in get_all_filenames(path + subpath):
            string = open_file(filename).read()
            for index, reference in ideology_reference_finder.get_next_scope(string):
                body_after_has_government = reference[reference.index('has_government') + 17:]
                reference_name = body_after_has_government.split(' ')[0].strip('\n\t\r}')
                yield Scope(filename, index, reference_name)


def find_next_ideology(ideology_scope):
    ideology_extractor = ScopeExtractorByScopeLevel(1)
    for starting_index, body in ideology_extractor.get_next_scope(ideology_scope.body):
        starting_index += ideology_scope.starting_line - 1
        yield Scope(ideology_scope.filename, starting_index, body)


def find_next_ideology_scope(path):
    subpath = '\\common\\ideologies'
    scope = 'ideologies'
    full_path = path + subpath

    ideology_scope_finder = ScopeExtractorByType(scope)
    for filename in get_all_filenames(full_path):
        string = open_file(filename).read()
        for start_line, body in ideology_scope_finder.get_next_scope(string):
            yield Scope(filename, start_line, body)
