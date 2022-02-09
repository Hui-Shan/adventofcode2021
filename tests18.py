import unittest

from day18 import SnailFishNumber, sum_snailfishnumber_str_list


class MyTestCase(unittest.TestCase):
    def test_magnitudes(self):
        magnitude_examples = {
            "[[1,2],[[3,4],5]]": 143,
            "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]": 1384,
            "[[[[1,1],[2,2]],[3,3]],[4,4]]": 445,
            "[[[[3,0],[5,3]],[4,4]],[5,5]]": 791,
            "[[[[5,0],[7,4]],[5,5]],[6,6]]": 1137,
            "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]": 3488,
            "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]": 4140,
        }

        res = []
        expected = list(magnitude_examples.values())
        for string in magnitude_examples.keys():
            snf_mag = SnailFishNumber.from_string(string).magnitude()
            res.append(snf_mag)

        self.assertEqual(res, expected)

    def test_explode(self):
        explode_examples = {
            "[[[[[9,8],1],2],3],4]": "[[[[0,9],2],3],4]",
            "[7,[6,[5,[4,[3,2]]]]]": "[7,[6,[5,[7,0]]]]",
            "[[6,[5,[4,[3,2]]]],1]": "[[6,[5,[7,0]]],3]",
            "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]": "[[3,[2,[8,0]]],[9,[5,[7,0]]]]",
        }

        results = []
        expected = list(explode_examples.values())
        for str_in in explode_examples.keys():
            snf_in = SnailFishNumber.from_string(str_in)
            snf_out = snf_in.explode()
            res = str(snf_out)
            results.append(res)

        self.assertEqual(expected, results)  # add assertion here

    def test_addition1(self):
        str1 = "[[[[4,3],4],4],[7,[[8,4],9]]]"
        num1 = SnailFishNumber.from_string(str1)

        str2 = "[1,1]"
        num2 = SnailFishNumber.from_string(str2)

        num_sum = num1 + num2

        str_exp = "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
        exp_sum = SnailFishNumber.from_string(str_exp)

        self.assertEqual(str(num_sum), str(exp_sum))

    def test_addition2(self):
        ii = 2
        el_list = [
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
            "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
            "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
            "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
            "[7,[5,[[3,8],[1,4]]]]",
            "[[2,[2,2]],[8,[8,1]]]",
            "[2,9]",
            "[1,[[[9,3],9],[[9,0],[0,7]]]]",
            "[[[5,[7,4]],7],1]",
            "[[[[4,2],2],6],[8,7]]",
        ]

        res = sum_snailfishnumber_str_list(el_list[:ii])
        exp_str = [
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
            "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
            "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]",
            "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
        ]

        self.assertEqual(exp_str[ii - 1], str(res))

    def test_addition3(self):
        el_list = [
            "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]",
            "[[[5,[2,8]],4],[5,[[9,9],0]]]",
            "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]",
            "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]",
            "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]",
            "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]",
            "[[[[5,4],[7,7]],8],[[8,3],8]]",
            "[[9,3],[[9,9],[6,[4,9]]]]",
            "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]",
            "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]",
        ]

        res_str = str(sum_snailfishnumber_str_list(el_list))

        exp_str = "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"

        self.assertEqual(exp_str, res_str)


if __name__ == "__main__":
    unittest.main()
