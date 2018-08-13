from Scripts.getAllFilenames import get_all_filenames
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

    eq_bonus_scope_extractor = ScopeExtractorByType(scope_type)
    eq_bonus_extractor = ScopeExtractorByScopeLevel(1)
    for filename in get_all_filenames(full_path):
        string = open_file(filename).read()
        for equipment_bonus_scope in eq_bonus_scope_extractor.get_next_scope(string):
            for index, equipment_bonus in eq_bonus_extractor.get_next_scope(equipment_bonus_scope.body, equipment_bonus_scope.filename):
                yield Scope(filename, index, equipment_bonus)
