from __future__ import annotations

_mapping = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

number_map = {4: "literal"}

key_map = {v: k for (k, v) in number_map.items()}

_head_len = 6
_chunk_len = 5
_digit_len = 15
_num_len = 11


class Packet:
    def __init__(self, version: int, packet_id: id, literal: str = None):
        self.version = version
        self.packet_id = packet_id
        self.literal = literal
        self.subpackets = []

    def add_subpacket(self, subpacket: Packet):
        self.subpackets.append(subpacket)

    def set_literal(self, literal: int):
        self.literal = literal

    def is_literal(self):
        return self.packet_id == key_map["literal"]

    def get_value(self):
        binary_value = ""
        num_chunks = int(len(self.literal) / _chunk_len)
        for ii in range(num_chunks):
            binary_value += self.literal[_chunk_len * ii + 1 : _chunk_len * (ii + 1)]

        return int(binary_value, 2)

    def get_version_sum(self):
        version_sum = self.version
        for packet in self.subpackets:
            version_sum += packet.get_version_sum()

        return version_sum

    def __str__(self):
        if self.is_literal():
            value = f"Literal: {self.get_value()}"
        else:
            value = f"Subpackets: {[str(el) for el in self.subpackets]}"

        return f"Version: {self.version} Id: {self.packet_id}, {value}"


def get_binary(hexadecimal_rep: str) -> str:
    binary_rep = ""
    for char in hexadecimal_rep:
        binary_rep += _mapping[char]

    return binary_rep


def get_packet_and_rest(binary_rep: str) -> (Packet, str):

    version = int(binary_rep[: int(_head_len / 2)], 2)
    pack_id = int(binary_rep[int(_head_len / 2) : _head_len], 2)

    packet = Packet(version=version, packet_id=pack_id)

    if packet.is_literal():
        n = 0
        while binary_rep[_head_len:][_chunk_len * n] == "1":
            n = n + 1

        threshold = _head_len + _chunk_len * (n + 1)

        literal = binary_rep[_head_len:threshold]
        packet.set_literal(literal)
        rest = binary_rep[threshold:]
    else:
        length_type_id = binary_rep[_head_len]
        if length_type_id == "0":
            subpack_length = int(
                binary_rep[_head_len + 1 : _head_len + _digit_len + 1], 2
            )
            threshold = _head_len + _digit_len + subpack_length + 1
            rest = binary_rep[threshold:]

            subpackets = binary_rep[_head_len + _digit_len + 1 : threshold]
            subpacket, subrest = get_packet_and_rest(subpackets)
            while len(subrest) > 0:
                packet.add_subpacket(subpacket)
                subpacket, subrest = get_packet_and_rest(subrest)
            packet.add_subpacket(subpacket)
        else:
            subpack_num = int(binary_rep[_head_len + 1 : _head_len + _num_len + 1], 2)

            subrest = binary_rep[_head_len + _num_len + 1 :]
            for ii in range(subpack_num):
                subpacket, subrest = get_packet_and_rest(subrest)
                packet.add_subpacket(subpacket)
            rest = subrest

    return packet, rest


if __name__ == "__main__":
    with open("inputs/input16.txt") as infile:
        puzzle_input = infile.readline().strip()

    # test = {
    #     "D2FE28": 2021,
    #     "38006F45291200": [10, 20],
    #     "EE00D40C823060": [1, 2, 3],
    #     "8A004A801A8002F478": "",
    #     "620080001611562C8802118E34": "",
    #     "C0015000016115A2E0802F182340": "",
    #     "A0016C880162017C3686B18A3D4780": ""
    # }
    #
    # for test_in, test_out in test.items():
    #     print(f"Case: {test_in} >> {test_out}")
    #     packet, rest = get_packet_and_rest(get_binary(test_in))
    #     print(packet)

    rest = get_binary(puzzle_input)

    packet, rest = get_packet_and_rest(rest)
    res1 = packet.get_version_sum()
    print(res1)
