import numpy as np

from typing import List


def get_points_str(line_str: str) -> tuple:
    """ Return tuple of coordinates from line string """

    point_list = line_str.strip().split(" -> ")

    start = [int(val) for val in point_list[0].split(",")]
    end = [int(val) for val in point_list[1].split(",")]

    return start, end


def get_grid_size(inputs: List):
    x_max = -1
    y_max = -1

    for item in inputs:
        start, end = get_points_str(item)
        x_max = max(x_max, max(start[0], start[0]))
        y_max = max(y_max, max(start[1], end[1]))

    return y_max + 2, x_max + 2


if __name__ == "__main__":
    with open('inputs/input05.txt') as infile:
        user_input = infile.readlines()

    grid_size = get_grid_size(user_input)

    for only_horizontal in [True, False]:
        field = np.zeros(grid_size)
        for line in user_input:
            (p1, p2) = get_points_str(line)

            ys = [p1[1], p2[1]]
            xs = [p1[0], p2[0]]

            if xs[0] == xs[1]:
                ys.sort()
                yrange = range(ys[0], ys[1] + 1)
                for yy in yrange:
                    field[yy, xs[0]] += 1
            elif ys[0] == ys[1]:
                xs.sort()
                xrange = range(xs[0], xs[1] + 1)
                for xx in xrange:
                    field[ys[0], xx] += 1
            else:
                if not only_horizontal:
                    if xs[1] > xs[0]:
                        xrange = range(xs[0], xs[1] + 1)
                    else:
                        xrange = range(xs[0], xs[1] - 1, -1)
                    if ys[1] > ys[0]:
                        yrange = range(ys[0], ys[1] + 1)
                    else:
                        yrange = range(ys[0], ys[1] - 1, -1)

                    for (xx, yy) in zip(xrange, yrange):
                        field[yy, xx] += 1

        res = np.sum(field >= 2)
        if only_horizontal:
            print(f"Part 1: Only horizontal {res}")
        else:
            print(f"Part 2: Also diagonal {res}")
