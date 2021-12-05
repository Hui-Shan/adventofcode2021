import pandas as pd

from typing import Dict


def get_rates(df_in: pd.DataFrame) -> Dict:
    most_common_binary = ""
    least_common_binary = ""

    for col in df_in.columns:
        counts = df_in[col].value_counts()
        ordered_bits = counts.index.to_list()

        most_common_bit = ordered_bits[0]
        least_common_bit = ordered_bits[-1]

        most_common_binary += str(most_common_bit)
        least_common_binary += str(least_common_bit)

    rates = {
        'gamma': most_common_binary,
        'epsilon': least_common_binary,
    }

    return rates


def compute_power_consumption(gamma_bin: str, epsilon_bin: str) -> int:
    gamma_decimal = int(gamma_bin, 2)
    epsilon_decimal = int(epsilon_bin, 2)

    return gamma_decimal * epsilon_decimal


def get_life_support_rating(df_in: pd.DataFrame) -> int:
    co2_rating_binary = get_rating(df_in, most=False)
    oxygen_rating_binary = get_rating(df_in, most=True)

    return int(co2_rating_binary, 2) * int(oxygen_rating_binary, 2)


def get_rating(df_in: pd.DataFrame, most: bool = True):

    if most:
        count_index = 0
    else:
        count_index = -1

    ordered_bits = df_in[0].value_counts().index.to_list()
    sel = df_in[0] == ordered_bits[count_index]
    ii = 1

    while sum(sel) > 1 and ii < len(df_in.columns):
        counts = df_in.loc[sel, ii].value_counts()
        ordered_bits = counts.index.to_list()
        bit_to_match = ordered_bits[count_index]
        if counts[0] == counts[-1]:
            if most:
                bit_to_match = '1'
            else:
                bit_to_match = '0'

        sel = sel & (df_in[ii] == bit_to_match)
        ii += 1

    return ''.join(df_in.loc[sel, ].values[0].tolist())


if __name__ == "__main__":

    with open("inputs\\input03") as infile:
        user_input = infile.readlines()

    df = pd.DataFrame()
    for number in user_input:
        split_number = list(number.strip())
        row = pd.DataFrame([split_number])

        if len(df) == 0:
            df = row
        else:
            df = pd.concat([df, row])

    rates_in = get_rates(df)

    res1 = compute_power_consumption(rates_in['gamma'], rates_in['epsilon'])
    print(res1)

    res2 = get_life_support_rating(df_in=df)
    print(res2)
