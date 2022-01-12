from random import randint


class Graph:
    def __init__(self):
        self.nodes_adjs = {}
        self._shortest_path_matrix = None
        self.has_changed = True

    @property
    def average(self):
        maximum_distance = 0
        for i in self.shortest_path_matrix:
            if max(i) > maximum_distance:
                maximum_distance = max(i)
        return maximum_distance

    @property
    def degrees_distribution_str(self):
        return "\n".join([f"Degree {i}: {j} nodes" for (i, j) in sorted(list(self.degrees_distribution.items()), key=lambda x: x[0], reverse=True)])

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
        degrees_list = list(self.degrees.values())
        return sum(degrees_list)/len(degrees_list)

    @property
    def nodes_data_str(self):
        degrees = [i[1] for i in sorted(list(self.degrees.items()), key=lambda x: x[0], reverse=False)]

        output_data = []
        for index, (degree, average_distance, closeness_centrality) in enumerate(zip(degrees, self.average_distances, self.closeness_centrality)):
            output_data.append(f"{index+1}. node has degree of {degree}, average distance is {round(average_distance, 2)} and closeness centrality is {round(closeness_centrality, 2)}")
        return "\n".join(output_data)

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
    def shortest_path_matrix_str(self):
        return "\n".join([str(i) for i in self.shortest_path_matrix])

    @property
    def shortest_path_matrix(self):
        if self.has_changed or not self._shortest_path_matrix:
            self._shortest_path_matrix = [self._bfs(i) for i in list(self.nodes_adjs.keys())]
            self.has_changed = False
        return self._shortest_path_matrix

    def _bfs(self, src):
        inf = float("inf")
        dist = {i: inf for i in self.nodes_adjs.keys()}

        dist[src] = 0
        queue = [src]

        while queue:
            u = queue[0]
            queue.pop(0)
            for i in self.nodes_adjs[u]:
                if dist[i] == inf:
                    dist[i] = dist[u] + 1
                    queue.append(i)
            if inf not in dist.values():
                break

        return list(dist.values())

    def save_csv(self, filename):
        edges = []
        for i, nodes in self.nodes_adjs.items():
            for j in [k for k in nodes if k > i]:
                edges.append((i, j))

        with open(filename, "w") as ass:
            ass.write("\n".join([*["Source;Target"], *[f"{i};{j}" for (i, j) in edges]]) + "\n")

    def load_csv(self, filename):
        warning = False
        with open(filename, "r") as ass:
            for line in ass.readlines():
                (i, j) = line.replace("\n", "").split(";")
                if not i.isnumeric() or not j.isnumeric():
                    continue
                (i, j) = (int(i), int(j))
                
                if not self.nodes_adjs.get(i) or j not in self.nodes_adjs.get(i):
                    self.nodes_adjs[i] = [*self.nodes_adjs.get(i, []), j]
                else:
                    warning = True

                if not self.nodes_adjs.get(j) or i not in self.nodes_adjs.get(j):
                    self.nodes_adjs[j] = [*self.nodes_adjs.get(j, []), i]
                else:
                    warning = True
        if warning:
            print("Loaded CSV contains some duplicates which have been filtered, this may cause inconsistency")

    def save_graph_analysis(self, filename):
        with open(filename, "w") as ass:
            ass.write(
        f"""Graph has average of {self.average}
The average degree is {self.average_degree}
The degree distribution is:
{self.degrees_distribution_str}
Data:
{self.nodes_data_str}

-------------------------------------------------------------------------------------
The shortest path matrix is:
{self.shortest_path_matrix_str}
""")


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
        random_pick_list = []
        for i, j in self.nodes_adjs.items():
            random_pick_list.extend([i for _ in range(len(j))])
        nodes_to_connect = []
        while len(nodes_to_connect) != self.m:
            picked_node = random_pick_list[randint(0, len(random_pick_list)-1)]
            if picked_node not in nodes_to_connect:
                nodes_to_connect.append(picked_node)
        return nodes_to_connect

    def add_node(self):
        self.current_number += 1
        nodes_to_connect = self.get_nodes_to_connect()
        for i in nodes_to_connect:
            self.nodes_adjs[i].append(self.current_number)
        self.nodes_adjs[self.current_number] = list(nodes_to_connect)
        self.has_changed = True
