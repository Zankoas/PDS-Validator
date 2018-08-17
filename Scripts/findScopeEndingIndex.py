from Scripts.generateScopes import change_in_scope_level


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