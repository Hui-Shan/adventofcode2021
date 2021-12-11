from typing import List


class Octopus:
    def __init__(self, x: int, y: int, level: int, xsize: int, ysize: int):
        self.x = int(x)
        self.y = int(y)
        self.level = int(level)
        self.has_flashed = False
        self.neighbors = self.get_neighbor_locations(int(xsize), int(ysize))

    def increase_level(self):
        if self.need_to_flash():
            self.has_flashed = True
        if self.has_flashed is False:
            self.level += 1

    def need_to_flash(self):
        return self.level > 9

    def get_neighbor_locations(self, xsize: int, ysize: int):
        deltas = [-1, 0, 1]
        neighbors = []
        for dx in deltas:
            for dy in deltas:
                posx = self.x + dx
                posy = self.y + dy
                if (
                    (posx != self.x or posy != self.y)
                    and 0 <= posx < xsize
                    and 0 <= posy < ysize
                ):
                    neighbors.append((posx, posy))
        return neighbors

    def flash(self):
        self.level = 0
        self.has_flashed = True

        return self.neighbors

    def __str__(self):
        return f"({self.x},{self.y}) {self.level} {self.has_flashed}"


class OctopusGrid:
    def __init__(self, octolist: List):
        self.total_flashes = 0
        self.octopi = []
        self.all_flash = False

        nrows = len(octolist)
        for row, line in enumerate(octolist):
            ncols = len(line.strip())
            for col, value in enumerate(line.strip()):
                self.octopi.append(Octopus(col, row, value, ncols, nrows))

    def get_octopus(self, locx: int, locy: int) -> Octopus:
        result = None
        for octopus in self.octopi:
            if octopus.x == locx and octopus.y == locy:
                result = octopus

        return result

    def get_flashing_octopi(self) -> List:
        coords = []
        for octopus in self.octopi:
            if octopus.level > 9:
                coords.append((octopus.x, octopus.y))

        return coords

    def take_step(self):
        # Add 1
        for octopus in self.octopi:
            octopus.increase_level()

        # Check for flashing octopi
        list_to_flash = self.get_flashing_octopi()

        while len(list_to_flash) > 0:
            for (xx, yy) in list_to_flash:
                neighbors = self.get_octopus(xx, yy).flash()
                for (ii, jj) in neighbors:
                    self.get_octopus(ii, jj).increase_level()

            list_to_flash = self.get_flashing_octopi()

        # Count flashes
        n_flashes_in_step = 0
        for octopus in self.octopi:
            if octopus.has_flashed:
                n_flashes_in_step += 1
                octopus.has_flashed = False

        self.all_flash = n_flashes_in_step == len(self.octopi)

        self.total_flashes += n_flashes_in_step

    def __str__(self):
        full_str = ""
        for octopus in self.octopi:
            full_str = full_str + str(octopus) + "\n"

        return full_str


if __name__ == "__main__":

    with open("inputs/input11.txt") as infile:
        user_input = infile.readlines()

    test_text = ["11111", "19991", "19191", "19991", "11111"]
    test_text = [
        "5483143223",
        "2745854711",
        "5264556173",
        "6141336146",
        "6357385478",
        "4167524645",
        "2176841721",
        "6882881134",
        "4846848554",
        "5283751526",
    ]

    octogrid = OctopusGrid(user_input)

    for step in range(100):
        octogrid.take_step()

    res1 = octogrid.total_flashes
    print(res1)

    octogrid2 = OctopusGrid(user_input)

    step = 0
    while not octogrid2.all_flash:
        octogrid2.take_step()
        step += 1

    res2 = step
    print(res2)
