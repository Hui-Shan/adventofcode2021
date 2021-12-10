import numpy as np

from typing import List

_points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

_opener = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<"
}

_closer = {v: k for k, v in _opener.items()}


def get_closing_indices(line_in: str):
    """Returns indices of the list where a key in _points appears"""

    idx = [i for (i, char) in enumerate(line_in) if char in _points.keys()]
    return idx


if __name__ == "__main__":
    with open("inputs/input10.txt") as infile:
        user_input = infile.readlines()

    test_input = ["[({(<(())[]>[[{[]{<()<>>",
                  "[(()[<>])]({[<{<<[]>>(",
                  "{([(<{}[<>[]}>{[]{[(<()>",
                  "(((({<>}<{<{<>}{[]{[]{}",
                  "[[<[([]))<([[{}[[()]]]",
                  "[{[{({}]{}}([{[{{{}}([]",
                  "{<[[]]>}<{[{[{[]{()[[[]",
                  "[<(<(<(<{}))><([]([]()",
                  "<{([([[(<>()){}]>(<<{{",
                  "<{([{{}}[<[[[<>{}]]]>[]]]"]

    high_score = 0
    for j, line in enumerate(user_input):
        exp = ""
        added_score = False
        stripped = line.strip()
        searched = np.zeros(len(stripped))
        closing_idx = get_closing_indices(stripped)

        for cid in closing_idx:
            closer = stripped[cid]
            opener = _opener[closer]
            k = cid - 1

            closed = True
            while k > 0 and added_score is False:
                if searched[k] == 0:
                    if stripped[k] == opener:
                        searched[k: cid+1] = 1
                    else:
                        exp = _closer[stripped[k]]
                        closed = False
                    k = 0
                k = k - 1

            if not closed and not added_score:
                print(f"Expected {exp} but found {closer} instead.")
                high_score += _points[closer]
                added_score = True

    res1 = high_score
    print(res1)
