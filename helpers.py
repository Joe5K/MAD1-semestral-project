from enum import Enum

from graph import BAGraph, Graph
from tkinter import *


def open_file(filepath):
    import subprocess, os, platform
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(filepath)
    else:  # linux variants
        subprocess.call(('xdg-open', filepath))


class BAGraphGUIEnum(Enum):
    NUMBER_OF_NODES = "Number of nodes"
    M = "m"
    FILENAME = "Generated graph filename"


class AnalysysGraphGUIEnum(Enum):
    GRAPH_FILENAME = "Analysis graph filename"
    OUTPUT_FILENAME = "Analysys graph text output filename"


def generate_form():
    fields = *(i.value for i in BAGraphGUIEnum), "break", *(i.value for i in AnalysysGraphGUIEnum)

    def generate_graph(entries):
        number_of_nodes = int(entries[BAGraphGUIEnum.NUMBER_OF_NODES.value].get())
        m = int(entries[BAGraphGUIEnum.M.value].get())
        filename = entries[BAGraphGUIEnum.FILENAME.value].get()

        ba_graph = BAGraph(m, number_of_nodes)
        ba_graph.generate_initial_subgraph()

        for i in range(number_of_nodes - 1 - m):
            ba_graph.add_node()

        ba_graph.save_csv(filename)
        if checkbox_var.get():
            open_file(filename)

    def analyse_graph(entries):
        graph_filename = entries[AnalysysGraphGUIEnum.GRAPH_FILENAME.value].get()
        analysis_filename = entries[AnalysysGraphGUIEnum.OUTPUT_FILENAME.value].get()

        loaded_graph = Graph()
        loaded_graph.load_csv(graph_filename)
        loaded_graph.save_graph_analysis(analysis_filename)
        if checkbox_var.get():
            open_file(analysis_filename)

    def makeform(root, fields):
        entries = {}
        for field in fields:
            if field == "break":
                row = Frame(root)
                lab = Label(row, width=53, text="_" * 100, anchor='w')
                lab.pack(side=LEFT)
                row.pack(side=TOP, fill=X, padx=5, pady=5)
                lab.pack(side=LEFT)
                continue
            row = Frame(root)
            lab = Label(row, width=30, text=field, anchor='w')
            ent = Entry(row)
            if field == BAGraphGUIEnum.NUMBER_OF_NODES.value:
                ent.insert(0, "1000")
            elif field == BAGraphGUIEnum.M.value:
                ent.insert(0, "4")
            elif field == BAGraphGUIEnum.FILENAME.value or field == AnalysysGraphGUIEnum.GRAPH_FILENAME.value:
                ent.insert(0, "graph.txt")
            elif field == AnalysysGraphGUIEnum.OUTPUT_FILENAME.value:
                ent.insert(0, "text_output.txt")
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries[field] = ent
        return entries


    root = Tk()
    ents = makeform(root, fields)
    lab = Label(root, width=8, text="Open files", anchor='w')
    lab.pack(side=LEFT, padx=5, pady=5)
    checkbox_var = IntVar(value=1)
    checkbox = Checkbutton(root, variable=checkbox_var)
    checkbox.pack(side=LEFT, padx=5, pady=5)
    b1 = Button(root, text='Generate graph',
                command=(lambda e=ents: generate_graph(e)))
    b1.pack(side=LEFT, padx=5, pady=5)
    b2 = Button(root, text='Analyse graph',
                command=(lambda e=ents: analyse_graph(e)))
    b2.pack(side=LEFT, padx=5, pady=5)
    b3 = Button(root, text='Quit', command=root.quit)
    b3.pack(side=LEFT, padx=5, pady=5)
    return root