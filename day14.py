from typing import Dict, List, Tuple


class Polymer:
    def __init__(self, template: str, reactions: dict):
        self.template = template
        self.reactions = reactions

    def step(self):
        new_template = self.template[:1]
        for jj in range(len(self.template) - 1):
            pair = self.template[jj : jj + 2]
            insertion = self.reactions[pair]
            new_template += insertion + pair[1:]

        self.template = new_template

    def get_counts(self) -> List[tuple]:
        counts = []
        elements = set([el for el in self.template])

        for count_el in elements:
            count = len([el for el in self.template if el == count_el])
            counts.append((count_el, count))

        counts.sort(key=lambda x: x[1])

        return counts

    def get_difference_quantity_most_least(self):
        counts = self.get_counts()

        assert len(counts) >= 1, "Not enough elements to calculate the sum"

        return counts[-1][1] - counts[0][1]


class PolymerDict:
    def __init__(self, template: str, reactions: dict):
        self.reactions = reactions
        self.steps = 0

        self.letter_counts = {}
        self.pair_counts = self.get_zero_pair_counts()

        all_letters = []
        for jj in range(len(template) - 1):
            pair = template[jj : jj + 2]
            for letter in pair:
                if letter not in all_letters:
                    all_letters.append(letter)
            self.pair_counts[pair] += 1

        elements = set([el for el in template])
        for count_el in elements:
            count = len([el for el in template if el == count_el])
            self.letter_counts[count_el] = count

    def get_zero_pair_counts(self):
        zero_dict = {}
        for pair in self.reactions.keys():
            zero_dict[pair] = 0

        return zero_dict

    def step(self):
        new_pair_counts = self.get_zero_pair_counts()
        for (pair, count) in self.pair_counts.items():
            insertion = self.reactions[pair]
            if insertion in self.letter_counts.keys():
                self.letter_counts[insertion] += count
            else:
                self.letter_counts[insertion] = count

            new_pairs = [pair[:1] + insertion, insertion + pair[1:]]
            for new_pair in new_pairs:
                new_pair_counts[new_pair] += count

        self.pair_counts = new_pair_counts
        self.steps += 1

    def get_num_letters(self):

        return sum(self.letter_counts.values())

    def get_difference_quantity_most_least(self):
        counts = list(self.letter_counts.items())
        counts.sort(key=lambda x: x[1])

        return counts[-1][1] - counts[0][1]


def get_polymer_and_reactions(
    txt_input: List[str], split: str = " -> "
) -> Tuple[str, Dict[str, str]]:
    start = ""
    reactions = {}

    for line in txt_input:
        if split in line:
            key, value = line.strip().split(split)
            reactions[key] = value
        elif len(line.strip()) > 0:
            start = line.strip()

    return start, reactions


if __name__ == "__main__":
    with open("inputs/input14.txt") as infile:
        puzzle_input = infile.readlines()

    # puzzle_input = [
    #     "NNCB",
    #     "CH -> B",
    #     "HH -> N",
    #     "CB -> H",
    #     "NH -> C",
    #     "HB -> C",
    #     "HC -> B",
    #     "HN -> C",
    #     "NN -> C",
    #     "BH -> H",
    #     "NC -> B",
    #     "NB -> B",
    #     "BN -> B",
    #     "BB -> N",
    #     "BC -> B",
    #     "CC -> N",
    #     "CN -> C"
    # ]

    my_start, my_reactions = get_polymer_and_reactions(puzzle_input)

    poly = Polymer(my_start, my_reactions)

    for ii in range(10):
        poly.step()

    res1 = poly.get_difference_quantity_most_least()
    print(res1)

    poly2 = PolymerDict(my_start, my_reactions)

    for ii in range(40):
        poly2.step()

    res2 = poly2.get_difference_quantity_most_least()
    print(res2)
