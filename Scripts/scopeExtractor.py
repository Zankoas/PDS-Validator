from Scripts.openFile import open_file
from Scripts.getAllFilenames import get_all_filenames


class ScopeExtractor:

    def from_path(self, path):
        scopes = []
        filenames = get_all_filenames(path)
        for filename in filenames:
            scopes += self.from_file(filename)
        return scopes

    def from_file(self, filename):
        file = open_file(filename)
        string = file.read()
        return self.from_string(string, filename)

    def from_string(self, string, filename):
        self.filename = filename
        self.lines = string.split('\n')
        for i in range(0, len(self.lines)-1):
            self.lines[i] = self._remove_comments(self.lines[i])
        indices_of_lines_with_scope_start = self._find_scope_starting_indices()
        indices_of_scope_endings = self._find_scope_ending_indices(indices_of_lines_with_scope_start)
        return self.find_scopes_from_starting_and_ending_indices(indices_of_lines_with_scope_start, indices_of_scope_endings)

    def _find_scope_starting_indices(self):
        indices_of_lines_with_scope_start = []
        for line in self.lines:
            if self.check_for_scope(line):
                indices_of_lines_with_scope_start += [self.lines.index(line)]
        return indices_of_lines_with_scope_start

    def _find_scope_ending_indices(self, indices_of_lines_with_scope_start):
        indices_of_scope_endings = []
        for line_index in indices_of_lines_with_scope_start:
            index = line_index
            scope_level = self.change_in_scope_level(self.lines[index])
            while scope_level > 0:
                index += 1
                scope_level += self.change_in_scope_level(self.lines[index])
            indices_of_scope_endings += [index]
        return indices_of_scope_endings

    def find_scopes_from_starting_and_ending_indices(self, indices_of_lines_with_scope_start, indices_of_scope_endings):
        scopes = []
        for i in range(0, len(indices_of_lines_with_scope_start)):
            scope_line = indices_of_lines_with_scope_start[i]
            body = self.lines[indices_of_lines_with_scope_start[i]:indices_of_scope_endings[i]+1]
            scope_body = '\n'.join(body)
            scope = Scope(scope_line, self.filename, scope_body)
            scopes += [scope]
        return scopes

    @staticmethod
    def _remove_comments(line):
        line_without_comments = line.split('#')[0]
        if not line_without_comments.endswith('\n'):
            line_without_comments += '\n'
        return line_without_comments

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


class ScopeExtractorByScopeLevel(ScopeExtractor):

    def __init__(self, scope_level):
        self.target_scope_level = scope_level
        self.scope_level = 0

    def check_for_scope(self, line):
        scope_at_target_level_found = False
        if self.scope_level == self.target_scope_level:
            scope_name = line.strip(' \t\n\r').split(' ')[0]
            if (scope_name != '') & (scope_name != '}'):
                scope_at_target_level_found = True
        self.scope_level += self.change_in_scope_level(line)
        return scope_at_target_level_found


class Scope:

    def __init__(self, starting_line_number, filename, body):
        self.starting_line = starting_line_number
        self.filename = filename
        self.body = body
