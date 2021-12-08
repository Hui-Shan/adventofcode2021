from typing import Dict, List


lengths = {
    2: 1,
    3: 7,
    4: 4,
    7: 8
}


def alphasort(inp: str):
    """ Returns input string in alphabetical order """
    return ''.join(sorted(inp))


def total_overlap(inp: str, comparison: str):
    """ Returns True if all elements in inp are also in comparison """
    present = True
    for letter in inp:
        present = present & (letter in comparison)

    return present


def get_output_part(lines_in: List) -> List:
    """ Returns alphabetically sorted output digits """
    lines_out = []
    for line in lines_in:
       output_parts = line.strip().split(" | ")[1].split(" ")
       output_parts_sorted = [alphasort(elem) for elem in output_parts]
       lines_out.append(output_parts_sorted)

    return lines_out


def decode_input(signal_patterns: List) -> Dict:
    digit2pattern = {}

    sorted_patterns = [alphasort(el) for el in signal_patterns]
    patterns_found = []

    # easy ones first
    for pat in sorted_patterns:
        if len(pat) in lengths.keys():
            digit2pattern[lengths[len(pat)]] = pat
            patterns_found.append(pat)

    patterns_to_find = [pat for pat in sorted_patterns if pat not in patterns_found]
    for pat in patterns_to_find:
        if len(pat) == 5:
            if total_overlap(digit2pattern[1], pat):
                digit2pattern[3] = pat
                patterns_found.append(pat)

    # find 0, 6 and 9 (len(6)
    patterns_to_find = [pat for pat in sorted_patterns if pat not in patterns_found]
    for pat in patterns_to_find:
        if len(pat) == 6:
            if total_overlap(digit2pattern[4], pat) and total_overlap(digit2pattern[7], pat):
                digit2pattern[9] = pat
                patterns_found.append(pat)
            elif total_overlap(digit2pattern[7], pat):
                digit2pattern[0] = pat
                patterns_found.append(pat)
            else:
                digit2pattern[6] = pat
                patterns_found.append(pat)

    # find letter of topleft segment
    topleft_letter = ""
    for letter in digit2pattern[9]:
        if letter not in digit2pattern[3]:
            topleft_letter = letter

    patterns_to_find = [pat for pat in sorted_patterns if pat not in patterns_found]
    for pat in patterns_to_find:
        if topleft_letter in pat:
            digit2pattern[5] = pat
            patterns_found.append(pat)
        else:
            digit2pattern[2] = pat
            patterns_found.append(pat)

    mapping = {v: k for k, v in digit2pattern.items()}

    return mapping


if __name__ == "__main__":
    with open('inputs/input08.txt') as infile:
        user_input = infile.readlines()

    outpart = get_output_part(user_input)
    unique_digit_lengths = [2, 3, 4, 7]

    n = 0
    for part in outpart:
        for subpart in part:
            if len(subpart) in unique_digit_lengths:
                n = n + 1

    res1 = n
    print(res1)

    total_sum = 0
    for line in user_input:
        input_part, output_part = line.split(" | ")
        dd = decode_input(input_part.split(" "))

        digit_out = ""
        for pattern in output_part.strip().split(" "):
            digit_out += str(dd[alphasort(pattern)])

        total_sum += int(digit_out)

    res2 = total_sum
    print(res2)



