def remove_comments(line):
    split_line = line.split('#')
    # check that the line is not just a comment; if it is, return a space so that the line evaluates to true
    if (len(split_line) > 1) & (split_line[0] == ''):
        line_without_comments = ' '
    else:
        line_without_comments = split_line[0]
    return line_without_comments