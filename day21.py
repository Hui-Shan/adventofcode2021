from copy import deepcopy
from typing import List


class DeterministicDice:
    def __init__(self, n_sides: int):
        self.n_sides = n_sides
        self.num_rolls = 0

    def roll(self):
        self.num_rolls += 1
        value = self.num_rolls % self.n_sides
        if value == 0:
            value = 100
        return value


class Player:
    def __init__(self, id: int, init_pos: int):
        self.id = id
        self.pos = init_pos
        self.score = 0

    def roll_n_times(self, n: int, dice: DeterministicDice):
        num_steps = 0
        for ii in range(n):
            num_steps += dice.roll()
        self.move_n_steps(num_steps)

    def move_n_steps(self, num_steps: int):
        self.pos = (self.pos + num_steps) % 10
        if self.pos == 0:
            self.pos = 10

        self.score += self.pos

    def clone(self):
        p = Player(id=self.id, init_pos=self.pos)
        p.score = self.score
        return p


class DiracDice:
    def __init__(self, sides: int, endscore: int):
        self.sides = sides
        self.dirac_outcomes = self.get_dirac_outcomes()
        self.endscore = endscore
        self.lut = {}

    def get_dirac_outcomes(self):
        # initialize dict
        steps = {}
        for st in range(3, 10):
            steps[st] = 0

        # find combinations
        for ii in range(self.sides):
            for jj in range(self.sides):
                for kk in range(self.sides):
                    stepsum = (ii + 1) + (jj + 1) + (kk + 1)
                    steps[stepsum] += 1

        return steps

    def roll(self, p1: Player, p2: Player):
        wins = {1: 0, 2: 0}
        for (n_steps, freq) in self.dirac_outcomes.items():
            player = p1.clone()
            player.move_n_steps(n_steps)

            if player.score >= self.endscore:
                # wins[player.id] += freq
                wins[1] += freq
            else:
                try:
                    sub_wins = self.lut[(p2.pos, p2.score, player.pos, player.score)]
                except KeyError:
                    sub_wins = self.roll(p2, player)

                # wins[p1.id] += sub_wins[p2.id] * freq
                # wins[p2.id] += sub_wins[p1.id] * freq
                wins[1] += sub_wins[2] * freq
                wins[2] += sub_wins[1] * freq

        self.lut[(p1.pos, p1.score, p2.pos, p2.score)] = wins
        return wins


if __name__ == "__main__":
    with open("inputs/input21.txt") as infile:
        puzzle_input = infile.readlines()

    dd = DeterministicDice(100)

    player_list = []
    for line in puzzle_input:
        parts = line.strip().split(" ")
        pid = int(parts[1])
        pos = int(parts[-1])

        new_player = Player(pid, pos)
        player_list.append(new_player)

    # Example
    # p1 = Player(1, 4)
    # p2 = Player(2, 8)
    # player_list = [p1, p2]
    player_list2 = deepcopy(player_list)
    n_turns = 0

    end_score = 1000
    while all([p.score < end_score for p in player_list]):
        player = player_list[n_turns % len(player_list)]
        player.roll_n_times(3, dd)
        # print(f"Player {player.id}'s turn, pos: {player.pos} score: {player.score}")
        n_turns += 1

    losing_score = min([p.score for p in player_list])
    res1 = dd.num_rolls * losing_score
    print(res1)

    dd = DiracDice(sides=3, endscore=21)
    wins = dd.roll(player_list2[0], player_list2[1])
    print(wins)
    res2 = max(wins.values())
    print(res2)
