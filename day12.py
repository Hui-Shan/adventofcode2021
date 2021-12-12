import copy

from typing import List


class Node:
    def __init__(self, name: str):
        self.name = name
        self.neighbors = []

    def set_neighbors(self, neighbors: List):
        self.neighbors = neighbors

    def __str__(self):
        return self.name


class Path:
    def __init__(self, nodes: List, cant_visit: List):
        self.nodes = nodes
        self.cant_visit = cant_visit
        self.has_ended = False

    def can_visit(self, node: Node) -> bool:
        visited_names = [el.name for el in self.cant_visit]
        visiting_okay = node.name not in visited_names

        return visiting_okay

    def get_last_node(self) -> Node:
        return self.nodes[-1]

    def visit_node(self, node: Node):
        self.nodes.append(node)
        if node.name == node.name.lower():
            self.cant_visit.append(node)

    def __copy__(self):
        return Path(nodes=list(self.nodes), cant_visit=list(self.cant_visit))

    def __str__(self):
        return "-".join([node.name for node in self.nodes])


class Path2(Path):
    def __init__(self, nodes: List, cant_visit: List, twice_visited_cave: Node = None):
        super().__init__(nodes, cant_visit)
        self.twice_visited_cave = twice_visited_cave

    def can_visit(self, node: Node) -> bool:
        visited_names = [el.name for el in self.cant_visit]
        visiting_okay = False

        if node.name == "start":
            return False

        if node.name in visited_names:
            if self.twice_visited_cave is None:
                visiting_okay = True
        else:
            visiting_okay = True

        return visiting_okay

    def visit_node(self, node: Node):
        self.nodes.append(node)
        if node.name == node.name.lower():
            if node in self.cant_visit:
                if self.twice_visited_cave is None:
                    self.twice_visited_cave = node
            else:
                self.cant_visit.append(node)

    def __copy__(self):
        return Path2(
            nodes=list(self.nodes),
            cant_visit=list(self.cant_visit),
            twice_visited_cave=self.twice_visited_cave,
        )


def get_unique_node_names(lines: List) -> set:
    all_nodes = []
    for line in lines:
        line_nodes = line.strip().split("-")
        all_nodes.extend(line_nodes)

    return set(all_nodes)


def get_neighbor_nodes(lines: List, node_name: str) -> List:
    neighbors = []
    for line in lines:
        line_nodes = line.strip().split("-")
        if line_nodes[0] == node_name:
            neighbors.append(line_nodes[1])
        elif line_nodes[1] == node_name:
            neighbors.append(line_nodes[0])
    return neighbors


if __name__ == "__main__":
    with open("inputs/input12.txt") as infile:
        user_input = infile.readlines()

    test_input = ["start-A", "start-b", "A-c", "A-b", "b-d", "A-end", "b-end"]

    the_input = [user_input, test_input][0]

    node_set = set()
    unique_node_names = get_unique_node_names(the_input)

    for name in unique_node_names:
        new_node = Node(name)
        node_set.add(new_node)

    for node in node_set:
        neighbor_names = get_neighbor_nodes(the_input, node.name)

        neighbor_nodes = []
        for nname in neighbor_names:
            found_neighbor = [node for node in node_set if node.name == nname][0]
            neighbor_nodes.append(found_neighbor)

        node.set_neighbors(neighbor_nodes)

    start_node = [node for node in node_set if node.name == "start"][0]

    for ii in [1, 2]:
        print(f"Part {ii}")
        if ii == 1:
            paths_to_check = [Path([start_node], [start_node])]
        else:
            paths_to_check = [Path2([start_node], [start_node])]

        completed_paths = []

        while len(paths_to_check) > 0:
            new_paths = []
            for prev_path in paths_to_check:
                last_node = prev_path.get_last_node()
                for neigh in last_node.neighbors:
                    if prev_path.can_visit(neigh):
                        new_path = copy.copy(prev_path)  # copy.deepcopy(prev_path)
                        new_path.visit_node(neigh)
                        if neigh.name == "end":
                            if str(new_path) not in completed_paths:
                                completed_paths.append(str(new_path))
                        else:
                            new_paths.append(new_path)

            paths_to_check = [path for path in new_paths if path.has_ended is False]
            print(len(completed_paths))

        res = len(completed_paths)
        print(f"result {ii}: {res}")
