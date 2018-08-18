from Scripts.openFile import open_file
from Scripts.scope import ScopeWithFilename
from Scripts.generateScopes import generate_scopes
from Scripts.generateScopeIndicesByType import generate_scope_indices_by_type
from Scripts.testGenerateTopLevelScopes import generate_top_level_scope_indices
from Scripts.timedFunction import timed_function
from Scripts.generateFilenames import generate_filenames


@timed_function
def check_equipment_bonus(path, output_file):
    for equipment_bonus in find_next_equipment_bonus(path):
        if 'instant' not in equipment_bonus.body:
            output_file.write("\'instant \' field missing from equipment bonus starting at " + str(equipment_bonus.index) + ' in ' + equipment_bonus.filename + '\n')


def find_next_equipment_bonus(path):
    subpath = '\\common\\ideas'
    scope_type = 'equipment_bonus'
    for file in generate_filenames(path, subpath):
        string = open_file(file).read()
        for equipment_bonus_scope in generate_scopes(string, generate_scope_indices_by_type, scope_type):
            for scope in generate_scopes(equipment_bonus_scope.body, generate_top_level_scope_indices):
                yield ScopeWithFilename(file, scope)
