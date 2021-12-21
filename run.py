from graph import BAGraph, Graph

NUMBER_OF_NODES = 1000
M = 4

ba_graph = BAGraph(M, NUMBER_OF_NODES)
ba_graph.generate_initial_subgraph()

for i in range(NUMBER_OF_NODES - 1 - M):
    ba_graph.add_node()

ba_graph.save_csv("graph.csv")
# print(ba_graph.average_degree)

loaded_graph = Graph()
loaded_graph.load_csv("graph.csv")

with open("text_output.txt", "w") as ass:
    ass.write(
        f"""Graph has average of {loaded_graph.average}
The average degree is {loaded_graph.average_degree}
The degree distribution is: 
{loaded_graph.degrees_distribution_str}
Data:
{loaded_graph.nodes_data_str}

-------------------------------------------------------------------------------------
The shortest path matrix is:
{loaded_graph.shortest_path_matrix_str} 

    """)
