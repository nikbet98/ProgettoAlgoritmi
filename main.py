import pickle
from gridGraph import GridGraph
from plotGraph import graphPlotter
from utils import dijkstra

graph = GridGraph(3,6,0.6,0.2)

# stampo su terminale la griglia
print(graph)

# salvo la griglia su file
"""
with open('graph.pickle', 'wb') as f:
    pickle.dump(graph, f)
    f.close()
"""

# leggo il grafico da file
# f = open('graph.pickle', 'rb')
# graph = pickle.load(f)
# f.close()

# print(graph)

dijkstra(graph, 0)

# disegna il grafico
graphPlotter(graph)