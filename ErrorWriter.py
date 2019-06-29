class ErrorWriter:
    def __init__(self, file_error):
        self.file_error = file_error
        self.line = 0

    def update_line(self, line):
        self.line = line

    def write(self, err):
        with open(file=self.file_error, mode="a") as err_file:
            err_file.write("{}: ".format(self.line) + err)
