from graph import BAGraph
from helpers import generate_form

if __name__ == '__main__':
    '''m = 5
    number_of_nodes = 10000
    ba_graph = BAGraph(m, number_of_nodes)
    ba_graph.generate_initial_subgraph()

    for i in range(number_of_nodes - 1 - m):
        ba_graph.add_node()
        print(i)

    ba_graph.save_csv("madcv.csv")'''
    generate_form().mainloop()