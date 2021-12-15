from __future__ import annotations

import numpy as np

from typing import List

from utils import get_time


class Node:
    def __init__(self, node_id: str, level: int):
        self.id = node_id
        self.level = level
        self.visited = False
        self.cost = np.Inf
        self.neighbors = []

    def set_neighbors(self, nodes: List[Node]):
        self.neighbors = nodes

    def get_unvisited_neighbors(self):
        return [item for item in self.neighbors if not item.visited]

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return "ID %s, Risk %i, Cost %s, Visited %s" % (
            self.id,
            self.level,
            str(self.cost),
            self.visited,
        )


class Network:
    def __init__(self, nodes: List[Node], start_node_id: str, end_node_id: str):
        self.nodes = {}
        for node in nodes:
            self.nodes[node.id] = node

        self.start_node = self.get_node(start_node_id)
        self.start_node.cost = 0

        self.end_node = self.get_node(end_node_id)

        self.candidates = [self.start_node]

    def reached_end_node(self):
        return self.end_node.cost < np.Inf

    def get_node(self, node_id: str):
        if node_id in self.nodes.keys():
            return self.nodes[node_id]
        else:
            return None

    def get_current_node(self):
        current_node = None
        if len(self.candidates) > 0:
            min_level = np.min([node.cost for node in self.candidates])
            current_node = [el for el in self.candidates if el.cost == min_level][0]

        return current_node

    def visit_next_node(self):
        cur_node = self.get_current_node()
        if cur_node is not None:
            for neigh in cur_node.get_unvisited_neighbors():
                if neigh.cost == np.Inf:  # Only update cost when it was not set before
                    neigh.cost = neigh.level + cur_node.cost
                    self.candidates.append(neigh)

            self.candidates.remove(cur_node)
            cur_node.set_visited()

    def full_dijkstra(self):
        while not self.reached_end_node():
            self.visit_next_node()

        return self.end_node.cost


def get_neighboring_ids(id_in: str, order: int):
    x = id_in[order:]
    y = id_in[:order]

    horizontal_neighbors = [y + str(int(x) + dx).zfill(order) for dx in [-1, 1]]
    vertical_neighbors = [str(int(y) + dy).zfill(order) + x for dy in [-1, 1]]

    return horizontal_neighbors + vertical_neighbors


def get_array_from_list(tile: List[str]) -> np.array:
    n_rows = len(tile)
    n_cols = len(tile[0].strip())

    array_out = np.zeros((n_rows, n_cols))
    for (tile_row, tile_line) in enumerate(tile):
        array_out[tile_row, :] = [int(el) for el in tile_line.strip()]

    return array_out.astype(int)


def get_big_array(array: np.array, factor: int = 5) -> np.array:
    array_out = np.zeros((factor * array.shape[0], factor * array.shape[1]))

    arrsize = array.shape[0]
    array_out[:arrsize, :arrsize] = array

    # horizontal expansion first
    array_ii = array
    for ii in range(1, factor):
        array_ii = np.add(array_ii, 1)
        array_ii[np.where(array_ii > 9)] = 1

        array_out[:arrsize, (arrsize * ii) : arrsize * (ii + 1)] = array_ii

    # vertical expansion
    array_jj = array_out[
        :arrsize,
    ]
    for jj in range(1, factor):
        array_jj = np.add(array_jj, 1)
        array_jj[np.where(array_jj > 9)] = 1

        array_out[(arrsize * jj) : arrsize * (jj + 1), :] = array_jj

    return array_out.astype(int)


def get_node_id(y: int, x: int, order: int):

    return str(y).zfill(order) + str(x).zfill(node_order)


if __name__ == "__main__":
    t0 = get_time()

    with open("inputs/input15.txt") as infile:
        puzzle_input = infile.readlines()

    test_input = [
        "1163751742",
        "1381373672",
        "2136511328",
        "3694931569",
        "7463417111",
        "1319128137",
        "1359912421",
        "3125421639",
        "1293138521",
        "2311944581",
    ]

    # Get nodes first
    input0 = [puzzle_input, test_input][0]
    node_order = int(np.floor(np.log10(len(input0[0])))) + 1

    node_list = []
    start_id = ""
    end_id = ""
    for row, line in enumerate(input0):
        stripped_line = line.strip()
        for col, lev in enumerate(stripped_line):
            nid = str(col).zfill(node_order) + str(row).zfill(node_order)

            new_node = Node(node_id=nid, level=int(lev))
            node_list.append(new_node)

            if row == 0 and col == 0:
                start_id = nid
            if row == len(input0) - 1 and col == len(stripped_line) - 1:
                end_id = nid

    network = Network(node_list, start_node_id=start_id, end_node_id=end_id)
    # Set neighbors
    for netnode in network.nodes.values():
        neighbor_ids = get_neighboring_ids(netnode.id, order=node_order)
        neighbor_nodes = []
        for id in neighbor_ids:
            neighbor = network.get_node(id)
            if neighbor is not None:
                neighbor_nodes.append(neighbor)
        netnode.set_neighbors(neighbor_nodes)

    res1 = network.full_dijkstra()
    print(f"Result part 1: {res1}")

    # Make 5 times as large grid
    node_list2 = []
    arr = get_array_from_list(input0)
    big = get_big_array(arr, factor=5)

    (nrows, ncols) = big.shape
    for ii in range(nrows):
        for jj in range(ncols):
            nid = get_node_id(ii, jj, order=node_order)

            new_node = Node(node_id=nid, level=big[ii, jj])
            node_list2.append(new_node)

            if ii == 0 and jj == 0:
                start_id = nid
            if ii == ncols - 1 and jj == nrows - 1:
                end_id = nid

    network2 = Network(node_list2, start_node_id=start_id, end_node_id=end_id)

    # Set neighbors
    for netnode in network2.nodes.values():
        neighbor_ids = get_neighboring_ids(netnode.id, order=node_order)
        neighbor_nodes = []
        for id in neighbor_ids:
            neighbor = network2.get_node(id)
            if neighbor is not None:
                neighbor_nodes.append(neighbor)
        netnode.set_neighbors(neighbor_nodes)

    res2 = network2.full_dijkstra()
    print(f"Result part 2: {res2}")
    print(f"Total runtime: {get_time() - t0}")
