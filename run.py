'''
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

'''

from tkinter import *
fields = ('Annual Rate', 'Number of Payments', 'Loan Principle', 'Monthly Payment', 'Remaining Loan')
def monthly_payment(entries):
   # period rate:
   r = (float(entries['Annual Rate'].get()) / 100) / 12
   print("r", r)
   # principal loan:
   loan = float(entries['Loan Principle'].get())
   n = float(entries['Number of Payments'].get())
   remaining_loan = float(entries['Remaining Loan'].get())
   q = (1 + r)** n
   monthly = r * ( (q * loan - remaining_loan) / ( q - 1 ))
   monthly = ("%8.2f" % monthly).strip()
   entries['Monthly Payment'].delete(0,END)
   entries['Monthly Payment'].insert(0, monthly )
   print("Monthly Payment: %f" % float(monthly))
def final_balance(entries):
   # period rate:
   r = (float(entries['Annual Rate'].get()) / 100) / 12
   print("r", r)
   # principal loan:
   loan = float(entries['Loan Principle'].get())
   n = float(entries['Number of Payments'].get())
   q = (1 + r)** n
   monthly = float(entries['Monthly Payment'].get())
   q = (1 + r)** n
   remaining = q * loan - ( (q - 1) / r) * monthly
   remaining = ("%8.2f" % remaining).strip()
   entries['Remaining Loan'].delete(0,END)
   entries['Remaining Loan'].insert(0, remaining )
   print("Remaining Loan: %f" % float(remaining))
def makeform(root, fields):
   entries = {}
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=22, text=field+": ", anchor='w')
      ent = Entry(row)
      ent.insert(0,"0")
      row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
      lab.pack(side = LEFT)
      ent.pack(side = RIGHT, expand = YES, fill = X)
      entries[field] = ent
   return entries
if __name__ == '__main__':
   root = Tk()
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e = ents: fetch(e)))
   b1 = Button(root, text = 'Final Balance',
      command=(lambda e = ents: final_balance(e)))
   b1.pack(side = LEFT, padx = 5, pady = 5)
   b2 = Button(root, text='Monthly Payment',
   command=(lambda e = ents: monthly_payment(e)))
   b2.pack(side = LEFT, padx = 5, pady = 5)
   b3 = Button(root, text = 'Quit', command = root.quit)
   b3.pack(side = LEFT, padx = 5, pady = 5)
   root.mainloop()