from Scripts.generateScopes import generate_scopes
from Scripts.generateScopeIndicesByType import generate_scope_indices_by_type
from Scripts.openFile import open_file
from Scripts.scope import ScopeWithFilename
from Scripts.timedFunction import timed_function
from Scripts.generateFilenames import generate_filenames


@timed_function
def check_events(path, output_file):
    for event in find_next_country_event(path):
        if 'ai_chance' in event.body and event.body.count('option =') == 1:
            output_file.write("ai_chance present in event starting at " + str(event.starting_line) + ' in ' + event.filename + 'but there is only one option.\n')
        if 'hidden = yes' not in event.body and 'picture =' not in event.body:
            output_file.write("No picture for event starting at " + str(event.starting_line) + ' in ' + event.filename + '.\n')
        if 'hidden = yes' in event.body:
            if 'picture =' in event.body:
                output_file.write("Hidden event at " + str(event.starting_line) + ' in ' + event.filename + ' has a picture.\n')
            if 'title =' in event.body:
                output_file.write("Hidden event at " + str(event.starting_line) + ' in ' + event.filename + ' has a title.\n')
            if 'desc =' in event.body:
                output_file.write("Hidden event at " + str(event.starting_line) + ' in ' + event.filename + ' has a description.\n')
            if 'option =' in event.body:
                output_file.write("Hidden event at " + str(event.starting_line) + ' in ' + event.filename + ' has options.\n')


def find_next_country_event(path):
    subpath = '\\events'
    scope = 'country_event'
    for filename in generate_filenames(path, subpath):
        string = open_file(filename).read()
        for scope in generate_scopes(string, generate_scope_indices_by_type, scope):
            yield ScopeWithFilename(filename, scope)