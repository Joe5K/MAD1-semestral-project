import math
from copy import deepcopy

from numpy import random

NUMBER_OF_NODES = 300
M = 2

class Node:
    def __init__(self, number):
        self.weight = 0
        self.number = number

    def __str__(self):
        return f"Number {self.number}, weight {self.weight}"


class BAGraph:
    def __init__(self, m):
        self.edges = []
        self.nodes = {}
        self.current_number = self.m = m
        self.matrix = None
        self.floyd = None

    def get_node(self, number):
        if not self.nodes.get(number):
            self.nodes[number] = Node(number)
        return self.nodes[number]

    def generate_initial_graph(self):
        for i in range(self.m, 0, -1):
            for j in range(i):
                self.edges.append((self.get_node(i), self.get_node(j)))
                self.get_node(i).weight += 1
                self.get_node(j).weight += 1

    def check_duplicates(self):
        for i in self.edges:
            if (i[1], i[0]) in self.edges:
                raise Exception
        return

    def get_nodes_to_connect(self):
        numbers = []
        weights = []
        for i in self.nodes.values():
            numbers.append(i.number)
            weights.append(i.weight)
        delitel = sum(weights)
        weights = [i/delitel for i in weights]
        return random.choice(numbers, size=self.m, replace=False, p=weights)

    def add_node(self):
        self.current_number += 1
        new_node = self.get_node(self.current_number)
        for i in self.get_nodes_to_connect():
            self.edges.append((new_node, self.get_node(i)))
            self.get_node(i).weight += 1
        new_node.weight = self.m

    def to_csv(self):
        with open(f"n={NUMBER_OF_NODES}_m={M}.csv", "w") as ass:
            ass.write("\n".join([*["Source;Target"], *[f"{i[0].number};{i[1].number}" for i in self.edges]])+"\n")

    def to_matrix(self):
        data = []
        for (i, j) in self.edges:
            data.append((i.number, j.number))
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
            print(k)
            for i in range(V):
                for j in range(V):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

        self.floyd = dist

graph = BAGraph(M)
graph.generate_initial_graph()

for i in range(NUMBER_OF_NODES-M-1):
    graph.add_node()


graph.to_floyd()
pass