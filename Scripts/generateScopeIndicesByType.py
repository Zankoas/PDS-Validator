from Scripts.findScopeEndingIndex import find_scope_ending_index


def generate_scope_indices_by_type(contents, type):
    index = 0
    while index < len(contents):
        starting_index_assigned = False
        while not starting_index_assigned and index < len(contents):
            potential_starting_index = contents.find(type, index)
            if potential_starting_index < 0 or contents[potential_starting_index-1] in ' \n{}':
                if potential_starting_index + len(type) >= len(contents) or contents[potential_starting_index + len(type)+1] in ' \n{}=':
                    starting_index = potential_starting_index
                    starting_index_assigned = True
            index += 1
        if starting_index_assigned:
            ending_index = find_scope_ending_index(starting_index, contents)
            yield starting_index, ending_index
            index = ending_index + 1


