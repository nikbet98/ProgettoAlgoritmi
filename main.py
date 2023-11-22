import pickle
from agents import Agents
from gridGraph import GridGraph
from plotGraph import graphPlotter
from search import ReachGoal, ReachGoal_variant
from heuristic import *
from problem import Problem
from state import State

def main():


    goal = 7
    max_time = 100

    pf4ea = Problem(
        rows=5,
        cols=5,
        traversability_ratio=0.90,
        obstacle_agglomeration_ratio=0.5,
        num_agents=2,
        maximum_time=5,
    )

    print(pf4ea.agent_paths)
    print("#---------------------#")
    print(pf4ea.grid)
 

    h = DiagonalDistance(
        pf4ea.grid, pf4ea.goal, weigh_cardinal_direction=1, weight_diagonal_direction=2
    )
    for i in range(pf4ea.grid.get_size()):
        print("nodo = ", i, " : ", "h = ", h(i))
    soluzione = ReachGoal(pf4ea, h)

    print(pf4ea.agent_paths)
    graphPlotter(pf4ea.grid)

  

if __name__ == "__main__":
    main()
