from os import listdir
from codecs import open


def check_brackets(path, output_file):
    check(path, output_file, "\\events", 'utf-8-sig')
    check(path, output_file, "\\common\\national_focus", 'utf-8-sig')


def not_commented(line):
    for letter in line:
        if letter == ' ' or letter == '\t':
            continue
        elif letter == '#':
            return False
        else:
            return True
    return False


def check(path, output_file, sub_path, encoding):
    path += sub_path
    for filename in listdir(path):
        current_line = 0
        file = open(path + '\\' + filename, 'r', encoding)
        line = file.readline()
        current_line += 1
        stack = []
        while line:
            split_line = line.split(' ')
            if not_commented(line):
                for letter in line:
                    if letter == '(':
                        stack.append(')')
                    elif letter == '[':
                        stack.append(']')
                    elif letter == '{':
                        stack.append('}')
                    elif letter == ')' or letter == ']' or letter == '}':
                        if (len(stack) == 0):
                            output_file.write(
                                sub_path + '\\' + filename + " Bracket: Not expected '" + letter + "' around line " + str(
                                    current_line) + '\n')
                        else:
                            letterPop = stack.pop()
                            if (letterPop != letter):
                                output_file.write(
                                    sub_path + '\\' + filename + " Bracket: Expecting: '" + letterPop + "' but found '" + letter + "' around line " + str(
                                        current_line) + '\n')
            line = file.readline()
            current_line += 1
        if len(stack) > 0:
            output_file.write(sub_path + '\\' + filename + " there are " + str(
                len(stack)) + " opening bracket(s) without closing bracket(s)\n")
