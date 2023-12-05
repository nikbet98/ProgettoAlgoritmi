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
import repository
from utils import get_path_cost

COLS = "COLS"
ROW = "ROWS"
TRAVERSABILITY_RATIO = "TRAVERSABILITY_RATIO"
OBSTACLE_AGREGATION = "OBSTACLE_AGGLOMERATION"
NUM_AGENTS = "NUM_AGENTS"
MAXIMUM_TIME = "MAXIMUM_TIME"
WEIGHT_CARDINAL_DIRECTION = 1
WEIGHT_DIAGONAL_DIRECTION = math.sqrt(2)

# file = "./csv/100x100_08_02_10_100.csv"
# file = "./csv/10x10_08_02_3_20 .csv"
# file = "./csv/1000x100_08_01_25_750.csv"
file = "./csv/10x10_1_1_30_30.csv"


def main():
    # leggiamo la configurazione da file
    # config = repository.load_csv(file)
    # generiamo il problema
    # pf4ea, generating_instance_time = generate_instance(config)
    # salvo il problema file
    # repository.write_problem(pf4ea)
    # carico il problema da file
    pf4ea = repository.read_problem("25x25_0.6_0.1_30_50_233_199")
    # calcoliamo l'euristica
    h, heuristic_time = generate_heuristic(pf4ea, 1)
    # troviamo la soluzione
    sol, open_list, closed_list, wait, resolution_time = search_solution(pf4ea, h, 1)
    # salva il risultato (se ho generato tutto da 0)
    # save_result(pf4ea, h, [generating_instance_time, heuristic_time, resolution_time], sol,
    #            get_path_cost(sol, pf4ea.grid), open_list, closed_list, wait)
    # salva il risultato (se ho caricato il problema)
    save_result(pf4ea, h, [0, heuristic_time, resolution_time], sol,
                get_path_cost(sol, pf4ea.grid), open_list, closed_list, wait)
    graphPlotter(pf4ea.grid)


# repository.write_problem(pf4ea,h)

# problem, h = repository.read_problem("10x10_0.8_0.2_3_20_79_19")


def generate_instance(config):
    st_time = time.time()
    pf4ea = Problem(int(config[ROW]),
                    int(config[COLS]),
                    float(config[TRAVERSABILITY_RATIO]),
                    float(config[OBSTACLE_AGREGATION]),
                    int(config[NUM_AGENTS]),
                    int(config[MAXIMUM_TIME]))
    end_time = time.time()
    elapsed_time = end_time - st_time
    return pf4ea, elapsed_time


def generate_heuristic(problem: Problem, type: int):
    # type 0: Diagonal Distance
    if type == 0:
        st_time = time.time()
        h = DiagonalDistance(problem.grid, problem.goal, WEIGHT_CARDINAL_DIRECTION, WEIGHT_DIAGONAL_DIRECTION)
        end_time = time.time()
    else:
        # type != 0: Relaxed path
        st_time = time.time()
        h = HeuristicRelaxPath(problem.grid, problem.goal)
        end_time = time.time()
    elapsed_time = end_time - st_time
    return h, elapsed_time


def search_solution(problem, h, type):
    if type == 0:
        st_time = time.time()
        sol, open_list, closed_list, wait = ReachGoal(problem, h)
        end_time = time.time()
    else:
        st_time = time.time()
        sol, open_list, closed_list, wait = ReachGoal_variant(problem, h)
        end_time = time.time()

    elapsed_time = end_time - st_time
    return sol, open_list, closed_list, wait, elapsed_time


def save_result(problem, h, times, sol, path_cost, open_list, closed_list, wait):
    repository.write_result(problem,
                            h,
                            times,
                            sol,
                            path_cost,
                            open_list,
                            closed_list,
                            wait)


if __name__ == "__main__":
    main()
