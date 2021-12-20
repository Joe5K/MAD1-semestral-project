import math

from numpy import random, mean


class Graph:
    def __init__(self):
        self.nodes_adjs = {}
        self.__shortest_path_matrix = None

    @property
    def average(self):
        maximum_distance = 0
        for i in self.shortest_path_matrix:
            if max(i) > maximum_distance:
                maximum_distance = max(i)
        return maximum_distance

    @property
    def degrees_distribution_str(self):
        return "{"+", ".join([f"{i}: {j}" for (i, j) in sorted(list(self.degrees_distribution.items()), key=lambda x: x[0], reverse=True)])+"}"

    @property
    def degrees_distribution(self):
        _degrees_distribution = {}
        for i in self.degrees.values():
            _degrees_distribution[i] = _degrees_distribution.get(i, 0) + 1
        for i in range(max(_degrees_distribution.keys())):
            if not _degrees_distribution.get(i):
                _degrees_distribution[i] = 0
        return _degrees_distribution


    @property
    def average_degree(self):
        return mean(list(self.degrees.values()))

    @property
    def degrees(self):
        return {i: len(j) for i, j in self.nodes_adjs.items()}

    @property
    def closeness_centrality(self):
        return [round(1/i, 3) for i in self.average_distances]

    @property
    def average_distances(self):
        return [sum(i)/(len(i)-1) for i in self.shortest_path_matrix]

    @property
    def shortest_path_matrix(self):
        if not self.__shortest_path_matrix:
            self.__shortest_path_matrix = [self._bfs(i) for i in range(len(self.nodes_adjs))]
        return self.__shortest_path_matrix

    def _bfs(self, src):
        visited = [False] * len(self.nodes_adjs)
        dist = [math.inf] * len(self.nodes_adjs)

        visited[src] = True
        dist[src] = 0
        queue = [src]

        while len(queue) != 0:
            u = queue[0]
            queue.pop(0)
            for i in self.nodes_adjs[u]:
                if not visited[i]:
                    visited[i] = True
                    dist[i] = dist[u] + 1
                    queue.append(i)
            if math.inf not in dist:
                break

        return dist

    def save_csv(self, filename):
        edges = []
        for i, nodes in self.nodes_adjs.items():
            for j in nodes:
                if not (j, i) in edges:
                    edges.append((i, j))
        with open(filename, "w") as ass:
            ass.write("\n".join([*["Source;Target"], *[f"{i};{j}" for (i, j) in edges]]) + "\n")

    def load_csv(self, filename):
        with open(filename, "r") as ass:
            for line in ass.readlines()[1:]:
                (i, j) = line.replace("\n", "").split(";")
                (i, j) = (int(i), int(j))
                self.nodes_adjs[i] = [*self.nodes_adjs.get(i, []), *[j]]
                self.nodes_adjs[j] = [*self.nodes_adjs.get(j, []), *[i]]


class BAGraph(Graph):
    def __init__(self, m, number_of_nodes):
        super().__init__()
        self.current_number = self.m = m
        self.number_of_nodes = number_of_nodes

    def generate_initial_subgraph(self):
        for i in range(self.m, 0, -1):
            for j in range(i):
                self.nodes_adjs[i] = [*self.nodes_adjs.get(i, []), *[j]]
                self.nodes_adjs[j] = [*self.nodes_adjs.get(j, []), *[i]]

    def get_nodes_to_connect(self):
        numbers = []
        weights = []
        for i, j in self.nodes_adjs.items():
            numbers.append(i)
            weights.append(len(j))
        factor = sum(weights)
        weights = [i / factor for i in weights]
        return random.choice(numbers, size=self.m, replace=False, p=weights)

    def add_node(self):
        self.current_number += 1
        nodes_to_connect = self.get_nodes_to_connect()
        for i in nodes_to_connect:
            self.nodes_adjs[i].append(self.current_number)
        self.nodes_adjs[self.current_number] = list(nodes_to_connect)
