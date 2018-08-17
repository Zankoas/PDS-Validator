from Scripts.findScopeEndingIndex import find_scope_ending_index


def generate_top_level_scope_indices(contents):
    index = 0
    while index < len(contents):
        while contents[index] in ' \n':
            index += 1
        starting_index = index
        ending_index = find_scope_ending_index(starting_index, contents)
        yield starting_index, ending_index
        index = ending_index + 1


