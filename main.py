import pickle
from gridGraph import GridGraph
from plotGraph import graphPlotter
from compito2 import ReachGoal, ReachGoal_variant
from heuristic import *
from state import State

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
h = HeuristicRelaxPath(graph,17)

prova = ReachGoal(graph, [], State(0,0),17, 100, h)
print(prova)
# disegna il grafico
graphPlotter(graph)

