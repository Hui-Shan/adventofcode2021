class Octopus:
    def __init__(self, level):
        self.level = level
        self.has_flashed = False

    def need_to_flash(self):
        return self.level > 9

    def flash(self):
        self.level = 0


if __name__ == "__main__":

    string = 'asf'

