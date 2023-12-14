# todo salva le istanza del problema -s da CLI
import csv
import cProfile
import os
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

args = cli.get_args()

os.environ['SEED'] = str(args.seed) if args.command and args.seed is not None else 'None'


def generate_problems(configurations):
    problems = []
    for config in configurations:
        try:
            problem, problem_time = generate_instance(config)
            if args.save:
                repository.save_problem(problem)
            problems.append((problem, problem_time))
        except Exception as e:
            print(f"Errore durante la generazione del problema: {e}")
    return problems

def solve_problems(problems,heuristic_type, use_variant=False):
    for problem, problem_time in problems:
        try:
            heuristic, heuristic_time = generate_heuristic(problem, heuristic_type)
            solver = ReachGoal(problem, heuristic, use_variant)
            _, search_time = solver.search()
            repository.save_report(
                problem, solver, heuristic, problem_time, search_time, heuristic_time
            )
            visualizer = Animation(problem.grid, problem.agent_paths, solver.path)
            visualizer.show()
        
            if args.csv_output:
                file_name = os.path.basename(args.file)
                repository.save_report_csv(
                    problem, solver, heuristic, problem_time, search_time, heuristic_time,file_name
                )

        except Exception as e:
            print(f"Errore durante la risoluzione del problema: {e}")

def main():
    if args.command == "man":
        handler = InputHandler()
    command_dispatch = {
        "gen": lambda: solve_problems(problems=generate_problems(repository.load_configurations(args.file)),heuristic_type = args.heuristic,use_variant=args.variant),
        "man": lambda: solve_problems(generate_problems([handler.config]),handler.heuristic_type,handler.use_variant),
        "run": lambda: solve_problems(repository.load_problem(args.file)),
    }

    try:
        command_func = command_dispatch.get(args.command)
        if command_func is None:
            raise ValueError(f"Comando non riconosciuto: {args.command}")

        command_func()

    except Exception as e:
        print(f"Si è verificato un errore: {e}")

def generate_instance(config):
    start_time = time.perf_counter()
    # Converte le stringhe numeriche in interi o float
    problem_instance = Problem(**config)
    elapsed_time = time.perf_counter() - start_time
    return problem_instance, elapsed_time


def generate_heuristic(problem: Problem, heuristic_type):

    if heuristic_type not in HEURISTIC_CLASSES:
        raise ValueError(f"Unsupported heuristic type: {heuristic_type}")

    start_time = time.perf_counter()
    heuristic = HEURISTIC_CLASSES[heuristic_type](problem.grid, problem.goal)
    elapsed_time = time.perf_counter() - start_time

    return heuristic, elapsed_time

if __name__ == "__main__":
    main()
