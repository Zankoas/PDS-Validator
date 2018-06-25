from Scripts.changeInScopeLevel import change_in_scope_level
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
        self.string = string
        self.lines = string.split('\n')
        for i in range(0, len(self.lines)-1):
            self.lines[i] = self._remove_comments(self.lines[i])
        scopes = []
        self.scope_level = 0
        self.line_number = 1
        while self.line_number < len(self.lines):
            self.line = self.lines[self.line_number-1]
            if self.check_for_scope():
                scope_line = self.line_number
                scope_body = self._extract_scope_body()
                scope = Scope(scope_line, filename, scope_body)
                scopes += [scope]
            else:
                self.scope_level += change_in_scope_level(self.lines[self.line_number-1])
            self.line_number += 1
        return scopes

    def _extract_scope_body(self):
        inner_scope_level = 0
        scope_body = self.lines[self.line_number-1]
        inner_scope_level += change_in_scope_level(self.lines[self.line_number-1])
        self.scope_level += change_in_scope_level(self.lines[self.line_number-1])
        while (inner_scope_level > 0) & (self.line_number < len(self.lines)):
            self.line_number += 1
            self.line = self.lines[self.line_number-1]
            scope_body += self.line
            inner_scope_level += change_in_scope_level(self.line)
            self.scope_level += change_in_scope_level(self.lines[self.line_number-1])
        return scope_body

    @staticmethod
    def _remove_comments(line):
        line_without_comments = line.split('#')[0]
        if not line_without_comments.endswith('\n'):
            line_without_comments += '\n'
        return line_without_comments


class ScopeExtractorByType(ScopeExtractor):

    def __init__(self, scope_type):
        self.scope_type = scope_type

    def check_for_scope(self):
        return self.scope_type in self.line


class ScopeExtractorByScopeLevel(ScopeExtractor):

    def __init__(self, scope_level):
        self.target_scope_level = scope_level

    def check_for_scope(self):
        scope_at_target_level_found = False
        if self.scope_level == self.target_scope_level:
            scope_name = self.line.strip(' \t\n\r').split(' ')[0]
            if (scope_name != '') & (scope_name != '}'):
                scope_at_target_level_found = True
        return scope_at_target_level_found


class Scope:

    def __init__(self, starting_line_number, filename, body):
        self.starting_line = starting_line_number
        self.filename = filename
        self.body = body