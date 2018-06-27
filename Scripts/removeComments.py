def remove_comments(line):
    split_line = line.split('#')
    # check that the line is not just a comment; if it is, return a space so that the line evaluates to true
    if (len(split_line) > 1) & (split_line[0] == ''):
        line_without_comments = '\n'
    else:
        line_without_comments = split_line[0]
        if not line_without_comments.endswith('\n'):
            line_without_comments = line_without_comments + '\n'
    return line_without_comments
