from graph import BAGraph

NUMBER_OF_NODES = 1000
M = 3

ba_graph = BAGraph(M, NUMBER_OF_NODES)
ba_graph.generate_initial_graph()

for i in range(NUMBER_OF_NODES - 1 - M):
    ba_graph.add_node()

ba_graph.to_csv()

