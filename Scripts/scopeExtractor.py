import bisect

from Scripts.removeComments import remove_comments


class ScopeExtractor:

    def __init__(self, scope_type):
        self.scope_type = scope_type

    def get_next_scope(self, string):
        contents_split_by_line_with_comments = string.split('\n')
        while contents_split_by_line_with_comments[-1] == '':
            contents_split_by_line_with_comments = contents_split_by_line_with_comments[0:-1]
        contents_split_by_line = [remove_comments(line) for line in contents_split_by_line_with_comments]
        contents = ''.join(contents_split_by_line)
        indices_of_new_lines = self._find_indices_of_new_lines(contents)
        for starting_index in self._generate_scope_starting_indices(contents):
            ending_index = self._find_scope_ending_index(starting_index, contents)
            starting_line = bisect.bisect(indices_of_new_lines, starting_index) + 1
            body = contents[starting_index:ending_index+1]
            yield starting_line, body

    def _generate_scope_starting_indices(self, contents):
        index = 0
        try:
            while True:
                index = contents.index(self.scope_type, index)
                yield index
        except ValueError:
            pass

    def _find_scope_ending_index(self, index_of_scope_start, contents):
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
                scope_level += self.change_in_scope_level(contents[index])
        else:
            while contents[index+1] != ' ' and contents[index+1] != '\n':
                index += 1
        return index

    def _find_indices_of_new_lines(self, contents):
        new_line_indices = []
        index = 0
        try:
            while True:
                index = contents.index(self.scope_type, index+1)
                new_line_indices += [index]
        except ValueError:
            return new_line_indices

    @staticmethod
    def change_in_scope_level(character):
        if character == '{':
            change = 1
        elif character == '}':
            change = -1
        else:
            change = 0
        return change


class FieldExtractor(ScopeExtractor):

    def __init__(self):
        self.scope_level = 0

    def check_for_scope(self, line):
        field_found = False
        if self.scope_level == 1:
            scope_name = line.strip(' \t\n\r').split(' ')[0]
            if (scope_name != '') & (scope_name != '}'):
                field_found = True
        self.scope_level += self.change_in_scope_level(line)
        return field_found
