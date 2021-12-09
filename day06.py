import numpy as np

from typing import List


def simulate_a_day_list(old_states: List):
    new_states = []
    new_fishes = []
    for old in old_states:
        if old == 0:
            new = 6
            new_fishes.append(8)
        else:
            new = old - 1
        new_states.append(new)

    return new_states + new_fishes


def simulate_a_day(old_states: np.array):
    new_states = np.subtract(old_states, 1)
    n_new_fishes = np.sum(new_states < 0)
    new_states[new_states < 0] = 6

    return np.append(new_states, 8 * np.ones(n_new_fishes)).astype(int)


def simulate_a_day2(old_counts: np.array) -> np.array:
    new_counts = np.zeros(9)

    n_new_fish = np.sum(old_counts[0])
    new_counts[: old_counts.shape[0] - 1] = old_counts[1:]
    new_counts[6] += n_new_fish
    new_counts[8] = n_new_fish

    return new_counts


def simulate(init_state: List, days: int, verbose: bool = False):
    """Returns the number of fish after following from init_state after days"""

    if verbose:
        print(f"Initial state: {init_state}")
    sim_state = init_state
    for dd in range(days):
        if (dd % 10) == 0:
            print(dd)
        sim_state = simulate_a_day(sim_state)
        if verbose:
            print(f"After {str(dd + 1).zfill(2)} days: {sim_state}")

    return len(sim_state)


def simulate2(counts: np.array, days: int, verbose: bool = False):
    """Returns the number of fish after following from init_state count array after days"""

    sim_bins = counts
    for dd in range(days):
        sim_bins = simulate_a_day2(sim_bins)
        if verbose:
            print(f"After {str(dd + 1).zfill(2)} days: {sim_bins}")

    return np.sum(sim_bins)


if __name__ == "__main__":
    test_input = np.array([3, 4, 3, 1, 2])
    bins = np.bincount(test_input)

    for ii in range(0, 18):
        bins = simulate_a_day2(bins)
    test_answer = int(np.sum(bins))
    print(f"example {test_answer}")

    with open("inputs/input06.txt") as infile:
        string_lines = infile.readlines()[0].split(",")
        user_input = [int(val) for val in string_lines]

    res1 = int(simulate2(np.bincount(user_input), 80))
    print(res1)

    res2 = int(simulate2(np.bincount(user_input), 256))
    print(res2)
