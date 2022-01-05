from __future__ import annotations

import numpy as np

from typing import List


class Cube:
    def __init__(
        self,
        mode: str,
        xmin: int,
        xmax: int,
        ymin: int,
        ymax: int,
        zmin: int,
        zmax: int,
    ):
        self.mode = mode
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

        if self.mode == "on":
            self.array = np.ones((xmax - xmin + 1, ymax - ymin + 1, zmax - zmin + 1))
        else:
            self.array = np.zeros((xmax - xmin + 1, ymax - ymin + 1, zmax - zmin + 1))

    def overlap(self, other: Cube):
        if (
            (self.xmin < other.xmax < self.xmax or other.xmin < self.xmin < other.xmax)
            and (
                self.ymin < other.ymax < self.ymax
                or other.ymin < self.ymin < other.ymax
            )
            and (
                self.zmin < other.zmax < self.zmax
                or other.zmin < self.zmin < other.zmax
            )
        ):
            return True
        else:
            return False

    def update_array(self, other: Cube):
        if self.mode == "on" and other.mode == "on":
            x_overlap = [
                idx
                for (idx, x) in enumerate(range(self.xmin, self.xmax + 1))
                if other.xmin < x < other.xmax
            ]
            y_overlap = [
                idy
                for (idy, y) in enumerate(range(self.ymin, self.ymax + 1))
                if other.ymin < y < other.ymax
            ]
            z_overlap = [
                idz
                for (idz, z) in enumerate(range(self.zmin, self.zmax + 1))
                if other.zmin < z < other.zmax
            ]
            self.array[x_overlap, y_overlap, z_overlap] += 1
        elif self.mode == "off" and other.mode == "on":
            x_overlap = [
                idx
                for (idx, x) in enumerate(range(other.xmin, other.xmax + 1))
                if self.xmin < x < self.xmax
            ]
            y_overlap = [
                idy
                for (idy, y) in enumerate(range(other.ymin, other.ymax + 1))
                if self.ymin < y < self.ymax
            ]
            z_overlap = [
                idz
                for (idz, z) in enumerate(range(other.zmin, other.zmax + 1))
                if self.zmin < z < self.zmax
            ]
            other.array[x_overlap, y_overlap, z_overlap] = 0

    def number_of_on_pixels(self):
        return np.sum(self.array[self.array == 1])

    def __str__(self):
        return f"{self.mode} : [{self.xmin}-{self.xmax}, {self.ymin}-{self.ymax}, {self.zmin}-{self.zmax}]"


def get_on_off_ranges(txt_input: List):
    ranges = []
    for line in txt_input:
        stripped = line.strip()
        splits = stripped.split(" ")
        mode = splits[0]
        x_range, y_range, z_range = splits[1].split(",")

        xmin, xmax = [int(val) for val in x_range.split("=")[1].split("..")]
        ymin, ymax = [int(val) for val in y_range.split("=")[1].split("..")]
        zmin, zmax = [int(val) for val in z_range.split("=")[1].split("..")]

        box = {
            "xmin": xmin,
            "xmax": xmax,
            "ymin": ymin,
            "ymax": ymax,
            "zmin": zmin,
            "zmax": zmax,
        }
        ranges.append((mode, box))

    return ranges


if __name__ == "__main__":
    with open("inputs/input22.txt") as infile:
        puzzle_input = infile.readlines()

    # test_input = [
    #     "on x=10..12,y=10..12,z=10..12",
    #     "on x=11..13,y=11..13,z=11..13",
    #     "off x=9..11,y=9..11,z=9..11",
    #     "on x=10..10,y=10..10,z=10..10"
    # ]

    init_ranges = get_on_off_ranges(puzzle_input)

    # Part 1
    init_procedure_area = np.zeros((101, 101, 101))

    xmin_min = 0
    xmax_max = 0
    ymin_min = 0
    ymax_max = 0
    zmin_min = 0
    zmax_max = 0

    for command in init_ranges:
        if command[0] == "on":
            value = 1
        else:
            value = 0

        coords = command[1]

        if coords["xmin"] < xmin_min:
            xmin_min = coords["xmin"]
        if coords["ymin"] < ymin_min:
            ymin_min = coords["ymin"]
        if coords["zmin"] < zmin_min:
            zmin_min = coords["zmin"]
        if coords["xmax"] > xmax_max:
            xmax_max = coords["xmax"]
        if coords["ymax"] > ymax_max:
            ymax_max = coords["ymax"]
        if coords["zmax"] > zmax_max:
            zmax_max = coords["zmax"]

        xmin = max(-50, coords["xmin"]) + 50
        xmax = min(50, coords["xmax"]) + 50
        ymin = max(-50, coords["ymin"]) + 50
        ymax = min(50, coords["ymax"]) + 50
        zmin = max(-50, coords["zmin"]) + 50
        zmax = min(50, coords["zmax"]) + 50

        init_procedure_area[xmin : xmax + 1, ymin : ymax + 1, zmin : zmax + 1] = value

    res1 = np.sum(init_procedure_area).astype(int)
    print(res1)

    # # Part 2
    # cube_list = []
    # for command in init_ranges:
    #     if command[0] == "on":
    #         value = 1
    #     else:
    #         value = 0
    #
    #     coords = command[1]
    #
    #     if coords["xmin"] < xmin_min:
    #         xmin_min = coords["xmin"]
    #     if coords["ymin"] < ymin_min:
    #         ymin_min = coords["ymin"]
    #     if coords["zmin"] < zmin_min:
    #         zmin_min = coords["zmin"]
    #     if coords["xmax"] > xmax_max:
    #         xmax_max = coords["xmax"]
    #     if coords["ymax"] > ymax_max:
    #         ymax_max = coords["ymax"]
    #     if coords["zmax"] > zmax_max:
    #         zmax_max = coords["zmax"]
    #
    #     try:
    #
    #         new_cube = Cube(
    #             command[0],
    #             xmin=coords["xmin"],
    #             xmax=coords["xmax"],
    #             ymin=coords["ymin"],
    #             ymax=coords["ymax"],
    #             zmin=coords["zmin"],
    #             zmax=coords["zmax"],
    #         )
    #     except:
    #         print(coords)
    #     cube_list.append(new_cube)
    #
    # overlapping_cubes = 0
    # for (ii, cube) in enumerate(cube_list[1:]):
    #     print(ii)
    #     print(f"#{ii}: {cube} overlaps with")
    #     for other_cube in cube_list[:ii]:
    #         cubes_overlap = cube.overlap(other_cube)
    #         if cubes_overlap:
    #             overlapping_cubes += 1
    #             cube.update_array(other_cube)
    #
    # for cube in cube_list:
    #     print(cube.number_of_on_pixels())
