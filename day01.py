import numpy as np


def get_input() -> np.array:
    """Returns user input as numpy array"""
    input_file = "inputs\\input01.txt"

    return np.loadtxt(input_file)


def get_number_of_increases(array: np.array) -> int:
    """Returns the number of times a depth measurement increases in th"""

    diff = array[1:] - array[0 : len(array) - 1]

    return sum(diff > 0)


def get_sliding_window_array(array: np.array, width: int = 3) -> np.array:
    """Returns array filtered by sliding window sum filter of width"""

    sums = []
    for ii in range(len(array) - width + 1):
        sums.append(np.sum(array[ii : ii + width]))

    return np.array(sums)


def get_result_two(array: np.array, width: int = 3) -> int:
    """Returns the number of times the sum of measurements in a sliding windows increases from the previous sum"""

    sliding_sums = get_sliding_window_array(array, width)
    return get_number_of_increases(sliding_sums)


if __name__ == "__main__":
    user_input = get_input()

    res1 = get_number_of_increases(user_input)
    print(res1)

    res2 = get_result_two(user_input)
    print(res2)
