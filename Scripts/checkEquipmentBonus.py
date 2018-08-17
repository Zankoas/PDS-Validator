import os

from Scripts.openFile import open_file
from Scripts.scope import Scope
from Scripts.generateScopes import generate_scopes
from Scripts.timedFunction import timed_function


@timed_function
def check_equipment_bonus(path, output_file):
    for equipment_bonus in find_next_equipment_bonus(path):
        if 'instant' not in equipment_bonus.body:
            output_file.write("\'instant \' field missing from equipment bonus starting at " + str(equipment_bonus.index) + ' in ' + equipment_bonus.filename + '\n')


def find_next_equipment_bonus(path):
    subpath = '\\common\\ideas'
    scope_type = 'equipment_bonus'
    full_path = path + subpath

    for dirpath, dirs, filenames in os.walk(full_path):
        for file in filenames:
            string = open_file(dirpath + file).read()
            for equipment_bonus_scope in ScopeExtractorByType(scope_type).get_next_scope(string):
                for index, equipment_bonus in generate_scopes(equipment_bonus_scope.body):
                    yield Scope(dirpath + file, index, equipment_bonus)
