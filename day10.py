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

_comp_points = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

_closer = {v: k for k, v in _opener.items()}


def get_closing_indices(line_in: str):
    """Returns indices of the list where a key in _points appears"""

    idx = [i for (i, char) in enumerate(line_in) if char in _points.keys()]
    return idx


def calculate_corruption_score(line: str) -> int:
    """
    Returns (0, "Incomplete") if line is incomplete.
    Otherwise, returns (score, "expected x but found y instead.").
    """

    exp = ""
    added_score = False

    stripped = line.strip()
    searched = np.zeros(len(stripped))
    closing_idx = get_closing_indices(stripped)

    score = 0
    message = "Incomplete"

    for cid in closing_idx:
        closer = stripped[cid]
        opener = _opener[closer]
        k = cid - 1

        closed = True
        while k > -1 and added_score is False:
            if searched[k] == 0:
                if stripped[k] == opener:
                    searched[k: cid + 1] = 1
                else:
                    exp = _closer[stripped[k]]
                    closed = False
                k = 0
            k = k - 1

        if not closed and not added_score:
            message = f"Expected {exp} but found {closer} instead."
            score = _points[closer]
            added_score = True

    return score, message


def get_completion(incomplete: str) -> str:
    stripped = incomplete.strip()
    searched = np.zeros(len(stripped))
    closing_idx = get_closing_indices(stripped)

    for cid in closing_idx:
        closer = stripped[cid]
        opener = _opener[closer]
        k = cid - 1

        while k > -1:
            if searched[k] == 0:
                if stripped[k] == opener:
                    searched[k: cid + 1] = 1
                k = 0
            k -= 1

    unmatched = [sym for (sym, search) in zip(stripped, searched) if search == 0]
    to_add = [_closer[el] for el in unmatched]

    return ''.join(to_add[::-1])


def get_autocompletion_score(completion: str) -> int:
    total_score = 0
    for el in completion:
        total_score = (5 * total_score) + _comp_points[el]

    return total_score


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

    #
    test_input2 = [
        "[({(<(())[]>[[{[]{<()<>>",
        "[(()[<>])]({[<{<<[]>>(",
        "(((({<>}<{<{<>}{[]{[]{}",
        "{<[[]]>}<{[{[{[]{()[[[]",
        "<{([{{}}[<[[[<>{}]]]>[]]"
    ]

    high_score = 0
    completion_scores = []
    for j, line in enumerate(user_input):
        line_score = calculate_corruption_score(line)[0]
        high_score += line_score

        if line_score == 0:
            comp_str = get_completion(line)
            comp_line_score = get_autocompletion_score(comp_str)
            completion_scores.append(comp_line_score)

    res1 = high_score
    print(res1)

    completion_scores.sort()
    res2 = completion_scores[int(len(completion_scores)/2)]
    print(res2)
