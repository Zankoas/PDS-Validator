from Scripts.removeComments import remove_comments


def get_next_line(file):
    line = file.readline()
    if line:
        line = remove_comments(line)
    return line