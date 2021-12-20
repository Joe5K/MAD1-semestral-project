import math
from copy import deepcopy

from numpy import random

NUMBER_OF_NODES = 300
M = 3


class BAGraph:
    def __init__(self, m):

        self.edges = []
        self.nodes = {}
        self.current_number = self.m = m
        self.nodes_dict = {}
        self.matrix = None
        self.floyd = None
        self.average_distances = None
        self._shortest_path_graph = None

    def get_node_weight(self, number):
        if not self.nodes.get(number):
            self.nodes[number] = number
        return self.nodes[number]

    def generate_initial_graph(self):
        for i in range(self.m, 0, -1):
            for j in range(i):
                self.edges.append((i, j))
                self.nodes[i] = self.nodes.get(i, 0) + 1
                self.nodes[i] = self.nodes.get(j, 0) + 1
                self.nodes_dict[i] = [*self.nodes_dict.get(i, []), *[j]]
                self.nodes_dict[j] = [*self.nodes_dict.get(j, []), *[i]]

    def check_duplicates(self):
        for i in self.edges:
            if (i[1], i[0]) in self.edges:
                raise Exception
        return

    def get_nodes_to_connect(self):
        numbers = []
        weights = []
        for i, j in self.nodes.items():
            numbers.append(i)
            weights.append(j)
        delitel = sum(weights)
        weights = [i / delitel for i in weights]
        return random.choice(numbers, size=self.m, replace=False, p=weights)

    def add_node(self):
        self.current_number += 1
        nodes_to_connect = self.get_nodes_to_connect()
        for i in nodes_to_connect:
            self.edges.append((self.current_number, i))
            self.nodes[i] += 1
            self.nodes_dict[i].append(self.current_number)
        self.nodes[self.current_number] = self.m
        self.nodes_dict[self.current_number] = list(nodes_to_connect)

    def to_csv(self):
        with open(f"n={NUMBER_OF_NODES}_m={M}.csv", "w") as ass:
            ass.write("\n".join([*["Source;Target"], *[f"{i[0].number};{i[1].number}" for i in self.edges]]) + "\n")

    def to_matrix(self):
        data = []
        for (i, j) in self.edges:
            data.append((i, j))
        matrix = [[math.inf for _ in range(NUMBER_OF_NODES)] for __ in range(NUMBER_OF_NODES)]

        for (i, j) in data:
            matrix[i][j] = 1
            matrix[j][i] = 1
        self.matrix = matrix

    def to_floyd(self):
        if not self.matrix:
            self.to_matrix()
        V = len(self.matrix)
        dist = deepcopy(self.matrix)

        for k in range(V):
            #print(k)
            for i in range(V):
                for j in range(V):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
            dist[k][k]=0

        self.floyd = dist

    @property
    def shortest_path_graph(self):
        if not self._shortest_path_graph:
            self._shortest_path_graph = [self.BFS(i) for i in range(NUMBER_OF_NODES)]
        return self._shortest_path_graph


    def BFS(self, src):
        queue = []
        visited = [False for i in range(NUMBER_OF_NODES)]
        pred = [-1 for i in range(NUMBER_OF_NODES)]
        dist = [1000000 for i in range(NUMBER_OF_NODES)]

        visited[src] = True
        dist[src] = 0
        queue.append(src)

        adj = self.nodes_dict

        # standard BFS algorithm
        while (len(queue) != 0):
            u = queue[0]
            queue.pop(0)
            for i in range(len(adj[u])):

                if (visited[adj[u][i]] == False):
                    visited[adj[u][i]] = True
                    dist[adj[u][i]] = dist[u] + 1
                    pred[adj[u][i]] = u
                    queue.append(adj[u][i])

                    # We stop BFS when we find
                    # destination.
        return dist

    # utility function to print the shortest distance
    # between source vertex and destination vertex


graph = BAGraph(M)
graph.generate_initial_graph()

for i in range(NUMBER_OF_NODES - M - 1):
    graph.add_node()


graph.to_floyd()
b = graph.floyd
print(graph.shortest_path_graph==b)
