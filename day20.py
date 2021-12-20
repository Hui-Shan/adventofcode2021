import numpy as np

from typing import List

from utils import get_time


symbols = {".": 0, "#": 1}


def get_binary_for_pixel(img: np.array, row: int, col: int, inf_value: str):
    neighborhood = np.ones((3, 3)).astype(int) * symbols[inf_value]

    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            y = row + dy
            x = col + dx
            if -1 < y < img.shape[0] and -1 < x < img.shape[1]:
                neighborhood[dy + 1, dx + 1] = img[y, x]

    binary_list = list(neighborhood.ravel())

    return "".join([str(el) for el in binary_list])


def iterate(img: np.array, encoding: str, inf_value: str = "."):
    pad_len = 2
    new_height = img.shape[0] + 2 * pad_len
    new_width = img.shape[1] + 2 * pad_len

    if inf_value == ".":
        img_in_padded = np.zeros((new_height, new_width))
    else:
        img_in_padded = np.ones((new_height, new_width))

    img_in_padded[
        pad_len : pad_len + img.shape[0], pad_len : pad_len + img.shape[1]
    ] = img

    img_out = np.zeros((new_height, new_width))

    for ii in range(img_out.shape[0]):
        for jj in range(img_out.shape[1]):
            bin_val = get_binary_for_pixel(img_in_padded, ii, jj, inf_value)
            idx = int(bin_val, 2)
            sym = symbols[encoding[idx]]
            img_out[ii, jj] = sym

    inf_digit = symbols[inf_value]
    new_inf_value = encoding[int("".join([str(inf_digit) * 9]), 2)]

    return img_out.astype(int), new_inf_value


def get_encoding_and_image(txt_input: List) -> (str, np.array):
    encoding = txt_input[0].strip()

    # make image
    width = len(txt_input[2].strip())
    height = len(txt_input[2:])
    image = np.zeros((height, width))
    for (row, line) in enumerate(txt_input[2:]):  # there is a space
        stripped = line.strip()
        for (key, value) in symbols.items():
            stripped = stripped.replace(key, str(value))
        image[row, :] = [int(el) for el in stripped]

    return encoding, image.astype(int)


if __name__ == "__main__":
    with open("inputs/input20.txt") as infile:
        puzzle_input = infile.readlines()

    test_input = [
        "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#",
        "",
        "#..#.",
        "#....",
        "##..#",
        "..#..",
        "..###",
    ]

    print(get_time())

    enc, img = get_encoding_and_image(puzzle_input)
    img_out = img
    inf_val_out = "."
    for ii in range(50):
        img_out, inf_val_out = iterate(img_out, enc, inf_value=inf_val_out)

        if ii == 1:
            res1 = np.sum(img_out)
            print(res1)
            print(get_time())

    res2 = np.sum(img_out)
    print(res2)
    print(get_time())
