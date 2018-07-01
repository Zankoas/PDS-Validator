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
    print("Time taken to check for events with single options with AI chances: " + (t0*1000).__str__() + " ms")

    t0 = time.time()

    flagged_events = check_events_for_pictures(country_events)

    for flagged_event in flagged_events:
        output_file.write("No picture for event starting at " + str(
            flagged_event.starting_line) + ' in ' + flagged_event.filename + '.\n')

    t0 = time.time() - t0
    print("Time taken to check events for pictures: " + (t0 * 1000).__str__() + " ms")

    t0 = time.time()

    hidden_events = filter_for_hidden_events(country_events)

    flagged_events = filter_for_events_with_field(hidden_events, 'picture')
    for flagged_event in flagged_events:
        output_file.write("Hidden event at " + str(flagged_event.starting_line) + ' in ' + flagged_event.filename + ' has a picture.\n')

    flagged_events = filter_for_events_with_field(hidden_events, 'title')
    for flagged_event in flagged_events:
        output_file.write("Hidden event at " + str(flagged_event.starting_line) + ' in ' + flagged_event.filename + ' has a title.\n')

    flagged_events = filter_for_events_with_field(hidden_events, 'desc')
    for flagged_event in flagged_events:
        output_file.write("Hidden event at " + str(flagged_event.starting_line) + ' in ' + flagged_event.filename + ' has a description.\n')

    flagged_events = filter_for_events_with_field(hidden_events, 'option')
    for flagged_event in flagged_events:
        output_file.write("Hidden event at " + str(flagged_event.starting_line) + ' in ' + flagged_event.filename + ' has options.\n')

    t0 = time.time() - t0
    print("Time taken to check that hidden events have no visible features: " + (t0 * 1000).__str__() + " ms")


def check_events_for_single_uses_of_ai_chance(country_events):
    flagged_events = []
    for event in country_events:
        if 'ai_chance' in event.body:
            if event.body.count('option =') == 1:
                flagged_events += [event]
    return flagged_events


def filter_for_hidden_events(events):
    hidden_events = []
    for event in events:
        if 'hidden = yes' in event.body:
            hidden_events += [event]
    return hidden_events


def filter_for_events_with_field(events, field_name):
    flagged_events = []
    for event in events:
        if field_name + ' =' in event.body:
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
