import pickle
from agents import generate_paths
from gridGraph import GridGraph
from plotGraph import graphPlotter
from compito2 import ReachGoal, ReachGoal_variant
from heuristic import *
from state import State

goal = 7
initial_state = State(0, 0)
max_time = 100
# robot1 = [0,2,3]
# robot2 = [6,4,7]
# paths = []
# paths.append(robot1)
# paths.append(robot2)

graph = GridGraph(
    rows=10, cols=10, traversability_ratio=0.90, obstacle_agglomeration_ratio=0.5
)

paths = generate_paths(graph, max_time, num_paths=3)
print(paths)
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
# h = HeuristicRelaxPath(graph, goal)

# # h = DiagonalDistance(
# #     graph, goal, weigh_cardinal_direction=1, weight_diagonal_direction=2
# # )

# for i in range(0, 9):
#     print("nodo = ", i, "h = ", h(i))

# prova = ReachGoal_variant(graph, paths, initial_state, goal, max_time, h)
# print("print del risultato")
# print(prova)

# # disegna il grafico
graphPlotter(graph)
