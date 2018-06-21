import time
from Scripts.scopeScanner import ScopeScanner


def check_events_for_pictures(path, output_file):
    t0 = time.time()

    subpaths = ['\\events']
    scope = 'event'

    event_chance_checker = EventPictureChecker(path, subpaths, scope=scope)
    flagged_events = event_chance_checker.scan_files()

    for flagged_event in flagged_events:
        output_file.write("Event ending at " + str(
            flagged_event.line) + ' in ' + flagged_event.filename + ' has no picture.\n')

    t0 = time.time() - t0
    print("Time taken for event picture script: " + (t0*1000).__str__() + " ms")


class Event:

    def __init__(self, line_number, filename):
        self.line = line_number
        self.filename = filename


class EventPictureChecker(ScopeScanner):

    def initialize_additional_variables(self):
        self.flagged_events = []

    def actions_on_scope_start(self):
        self.picture_present = False
        self.is_hidden = False

    def actions_in_scope(self):
        if 'picture' in self.line:
            self.picture_present = True
        if 'hidden = yes' in self.line:
            self.is_hidden = True

    def actions_on_end_of_scope(self):
        if (not self.picture_present) & (not self.is_hidden):
            self.flagged_events += [Event(self.current_line, self.filename)]

    def return_outputs(self):
        return self.flagged_events
