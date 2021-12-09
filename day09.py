import numpy as np

from typing import List


def get_array_from_input(input_in: List) -> np.array:
    """ Returns array from number input where each line is a row """

    n_rows = len(input_in)
    n_cols = len(input_in[0].strip())
    arr = np.zeros((n_rows, n_cols))

    for (ii, line_in) in enumerate(input_in):
        numbers = [int(num) for num in line_in.strip()]
        arr[ii, :] = numbers

    return arr.astype(int)


def get_neighbors(x: int, y: int, xmax: int, ymax: int) -> List:
    points = []
    steps = [-1, 1]

    for step in steps:
        if 0 <= (step + x) < xmax:
            points.append((step + x, y))
        if 0 <= (step + y) < ymax:
            points.append((x, step + y))

    return points


def get_risk_points(array: np.array) -> np.array:
    (n_rows, n_cols) = array.shape
    risk_array = np.zeros(array.shape)
    for rr in range(n_rows):
        for cc in range(n_cols):
            neighbors = get_neighbors(rr, cc, n_rows, n_cols)

            is_low = True
            for (y_neigh, x_neigh) in neighbors:
                is_low = is_low and (array[rr, cc] < array[y_neigh, x_neigh])

            if is_low:
                risk_array[rr, cc] = 1

    return risk_array


if __name__ == "__main__":
    with open("inputs/input09.txt") as infile:
        user_input = infile.readlines()

    test_input = ['2199943210',
                  '3987894921',
                  '9856789892',
                  '8767896789',
                  '9899965678']

    grid = get_array_from_input(user_input)
    # grid = get_array_from_input(test_input)

    risk_points = get_risk_points(grid)

    res1 = np.sum(np.multiply(grid + 1,  risk_points))
    print(res1)
