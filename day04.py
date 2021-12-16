import numpy as np

from typing import List


class BingoBoard:
    def __init__(self, grid_str):
        self.grid = np.array(grid_str).astype(int)
        self.drawn = np.zeros(self.grid.shape)
        self.won = False

    def get_grid(self):
        return self.grid

    def get_drawn(self):
        return self.drawn

    def add_draw(self, number):
        self.drawn[self.get_grid() == number] = 1

    def is_winner(self):
        (n_rows, n_cols) = self.grid.shape

        for ii in range(n_rows):
            if np.sum(self.drawn[ii, :]) == n_cols:
                self.won = True

        for jj in range(n_cols):
            if np.sum(self.drawn[:, jj]) == n_rows:
                self.won = True

        return self.won

    def get_sum_unmarked(self):
        return np.sum(self.get_grid()[self.get_drawn() == 0])

    def get_score(self, last_num: int):
        return last_num * self.get_sum_unmarked()

    def __str__(self):
        return str(self.get_grid()) + "\n" + str(self.get_drawn())


class BingoGame:
    def __init__(self, init_numbers, init_boards):
        self.numbers = init_numbers
        boards_list = []
        for board_str in init_boards:
            board = BingoBoard(board_str)
            boards_list.append(board)
        self.boards = boards_list
        self.winner_list = []

    def get_boards(self):
        return self.boards

    def play(self):
        for num in self.numbers:
            for (bb, brd) in enumerate(self.boards):
                if not self.boards[bb].is_winner():
                    self.boards[bb].add_draw(num)

                    if self.boards[bb].is_winner():
                        winner_dict = {
                            "board": bb,
                            "number": num,
                            "score": self.boards[bb].get_score(num),
                        }
                        self.winner_list.append(winner_dict)

    def get_winner_list(self):
        return self.winner_list


def get_drawn_numbers(lines_in: List) -> List:
    """Returns drawn numbers in List"""

    return [int(val) for val in lines_in[0].strip().split(",")]


def get_boards(lines_in: List) -> List:
    """Returns BingoBoard List"""

    board_list = []
    make_new_board = False
    arr = None

    for line in lines_in:
        if line.startswith("\n") and line.endswith("\n"):
            if arr is not None:
                board_list.append(arr)
            make_new_board = True
        else:
            clean_line = line.strip().replace("  ", " ").split(" ")
            if make_new_board:
                arr = [clean_line]
                make_new_board = False
            elif arr is not None:
                arr.append(clean_line)

    return board_list


if __name__ == "__main__":
    with open("inputs/input04.txt") as infile:
        user_input = infile.readlines()

    numbers = get_drawn_numbers(lines_in=user_input)
    boards = get_boards(lines_in=user_input)

    game = BingoGame(numbers, boards)
    game.play()
    winners = game.get_winner_list()

    first_winner = winners[0]
    last_winner = winners[-1]

    res1 = first_winner["score"]
    print(res1)

    res2 = last_winner["score"]
    print(res2)
