from __future__ import annotations

import numpy as np

from typing import List


def get_on_off_ranges(txt_input: List) -> List:
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


class Zone:
    def __init__(self, x_range: tuple, y_range: tuple, z_range: tuple, sign: int):
        self.corners = [
            (x_range[0], x_range[1] + 1),
            (y_range[0], y_range[1] + 1),
            (z_range[0], z_range[1] + 1),
        ]
        self.sign = sign

    def is_positive(self) -> bool:
        return self.sign > 0

    def is_init_step(self) -> bool:
        within_range = True
        for ii in range(len(self.corners)):
            within_range = within_range and (
                min(self.corners[ii]) >= -50 and max(self.corners[ii]) <= 52
            )

        return within_range

    def signed_volume(self) -> int:
        volume = 1
        for ii in range(len(self.corners)):
            volume *= self.corners[ii][1] - self.corners[ii][0]
        return self.sign * volume

    def intersection(self, other: Zone) -> Zone:
        corners = []

        for ii in range(len(self.corners)):
            self_max = self.corners[ii][1]
            other_max = other.corners[ii][1]
            self_min = self.corners[ii][0]
            other_min = other.corners[ii][0]
            min_int = max(self_min, other_min)
            max_int = min(self_max, other_max) - 1
            if max_int >= min_int:
                int_corner = (min_int, max_int)
            else:
                return None
            corners.append(int_corner)

        return Zone(
            (min(corners[0]), max(corners[0])),
            (min(corners[1]), max(corners[1])),
            (min(corners[2]), max(corners[2])),
            -other.sign,
        )

    def __str__(self):
        corner_ranges = ""
        for ii in range(3):
            corner_ranges += (
                str(min(self.corners[ii])) + "-" + str(max(self.corners[ii]) - 1) + " "
            )
        return corner_ranges + str(self.sign)


def reboot_reactor(instructions: List[Zone]) -> int:
    zones = []
    for (ii, inst) in enumerate(instructions):
        zones_to_add = []

        if inst.is_positive():
            zones_to_add.append(inst)

        for known_zone in zones:
            int_zone = inst.intersection(known_zone)
            if int_zone is not None:
                zones_to_add.append(int_zone)

        zones.extend(zones_to_add)

    return sum([zone.signed_volume() for zone in zones])


if __name__ == "__main__":
    with open("inputs/input22.txt") as infile:
        puzzle_input = infile.readlines()

    test_input = [
        "on x=-20..26,y=-36..17,z=-47..7",
        "on x=-20..33,y=-21..23,z=-26..28",
        "on x=-22..28,y=-29..23,z=-38..16",
        "on x=-46..7,y=-6..46,z=-50..-1",
        "on x=-49..1,y=-3..46,z=-24..28",
        "on x=2..47,y=-22..22,z=-23..27",
        "on x=-27..23,y=-28..26,z=-21..29",
        "on x=-39..5,y=-6..47,z=-3..44",
        "on x=-30..21,y=-8..43,z=-13..34",
        "on x=-22..26,y=-27..20,z=-29..19",
        "off x=-48..-32,y=26..41,z=-47..-37",
        "on x=-12..35,y=6..50,z=-50..-2",
        "off x=-48..-32,y=-32..-16,z=-15..-5",
        "on x=-18..26,y=-33..15,z=-7..46",
        "off x=-40..-22,y=-38..-28,z=23..41",
        "on x=-16..35,y=-41..10,z=-47..6",
        "off x=-32..-23,y=11..30,z=-14..3",
        "on x=-49..-5,y=-3..45,z=-29..18",
        "off x=18..30,y=-20..-8,z=-3..13",
        "on x=-41..9,y=-7..43,z=-33..15",
        "on x=-54112..-39298,y=-85059..-49293,z=-27449..7877",
        "on x=967..23432,y=45373..81175,z=27513..53682",
    ]
    test_input = puzzle_input

    init_ranges = get_on_off_ranges(test_input)
    init_instructions = []
    puzzle_instructions = []
    for item in init_ranges:
        if item[0] == "on":
            sign = 1
        else:
            sign = -1

        zone = Zone(
            x_range=(item[1]["xmin"], item[1]["xmax"]),
            y_range=(item[1]["ymin"], item[1]["ymax"]),
            z_range=(item[1]["zmin"], item[1]["zmax"]),
            sign=sign,
        )

        puzzle_instructions.append(zone)
        if zone.is_init_step():
            init_instructions.append(zone)
            # print(zone.signed_volume())

    print("Part 1")
    res1b = reboot_reactor(init_instructions)
    print(f"Reboot version: {res1b}")

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
    print(f"Exp from simple version: {res1}")

    print("Part 2")
    res2 = reboot_reactor(puzzle_instructions)
    print(f"Reboot version: {res2}")
