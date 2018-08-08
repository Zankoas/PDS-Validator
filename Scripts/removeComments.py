def remove_comments(line):
    line_without_comments = line.split('#')[0]
    if not line_without_comments.endswith('\n'):
        line_without_comments += '\n'
    return line_without_comments
