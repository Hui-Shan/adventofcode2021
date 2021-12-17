def get_vy(vy0: str, t: int):
    return int(vy0) - t


def sum_series(n: int):
    return int(n * (n + 1) / 2)


if __name__ == "__main__":
    with open("inputs/input17.txt") as infile:
        puzzle_input = infile.readline()

    # example
    # puzzle_input = "target area: x=20..30, y=-10..-5"

    x_index = puzzle_input.index("x")
    xrange, yrange = puzzle_input[x_index:].split(", ")
    xmin, xmax = xrange.split("=")[-1].split("..")
    ymin, ymax = yrange.split("=")[-1].split("..")

    xmin = int(xmin)
    xmax = int(xmax)
    ymin = int(ymin)
    ymax = int(ymax)

    vymax = abs(ymin) - 1
    res1 = sum_series(vymax)
    print(res1)

    # Determine vx_min
    x_solve = 0
    sum = sum_series(x_solve)
    while sum < xmin:
        x_solve += 1
        sum = sum_series(x_solve)

    vy_min = ymin
    vy_max = abs(ymin) - 1
    vx_min = x_solve
    vx_max = xmax

    distinct_initials = []

    for vx0 in range(vx_min, vx_max + 1):
        for vy0 in range(vy_min, vy_max + 1):
            x = 0
            y = 0
            t = 0
            in_target_area = False
            while (x <= xmax and y >= ymin) and not in_target_area:
                if vx0 - t > 0:
                    x += vx0 - t
                y += vy0 - t
                t += 1

                in_target_area = xmin <= x <= xmax and ymin <= y <= ymax
                if in_target_area:
                    distinct_initials.append((vx0, vy0))

    distinct_initials = sorted(distinct_initials, key=lambda l: l[0])
    res2 = len(distinct_initials)
    print(res2)
