import collections

from stringAndFileFromPath import files_as_strings_from_path_gen
from timedFunction import timed
from checkEvents import Bug, events_gen
from checkDuplicateIds import find_id

Event = collections.namedtuple('Event', 'id start_line filename')

@timed
def check_event_usage(mod_path, output_file):

    non_mtth_events = []

    event_ids = []
    called_ids = []
    called_events = []
    events_directory = '/events/'
    path = mod_path + events_directory
    for contents, filename in files_as_strings_from_path_gen(path):
        for event, start_line in events_gen(contents):
            event_id = find_id(event)
            if event_id:
                event_ids += [event_id]
            if 'mean_time_to_happen' not in event:
                non_mtth_events += [Event(event_id, start_line, filename)]
            for called_event, called_event_start_line in events_gen(event):
                called_event_id = find_id(called_event)
                if called_event_id:
                    called_ids += [called_event_id]
                    called_events += [Event(called_event_id, called_event_start_line+start_line-1, events_directory+filename)]

    directories_that_can_call_events = ['/common/national_focus/', '/common/on_actions/']
    for subdir in directories_that_can_call_events:
        for contents, filename in files_as_strings_from_path_gen(mod_path + subdir):
            for event, start_line in events_gen(contents):
                called_event_id = find_id(event)
                if called_event_id:
                    called_ids += [called_event_id]
                    called_events += [Event(find_id(event), start_line, subdir + filename)]

    bugs = []
    for event in non_mtth_events:
        if event.id not in called_ids:
            bugs += [Bug('Non-MTTH event is not called', event.start_line, event.filename)]

    for event in called_events:
        if event.id not in event_ids:
            bugs += [Bug('Event is called but not defined', event.start_line, event.filename)]

    for bug in bugs:
        output_file.write(bug.description + ' at line ' + str(bug.line) + ' in ' + bug.filename + '\n')