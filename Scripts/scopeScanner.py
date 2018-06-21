from Scripts.fileScanner import FileScanner
from Scripts.changeInScopeLevel import change_in_scope_level


class ScopeScanner(FileScanner):

    #template function which executes for every line in a given file
    def while_in_file(self):
        if not self._in_scope:
            if self.scope in self.line:
                self._in_scope = True
                self.actions_on_scope_start()

        if self._in_scope:
            self.actions_in_scope()
            change = change_in_scope_level(self.line)
            self.actions_on_scope_level_change(change)
            self.scope_level += change
            if self.scope_level == 0:
                self._in_scope = False
                self.actions_on_end_of_scope()

    # actions that occur when the scope of interest is first found, but before moving on to the next line
    def actions_on_scope_start(self):
        pass

    # actions to carry out if the scope level changes in the current line
    def actions_on_scope_level_change(self, change):
        pass

    # actions to be carried out every line which still in scope
    def actions_in_scope(self):
        pass

    # actions to be carried out at the end of the scope of interest
    def actions_on_end_of_scope(self):
        pass

    def before_opening_file(self):
        self._in_scope = False
        self.scope_level = 0