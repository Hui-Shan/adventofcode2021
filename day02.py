class Submarine1:
    def __init__(self, horizontal, depth):
        self.horizontal = horizontal
        self.depth = depth

    def get_horizontal(self):
        return self.horizontal

    def get_depth(self):
        return self.depth

    def get_depth_horizontal_multiplied(self):
        return self.get_depth() * self.get_horizontal()

    def set_horizontal(self, value):
        self.horizontal = value

    def set_depth(self, value):
        self.depth = value

    def edit_location(self, commando: str):
        diff = int(commando.split(" ")[1])
        if commando.startswith("forward"):
            self.set_horizontal(self.get_horizontal() + diff)
        elif commando.startswith("down"):
            self.set_depth(self.get_depth() + diff)
        elif commando.startswith("up"):
            self.set_depth(self.get_depth() - diff)


class Submarine2(Submarine1):
    def __init__(self, horizontal, depth, aim):
        super().__init__(horizontal, depth)
        self.aim = aim

    def get_aim(self):
        return self.aim

    def set_aim(self, value):
        self.aim = value

    def edit_location(self, command: str):
        diff = int(command.split(" ")[1])
        if command.startswith("forward"):
            self.set_horizontal(self.get_horizontal() + diff)
            self.set_depth(self.get_depth() + diff * self.get_aim())
        elif command.startswith("down"):
            self.set_aim(self.get_aim() + diff)
        elif command.startswith("up"):
            self.set_aim(self.get_aim() - diff)


if __name__ == "__main__":
    with open("inputs/input02") as infile:
        commands = infile.readlines()

    yellow1 = Submarine1(0, 0)
    for command in commands:
        yellow1.edit_location(commando=command)

    res1 = yellow1.get_depth_horizontal_multiplied()
    print(res1)

    yellow2 = Submarine2(0, 0, 0)
    for command in commands:
        yellow2.edit_location(command=command)

    res2 = yellow2.get_depth_horizontal_multiplied()
    print(res2)
