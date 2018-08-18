import bisect

from Scripts.removeComments import remove_comments
from Scripts.scope import Scope


def generate_scopes(string, scope_index_generator, *args):
    contents_split_by_line_with_comments = string.split('\n')
    while contents_split_by_line_with_comments[-1] == '':
        contents_split_by_line_with_comments = contents_split_by_line_with_comments[0:-1]
    contents_split_by_line = [remove_comments(line) for line in contents_split_by_line_with_comments]
    contents = ''.join(contents_split_by_line)
    indices_of_new_lines = find_indices_of_new_lines(contents)
    for starting_index, ending_index in scope_index_generator(contents, *args):
        starting_line = bisect.bisect(indices_of_new_lines, starting_index) + 1
        body = contents[starting_index:ending_index+1]
        name, body = parse_scope(body)
        yield Scope(starting_line, name, body)


def parse_scope(contents):
    equals_index = 0
    while contents[equals_index] != '=':
        equals_index += 1
    name = find_name(contents, equals_index)
    body = find_body(contents, equals_index)
    return name, body


def find_body(contents, equals_index):
    body_index = equals_index + 1
    while contents[body_index] == ' ':
        body_index += 1
    if contents[body_index] == '{':
        parenthesis_start_index = body_index
        scope_level = 1
        body_index += 1
        while (scope_level > 0):
            body_index += 1
            scope_level += change_in_scope_level(contents[body_index])
        parenthesis_end_index = body_index

        body_start_index = parenthesis_start_index + 1
        while contents[body_start_index] in ' \n':
            body_start_index += 1

        body_end_index = parenthesis_end_index - 1
        while contents[body_end_index] in ' \n':
            body_end_index -= 1
    else:
        body_start_index = body_index
        while contents[body_index] not in ' \n' and body_index < len(contents) - 1:
            body_index += 1
        body_end_index = body_index
    body = contents[body_start_index:body_end_index + 1]
    return body


def find_name(contents, equals_index):
    name_index = equals_index - 1
    while contents[name_index] == ' ':
        name_index -= 1
    name_end_index = name_index
    while contents[name_index] not in ' \n' and name_index > 0:
        name_index -= 1
    name_start_index = name_index
    name = contents[name_start_index:name_end_index + 1]
    return name


def find_indices_of_new_lines(contents):
    new_line_indices = []
    index = 0
    try:
        while True:
            index = contents.index('\n', index+1)
            new_line_indices += [index]
    except ValueError:
        return new_line_indices


def change_in_scope_level(character):
    if character == '{':
        change = 1
    elif character == '}':
        change = -1
    else:
        change = 0
    return change

