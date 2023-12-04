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
import csv
import time
import repostitory
from utils import get_path_cost


COLS = "COLS"
ROW = "ROWS"
TRAVERSABILITY_RATIO = "TRAVERSABILITY_RATIO"
OBSTACLE_AGREGATION = "OBSTACLE_AGGLOMERATION"
NUM_AGENTS = "NUM_AGENTS"
MAXIMUM_TIME = "MAXIMUM_TIME"

file = "./csv/10x10_08_02_3_20 .csv"

config = repostitory.load_csv(file)
st_time = time.time()
pf4ea = Problem(int(config[ROW]),
                int(config[COLS]),
                float(config[TRAVERSABILITY_RATIO]),
                float(config[OBSTACLE_AGREGATION]),
                int(config[NUM_AGENTS]),
                int(config[MAXIMUM_TIME]))
print(pf4ea.print_info())
end_time = time.time()
generating_instance_time = end_time-st_time

st_time = time.time()
h = DiagonalDistance(pf4ea.grid, pf4ea.goal, 1, 2)
end_time = time.time()
heuristic_time = end_time - st_time

# repostitory.write_problem(pf4ea,h)

# problem, h = repostitory.read_problem("10x10_0.8_0.2_3_20_79_19")
st_time = time.time()
sol, open, closed, wait = ReachGoal(pf4ea,h)
end_time = time.time()
resolution_time = end_time - st_time
print(get_path_cost(sol, pf4ea.grid))
print(sol)

repostitory.write_result(pf4ea,
                         h,
                         [generating_instance_time,heuristic_time,resolution_time],
                         sol,
                         get_path_cost(sol,pf4ea.grid),
                         open,
                         closed,
                         wait)
graphPlotter(pf4ea.grid)


