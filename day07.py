import numpy as np


def calculate_fuel_costs(crabs: np.array, index: int, linear: bool = False):
    crabs = crabs.astype(int)
    abs_distances = np.abs(crabs - index)

    if linear:
        costs = np.sum(abs_distances).astype(int)
    else:
        # use n * (n + 1) / 2
        costs = np.sum(abs_distances * (abs_distances + 1) / 2).astype(int)

    return costs


if __name__ == "__main__":
    test_input = np.array([16, 1, 2, 0, 4, 2, 7, 1, 2, 14])

    with open('inputs/input07.txt') as infile:
        input_strings = infile.readlines()[0].strip().split(",")
        user_input = [int(val) for val in input_strings]

    # user_input = test_input
    positions = range(0, np.max(user_input).astype(int))

    for (part, lin) in enumerate([True, False]):
        min_pos = 0
        min_fuel = None
        for pos in positions:
            fuel = calculate_fuel_costs(np.array(user_input), pos, linear=lin)
            if min_fuel is None or fuel < min_fuel:
                min_pos = pos
                min_fuel = fuel

        print(f"Part {part}: {min_pos} {min_fuel}")
