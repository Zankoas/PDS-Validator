from Scripts.getAllFilenamesIn import get_all_filenames_in
from Scripts.removeComments import remove_comments
from Scripts.openFile import open_file


class FileScanner:
    def __init__(self, path, subpaths, scope=''):
        self.subpaths = subpaths
        self.scope = scope
        self.path = path
        self.filename = ''
        self.line = ''
        self.current_line = 0

    def scan_files(self):
        # template method for scanning through the files in subpaths
        self.initialize_additional_variables()
        for subpath in self.subpaths:
            path = self.path + subpath
            filenames = get_all_filenames_in(path)
            for self.filename in filenames:
                self.before_opening_file()

                file = open_file(self.filename)
                line = file.readline()
                self.line = remove_comments(line)
                self.current_line = 1

                while line:
                    self.while_in_file()

                    line = file.readline()
                    self.line = remove_comments(line)
                    self.current_line += 1

        return self.return_outputs()

    def initialize_additional_variables(self):
        # initialize any object variables that you need, such as output lists
        pass

    def while_in_file(self):
        # things to do for every line in the file
        pass

    def return_outputs(self):
        # have the return value of this function
        pass

    def before_opening_file(self):
        # things to do before opening each file, such as resetting variables
        pass
