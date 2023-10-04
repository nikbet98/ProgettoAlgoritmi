from gridGraph import GridGraph
from plotGraph import graphPlotter

graph = GridGraph(2,5,0.6,0)

#graph.print_adj_list()
print(graph.__str__())
# commento
graphPlotter(graph)