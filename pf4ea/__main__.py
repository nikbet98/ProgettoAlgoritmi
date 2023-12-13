# todo salva le istanza del problema -s da CLI
import csv
import cProfile
import pickle
import time

from agents import Agents
from gridGraph import GridGraph
from heuristic import *
from plotGraph import graphPlotter
from problem import Problem

from search import ReachGoal
from state import State
from utils import get_path_cost
from visualize import Animation
from memory_profiler import memory_usage
from input_handler import InputHandler
import repository
import cli
from memory_profiler import memory_usage
args = cli.get_args()


# file = "./csv/100x100_08_02_10_100.csv"
# file = "./csv/10x10_08_02_3_20 .csv"
# file = "./csv/25x25_06_05_10_50.csv"
# file = "./csv/10x10_08_02_3_20.csv"


def generate_problems(configurations):
    problems = []
    for config in configurations:
        try:
            problem, problem_time, problem_mem_usage = generate_instance(config)
            if args.save:
                repository.save_problem(problem)
            problems.append((problem, problem_time, problem_mem_usage))
        except Exception as e:
            print(f"Errore durante la generazione del problema: {e}")
    return problems


def solve_problems(problems, heuristic_type, use_variant=False):
    for problem, problem_time, problem_mem_usage in problems:
        try:
            heuristic, heuristic_time, h_mem_usage = generate_heuristic(problem, heuristic_type)
            solver = ReachGoal(problem, heuristic, use_variant)
            _, search_time = solver.search()
            search_mem_usage = memory_usage(solver.search(), max_usage=True)
            repository.save_report(
                problem, solver, heuristic, problem_time, search_time, heuristic_time,problem_mem_usage,  h_mem_usage, search_mem_usage
            )
            visualizer = Animation(problem.grid, problem.agent_paths, solver.path)
            visualizer.show()
        except Exception as e:
            print(f"Errore durante la risoluzione del problema: {e}")


def main():
    if args.command == "man":
        handler = InputHandler()
    command_dispatch = {
        "gen": lambda: solve_problems(problems=generate_problems(repository.load_configurations(args.file)),
                                      heuristic_type=args.heuristic, use_variant=args.variant),
        "man": lambda: solve_problems(generate_problems([handler.config]), handler.heuristic_type, handler.use_variant),
        "run": lambda: solve_problems(repository.load_problem(args.file)),
    }

    try:
        command_func = command_dispatch.get(args.command)
        if command_func is None:
            raise ValueError(f"Comando non riconosciuto: {args.command}")

        command_func()

    except Exception as e:
        print(f"Si è verificato un errore: {e}")


# def main():
#     # leggiamo la configurazione da file
#     configs = repository.load_csv(file)

#     pf4ea, generating_instance_time = generate_instance(config)
#     # # salvo il problema file
#     repository.write_problem(pf4ea)
#     # carico il problema da file
#     # pf4ea = repository.read_problem("10x10_0.8_0.2_3_20_74_46")
#     # calcoliamo l'euristica
#     h, heuristic_time = generate_heuristic(pf4ea, 1)
#     # troviamo la soluzione
#     result = search_solution(pf4ea, h, 1)

#     # salva il risultato (se ho generato tutto da 0)
#     save_report(result)
#     # salva il risultato (se ho caricato il problema)
#     # save_result(pf4ea, h, [0, heuristic_time, resolution_time], sol,
#     #             get_path_cost(sol, pf4ea.grid), open_list, closed_list, wait)
#     print(pf4ea.grid)
#     graphPlotter(pf4ea.grid)

#     animation = Animation(pf4ea.grid, pf4ea.agent_paths, sol)
#     animation.show()


# repository.write_problem(pf4ea,h)

# problem, h = repository.read_problem("10x10_0.8_0.2_3_20_79_19")


def generate_instance(config):
    start_time = time.time()
    # Converte le stringhe numeriche in interi o float
    problem_instance = Problem(**config)
    elapsed_time = time.time() - start_time
    mem = memory_usage(Problem(**config), max_usage=True)
    return problem_instance, elapsed_time, mem


def generate_heuristic(problem: Problem, heuristic_type):
    heuristic_classes = {
        "h1": DiagonalDistance,
        "h2": HeuristicRelaxPath,
    }

    if heuristic_type not in heuristic_classes:
        raise ValueError(f"Unsupported heuristic type: {heuristic_type}")

    start_time = time.time()
    heuristic = heuristic_classes[heuristic_type](problem.grid, problem.goal)
    elapsed_time = time.time() - start_time
    mem = memory_usage(heuristic_classes[heuristic_type](problem.grid, problem.goal), max_usage=True)
    return heuristic, elapsed_time, mem


if __name__ == "__main__":
    main()
