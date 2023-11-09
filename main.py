import pickle
from gridGraph import GridGraph
from plotGraph import graphPlotter
from compito2 import ReachGoal, ReachGoal_variant
from heuristic import *
from state import State

goal = 8
initial_state = State(0, 0)
max_time = 100
paths = []

graph = GridGraph(rows=3,cols= 3,traversability_ratio=1,obstacle_agglomeration_ratio=1)

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
h = HeuristicRelaxPath(graph, goal)

#h = DiagonalDistance(graph, goal,1,2)
for i in range(0, 9):
    print("nodo = ",i,"h = ",h(i))

prova = ReachGoal_variant(graph, paths, initial_state, goal, max_time, h)
print(prova)
# disegna il grafico
graphPlotter(graph)