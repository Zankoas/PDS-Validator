import bisect

from Scripts.removeComments import remove_comments


def get_next_scope(string, *scope_type):
    contents_split_by_line_with_comments = string.split('\n')
    while contents_split_by_line_with_comments[-1] == '':
        contents_split_by_line_with_comments = contents_split_by_line_with_comments[0:-1]
    contents_split_by_line = [remove_comments(line) for line in contents_split_by_line_with_comments]
    contents = ''.join(contents_split_by_line)
    indices_of_new_lines = find_indices_of_new_lines(contents)
    for starting_index in generate_scope_starting_indices(contents):
        ending_index = find_scope_ending_index(starting_index, contents)
        starting_line = bisect.bisect(indices_of_new_lines, starting_index) + 1
        body = contents[starting_index:ending_index+1]
        name, body = parse_scope(body)
        if scope_type:
            if scope_type == name:
                yield starting_line, name, body
        else:
            yield starting_line, name, body


def parse_scope(contents):
    equals_index = 0
    while contents[equals_index] != '=':
        equals_index += 1
    name_index = equals_index - 1
    while contents[name_index] == ' ':
        name_index -= 1
    name_end_index = name_index
    while contents[name_index] not in ' \n':
        name_index -= 1
    name_start_index = name_index
    name = contents[name_start_index:name_end_index+1]

    body_index = equals_index + 1
    while contents[body_index] == ' ':
        body_index += 1
    if contents[body_index] == '{':
        parenthesis_start_index = body_index
        scope_level = 1
        body_index += 1
        while (scope_level > 0):
            body_index += 1
            scope_level += change_in_scope_level(contents[index])
        parenthesis_end_index = body_index

        body_start_index = parenthesis_start_index + 1
        while contents[body_start_index] in ' \n':
            body_start_index += 1

        body_end_index = parenthesis_end_index - 1
        while contents[body_end_index] in ' \n':
            body_end_index -= 1
    else:
        body_start_index = body_index
        while contents[body_index] not in ' \n':
            body_index += 1
        body_end_index = body_index
    body = contents[body_start_index, body_end_index]
    return name, body


def generate_scope_starting_indices(contents, *scope_type):
    index = 0
    try:
        while True:
            index = contents.index(scope_type, index)
            yield index
    except ValueError:
        pass


def find_scope_ending_index(index_of_scope_start, contents):
    index = index_of_scope_start
    while contents[index] != '=':
        index += 1
    index += 1
    while contents[index] == ' ' or contents[index] == '\n':
        index += 1
    if contents[index] == '{':
        scope_level = 1
        index += 1
        while (scope_level > 0) & (index < len(contents)):
            index += 1
            scope_level += change_in_scope_level(contents[index])
    else:
        while contents[index+1] != ' ' and contents[index+1] != '\n':
            index += 1
    return index


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

