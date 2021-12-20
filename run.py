from numpy import random

NUMBER_OF_NODES = 1000
M = 3

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

    def get_node(self, number):
        if not self.nodes.get(number):
            self.nodes[number] = Node(number)
        return self.nodes[number]

    def generate_initial_graph(self):
        for i in range(self.m-1, 0, -1):
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


graph = BAGraph(M)
graph.generate_initial_graph()

for i in range(NUMBER_OF_NODES-M):
    graph.add_node()
print(graph)
