import numpy as np
from typing import List


def get_dots_and_instructions(txt_input: List):
    coords = []
    instructions = []
    for line in txt_input:
        if line.startswith("fold along"):
            axis, val = line.strip().split(" ")[-1].split("=")
            instructions.append((axis, int(val)))
        elif "," in line:
            x, y = line.strip().split(",")
            coords.append((int(x), int(y)))

    return coords, instructions


def fold_point(x_in: int, y_in: int, axis: str, val: int):

    y_out = y_in
    x_out = x_in
    if axis == "x":
        dx = x_in - val
        if dx > 0:
            x_out = val - dx

    if axis == "y":
        dy = y_in - val
        if dy > 0:
            y_out = val - dy

    return x_out, y_out


def print_dots(coords: List):
    # calculate maxes
    xmax = -1
    ymax = -1
    for coord in coords:
        x, y = coord
        if x > xmax:
            xmax = x
        if y > ymax:
            ymax = y

    # default_lines # [['.' for ii in range(xmax)] for jj in range(ymax)]
    folded_array = np.zeros((ymax + 1, xmax + 1))  # 0,0 is top left corner!

    for (x, y) in coords:
        folded_array[y, x] = 1

    # convert to string
    full_code = ""
    for jj in range(folded_array.shape[0]):
        line_out = ""
        for digit in list(folded_array[jj]):
            if digit == 0:
                line_out += "."
            else:
                line_out += "#"
        line_out += "\n"
        full_code += line_out

    print(full_code)


if __name__ == "__main__":
    with open("inputs/input13.txt") as infile:
        puzzle_input = infile.readlines()

    dots, instrs = get_dots_and_instructions(puzzle_input)

    dots_old = dots
    for (jj, (axis_i, val_i)) in enumerate(instrs):
        dots_new = []

        for (x_old, y_old) in dots_old:
            x_new, y_new = fold_point(x_old, y_old, axis_i, val_i)
            if (x_new, y_new) not in dots_new:
                dots_new.append((x_new, y_new))

        dots_old = dots_new

        if jj == 0:
            res1 = len(dots_new)
            print(f"Result part 1: {res1}")

    print("Result part 2:")
    print_dots(dots_old)
