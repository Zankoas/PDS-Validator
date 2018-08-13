import os

from Scripts.openFile import open_file
from Scripts.scope import Scope
from Scripts.scopeExtractor import ScopeExtractorByType, ScopeExtractorByScopeLevel
from Scripts.timedFunction import timed_function


@timed_function
def check_equipment_bonus(path, output_file):
    for equipment_bonus in find_next_equipment_bonus(path):
        if 'instant' not in equipment_bonus.body:
            output_file.write("\'instant \' field missing from equipment bonus starting at " + str(equipment_bonus.starting_line) + ' in ' + equipment_bonus.filename + '\n')


def find_next_equipment_bonus(path):
    subpath = '\\common\\ideas'
    scope_type = 'equipment_bonus'
    full_path = path + subpath

    for filename in os.walk(full_path):
        string = open_file(filename).read()
        for equipment_bonus_scope in ScopeExtractorByType(scope_type).get_next_scope(string):
            for index, equipment_bonus in ScopeExtractorByScopeLevel(1).get_next_scope(equipment_bonus_scope.body, equipment_bonus_scope.filename):
                yield Scope(filename, index, equipment_bonus)
