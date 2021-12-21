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
        self.pos = (self.pos + num_steps) % 10
        if self.pos == 0:
            self.pos = 10

        self.score += self.pos


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
    n_turns = 0

    end_score = 1000
    while all([p.score < end_score for p in player_list]):
        player = player_list[n_turns % len(player_list)]
        player.roll_n_times(3, dd)
        print(f"Player {player.id}'s turn, pos: {player.pos} score: {player.score}")
        n_turns += 1

    losing_score = min([p.score for p in player_list])
    res1 = dd.num_rolls * losing_score
    print(res1)
