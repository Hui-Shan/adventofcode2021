from __future__ import annotations
import numpy as np

from typing import List


class SnailFishNumber:
    def __init__(self, values: List[int], depths: List[int]):
        assert len(values) - len(depths) == 1, "len(values) - len(depths) != 1"
        self.values = values
        self.depths = depths

    def magnitude(self) -> int:
        if len(self.depths) == 0:
            val = self.values[0]
        else:
            index = self.depths.index(1)

            a = SnailFishNumber(
                self.values[: index + 1], [el - 1 for el in self.depths[:index]]
            )

            b = SnailFishNumber(
                self.values[index + 1 :], [el - 1 for el in self.depths[index + 1 :]]
            )

            val = 3 * a.magnitude() + 2 * b.magnitude()

        return val

    def explode(self) -> SnailFishNumber:
        index = [idx for idx, depth in enumerate(self.depths) if depth > 4]
        if len(index) == 0:
            return self
        else:
            index = index[0]

        new_values = []
        for ii, value in enumerate(self.values):
            if ii == index - 1:
                new_value = value + self.values[index]
            elif ii == index:
                new_value = 0
            elif ii == index + 1:
                pass  # Do not add new_value item to new_values
            elif ii == index + 2:
                new_value = value + self.values[index + 1]
            else:
                new_value = value

            if ii != index + 1:
                new_values.append(new_value)

        new_depths = self.depths
        new_depths.pop(index)

        return SnailFishNumber(new_values, new_depths).explode()

    def split(self) -> SnailFishNumber:

        index = [idx for idx, val in enumerate(self.values) if val > 9]
        if type(index) != int and len(index) > 0:
            index = index[0]
        else:
            return self

        # Replace offending value with a new pair with half of the value
        old_value = self.values[index]
        new_left_value = int(np.floor(self.values[index] / 2))
        new_right_value = old_value - new_left_value
        new_values = (
            self.values[:index]
            + [new_left_value, new_right_value]
            + self.values[index + 1 :]
        )

        # Get new depths value
        if index == 0:
            new_depth = self.depths[0] + 1
        elif index == len(self.depths):
            new_depth = self.depths[index - 1] + 1
        else:
            new_depth = max(self.depths[index - 1], self.depths[index]) + 1

        new_depths = self.depths
        new_depths.insert(index, new_depth)

        return SnailFishNumber(new_values, new_depths)

    def __add__(self, other):
        # concatenate values
        new_values = self.values + other.values
        # and make new depths
        new_depths = [depth + 1 for depth in self.depths]
        new_depths.append(1)
        new_depths.extend([depth + 1 for depth in other.depths])

        new_number = SnailFishNumber(new_values, new_depths)

        while True:
            reduced_number = new_number.explode().split()
            if reduced_number == new_number:
                break
            new_number = reduced_number

        return new_number

    def __str__(self):
        str_rep = ""

        for ii, val in enumerate(self.values):
            if ii < len(self.depths):
                depth = self.depths[ii]
            else:
                depth = 0
            if ii > 0:
                previous_depth = self.depths[ii - 1]
            else:
                previous_depth = 0
            if depth > previous_depth:
                str_rep += (depth - previous_depth) * "[" + str(val) + ","
            else:
                str_rep += str(val) + (previous_depth - depth) * "]"
                if ii < (len(self.values) - 1):
                    str_rep += ","

        return str_rep

    @staticmethod
    def from_string(str_rep: str) -> SnailFishNumber:
        values = str_rep.replace("[", "").replace("]", "").split(",")
        depths = []
        depth = 0
        for ii, el in enumerate(str_rep):
            if el == "[":
                depth += 1
            elif el == "]":
                depth -= 1
            elif el == ",":
                depths.append(depth)
        values = [int(el) for el in values]

        return SnailFishNumber(values, depths)


def sum_snailfishnumber_str_list(snf_str_list: List[str]) -> SnailFishNumber:
    """Returns snailfish sum from list of snailfishnumber strings"""

    snf_sum = SnailFishNumber.from_string(snf_str_list[0])
    for (ii, el) in enumerate(snf_str_list):
        if ii > 0:
            snf_el = SnailFishNumber.from_string(el)
            snf_sum = snf_sum + snf_el

    return snf_sum


if __name__ == "__main__":

    str_list = []
    with open("inputs/input18.txt") as infile:
        puzzle_input = infile.readlines()
        for line in puzzle_input:
            str_list.append(line.strip())

    res1 = sum_snailfishnumber_str_list(str_list).magnitude()
    print(res1)

    max_mag = 0
    for ii in range(len(str_list)):
        num_ii = SnailFishNumber.from_string(str_list[ii])
        for jj in range(1, len(str_list)):
            num_jj = SnailFishNumber.from_string(str_list[jj])

            num_sum = num_ii + num_jj
            mag = num_sum.magnitude()

            if mag > max_mag:
                max_mag = mag

    res2 = max_mag
    print(res2)
