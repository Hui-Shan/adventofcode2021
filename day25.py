import numpy as np

from typing import List


class Seafloor:
    def __init__(self, herd_map: List):
        self.xdim = len(herd_map[0])
        self.ydim = len(herd_map)
        self.symdict = {".": 0, ">": 1, "v": 2}
        self.numdict = {val: key for (key, val) in self.symdict.items()}
        self.steps = 0
        self.numeric_map = self.get_numeric_map(herd_map)

    def get_numeric_map(self, herd_map: List) -> np.array:
        numeric_map = np.zeros((self.ydim, self.xdim))
        for (y, line) in enumerate(herd_map):
            for (x, el) in enumerate(line):
                numeric_map[y, x] = self.symdict[el]

        return numeric_map

    def get_east_map(self, numeric_map: np.array) -> np.array:
        east_map = np.zeros(numeric_map.shape)
        east_map[:, : self.xdim - 1] = numeric_map[:, 1:]
        east_map[:, self.xdim - 1] = numeric_map[:, 0]

        return east_map.astype(int)

    def get_south_map(self, numeric_map: np.array) -> np.array:
        south_map = np.zeros(numeric_map.shape)
        south_map[: self.ydim - 1, :] = numeric_map[1:, :]
        south_map[self.ydim - 1, :] = numeric_map[0, :]

        return south_map

    def is_moving_east(self, numeric_map: np.array) -> tuple:
        moving = np.zeros(numeric_map.shape)
        east_map = self.get_east_map(numeric_map)

        moving[
            (east_map == 0) & (numeric_map == self.symdict[">"]),
        ] = 1

        new_pos = np.zeros((self.ydim, self.xdim))
        new_pos[:, 1:] = moving[:, : self.xdim - 1]
        new_pos[:, 0] = moving[:, self.xdim - 1]

        return moving, new_pos

    def is_moving_south(self, numeric_map: np.array) -> tuple:
        moving = np.zeros(numeric_map.shape)
        south_map = self.get_south_map(numeric_map)

        moving[
            (south_map == 0) & (numeric_map == self.symdict["v"]),
        ] = 1

        new_pos = np.zeros((self.ydim, self.xdim))
        new_pos[1:, :] = moving[: self.ydim - 1, :]
        new_pos[0, :] = moving[self.ydim - 1, :]

        return moving, new_pos

    def step(self) -> bool:
        # step east first
        new_herd_map = self.numeric_map
        moving_map_east, new_pos = self.is_moving_east(new_herd_map)
        new_herd_map[moving_map_east == 1] = self.symdict["."]
        new_herd_map[new_pos == 1] = self.symdict[">"]

        # then step south
        moving_map_south, new_pos_south = self.is_moving_south(new_herd_map)

        new_herd_map[moving_map_south == 1] = self.symdict["."]
        new_herd_map[new_pos_south == 1] = self.symdict["v"]

        self.numeric_map = new_herd_map
        self.steps += 1

        return new_herd_map

    def __str__(self):
        floor_str = ""
        for yy in range(self.ydim):
            line = ""
            for xx in range(self.xdim):
                line += self.numdict[self.numeric_map[yy, xx]]
            floor_str += line + "\n"

        return floor_str


if __name__ == "__main__":
    with open("inputs/input25.txt") as infile:
        puzzle_input = [line.strip() for line in infile.readlines()]

    # test_input = [
    #     "v...>>.vv>",
    #     ".vv>>.vv..",
    #     ">>.>v>...v",
    #     ">>v>>.>.v.",
    #     "v>v.vv.v..",
    #     ">.>>..v...",
    #     ".vv..>.>v.",
    #     "v.v..>>v.v",
    #     "....v..v.>"
    # ]
    # puzzle_input = test_input

    seafloor = Seafloor(puzzle_input)

    old_map = str(seafloor)
    new_map = ""

    while not (old_map == new_map):
        old_map = new_map
        seafloor.step()
        new_map = str(seafloor)

    res1 = seafloor.steps
    print(f"Res 1: {res1}")
