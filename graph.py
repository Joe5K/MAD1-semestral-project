from numpy import random


class Graph:
    def __init__(self):
        self.nodes_adjs = {}
        self.__shortest_path_matrix = None

    @property
    def shortest_path_matrix(self):
        if not self.__shortest_path_matrix:
            self.__shortest_path_matrix = [self._bfs(i) for i in range(len(self.nodes_adjs))]
        return self.__shortest_path_matrix

    def _bfs(self, src):
        queue = []
        visited = [False for _ in range(len(self.nodes_adjs))]
        pred = [-1 for _ in range(len(self.nodes_adjs))]
        dist = [1000000 for _ in range(len(self.nodes_adjs))]

        visited[src] = True
        dist[src] = 0
        queue.append(src)

        adj = self.nodes_adjs

        while len(queue) != 0:
            u = queue[0]
            queue.pop(0)
            for i in range(len(adj[u])):

                if not visited[adj[u][i]]:
                    visited[adj[u][i]] = True
                    dist[adj[u][i]] = dist[u] + 1
                    pred[adj[u][i]] = u
                    queue.append(adj[u][i])

        return dist

    def to_csv(self):
        edges = []
        for i, nodes in self.nodes_adjs.items():
            for j in nodes:
                if not (j, i) in edges:
                    edges.append((i, j))
        with open("out.csv", "w") as ass:
            ass.write("\n".join([*["Source;Target"], *[f"{i};{j}" for (i, j) in edges]]) + "\n")

    def load_csv(self):
        pass


class BAGraph(Graph):
    def __init__(self, m, number_of_nodes):
        super().__init__()
        self.current_number = self.m = m
        self.number_of_nodes = number_of_nodes
        self.average_distances = None

    def generate_initial_graph(self):
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
