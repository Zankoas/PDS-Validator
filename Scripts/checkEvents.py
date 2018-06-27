import time
from Scripts.scopeExtractor import ScopeExtractorByType


def check_events(path, output_file):
    t0 = time.time()

    country_events = find_country_events(path)
    flagged_events = check_events_for_single_uses_of_ai_chance(country_events)

    for flagged_event in flagged_events:
        output_file.write("ai_chance present in event starting at " + str(
            flagged_event.starting_line) + ' in ' + flagged_event.filename + 'but there is only one option.\n')

    t0 = time.time() - t0
    print("Time taken for AI chance script: " + (t0*1000).__str__() + " ms")

    t0 = time.time()

    flagged_events = check_events_for_pictures(country_events)

    for flagged_event in flagged_events:
        output_file.write("No picture for event starting at " + str(
            flagged_event.starting_line) + ' in ' + flagged_event.filename + '.\n')

    t0 = time.time() - t0
    print("Time taken for picture script: " + (t0 * 1000).__str__() + " ms")

    t0 = time.time()

    flagged_events = check_hidden_events_for_pictures(country_events)

    for flagged_event in flagged_events:
        output_file.write("Hidden event at " + str(
            flagged_event.starting_line) + ' in ' + flagged_event.filename + ' has a picture but shouldn\'t.\n')




def check_events_for_single_uses_of_ai_chance(country_events):
    flagged_events = []
    for event in country_events:
        if 'ai_chance' in event.body:
            if event.body.count('option =') == 1:
                flagged_events += [event]
    return flagged_events


def check_hidden_events_for_pictures(events):
    flagged_events = []
    for event in events:
        if 'hidden = yes' in event.body:
            if 'picture =' in event.body:
                flagged_events += [event]
    return flagged_events


def check_events_for_pictures(events):
    flagged_events = []
    for event in events:
        if 'hidden = yes' not in event.body:
            if 'picture =' not in event.body:
                flagged_events += [event]
    return flagged_events


def find_country_events(path):
    subpath = '\\events'
    scope = 'country_event'
    event_extractor = ScopeExtractorByType(scope)
    return event_extractor.from_path(path + subpath)
