import pickle
from agents import Agents
from gridGraph import GridGraph
from plotGraph import graphPlotter
from search import ReachGoal, ReachGoal_variant
from heuristic import *
from problem import Problem
from state import State
from memory_profiler import profile
import cProfile

pf4ea = Problem(
        rows=500,
        cols=500,
        traversability_ratio=0.50,
        obstacle_agglomeration_ratio=0.005,
        num_agents=0,
        maximum_time=5,
    )

graphPlotter(pf4ea.grid)