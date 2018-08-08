from Scripts.removeComments import remove_comments


class ScopeExtractor:

    def get_next_scope(self, string):
        contents_split_by_line_with_comments = string.split('\n')[0:-1]
        self.contents_split_by_line = [remove_comments(line) for line in contents_split_by_line_with_comments]
        for starting_index in self._find_next_scope_starting_index():
            ending_index = self._find_scope_ending_index(starting_index)
            body = self._get_scope_from_starting_and_ending_indices(starting_index, ending_index)
            yield starting_index, body

    def _find_next_scope_starting_index(self):
        scope_level = 0
        index = 1
        for line in self.contents_split_by_line:
            if scope_level == 0:
                if self.check_for_scope(line):
                    yield index
            scope_level += self.change_in_scope_level(line)
            index += 1

    def _find_scope_ending_index(self, index_of_scope_start):
        index = index_of_scope_start
        scope_level = self.change_in_scope_level(self.contents_split_by_line[index - 1])
        while (scope_level > 0) & (index < len(self.contents_split_by_line)):
            index += 1
            scope_level += self.change_in_scope_level(self.contents_split_by_line[index - 1])
        return index

    def _get_scope_from_starting_and_ending_indices(self, start_index, end_index):
        body = self.contents_split_by_line[start_index-1:end_index]
        scope_body = ''.join(body)
        return scope_body

    @staticmethod
    def change_in_scope_level(line):
        change = 0
        for character in line:
            if character == '{':
                change += 1
            elif character == '}':
                change += -1
        return change


class ScopeExtractorByType(ScopeExtractor):

    def __init__(self, scope_type):
        self.scope_type = scope_type

    def check_for_scope(self, line):
        return self.scope_type in line


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
