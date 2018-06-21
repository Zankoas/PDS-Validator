import time
from Scripts.scopeScanner import ScopeScanner


def check_ai_chance(path, output_file):
    t0 = time.time()

    subpaths = ['\\events']
    scope = 'country_event'

    ai_chance_checker = AIChanceChecker(path, subpaths, scope=scope)
    flagged_events = ai_chance_checker.scan_files()

    for flagged_event in flagged_events:
        output_file.write("ai_chance present in event ending at " + str(
            flagged_event.line) + ' in ' + flagged_event.filename + 'but there is only one option.\n')

    t0 = time.time() - t0
    print("Time taken for AI chance script: " + (t0*1000).__str__() + " ms")


class Event:

    def __init__(self, line_number, filename):
        self.line = line_number
        self.filename = filename


class AIChanceChecker(ScopeScanner):

    def initialize_additional_variables(self):
        self.flagged_events = []

    def actions_on_scope_start(self):
        self.number_of_options = 0
        self.ai_chance_present = False

    def actions_in_scope(self):
        if 'ai_chance' in self.line:
            self.ai_chance_present = True
        if 'option' in self.line:
            self.number_of_options += 1

    def actions_on_end_of_scope(self):
        if (self.number_of_options == 1) & self.ai_chance_present:
            self.flagged_events += [Event(self.current_line, self.filename)]

    def return_outputs(self):
        return self.flagged_events
