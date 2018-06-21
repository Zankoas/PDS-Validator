def change_in_scope_level(line):
    change = 0
    for character in line:
        if character == '{':
            change += 1
        elif character == '}':
            change += -1
    return change