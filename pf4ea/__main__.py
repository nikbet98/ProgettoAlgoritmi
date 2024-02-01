# todo specificare nel reachgoal variant che è finito il tempo nel Result
import os
import traceback

from heuristic import *
from problem import ProblemFactory
from search import PathFinder
from visualize import Animation
from input_handler import InputHandler
import repository
import cli

HEURISTIC_CLASSES = {
    "h1": DiagonalDistance,
    "h2": ChebyshevDistance,
    "h3": ManhattanDistance,
    "h4": EuclideanDistance,
    "h5": HeuristicRelaxPath,
}

args = cli.get_args()


def generate_problems(configurations):
    problems = []
    for config in configurations:
        try:
            problem = ProblemFactory.create_problem(config)
            if args.save:
                repository.save_problem(problem)
            problems.append(problem)
        except Exception as e:
            print(f"Errore durante la generazione del problema: {e}")
            print(f"Tipo di errore: {type(e).__name__}")
            print(f"Traceback: {traceback.format_exc()}")
    return problems


def solve_problems(problems, heuristic_type, use_variant=False):
    for problem in problems:
        try:
            heuristic = HeuristicFactory.create_heuristic(
                problem, heuristic_type, HEURISTIC_CLASSES
            )
            solver = PathFinder(problem, heuristic, use_variant)
            result = solver.search()

            visualizer = Animation(problem.grid, problem.agent_paths, result.path)

            if args.report:
                repository.save_report(problem, heuristic, result, visualizer)

            if args.show:
                visualizer.show()

            if args.command == "gen" and args.csv_output:
                file_name = os.path.basename(args.file)
                repository.save_report_csv(problem, heuristic, result, file_name)
        except Exception as e:
            print(f"Errore durante la risoluzione del problema: {e}")
            print(f"Tipo di errore: {type(e).__name__}")
            print(f"Traceback: {traceback.format_exc()}")


def main():
    if args.command == "man":
        handler = InputHandler()
    command_dispatch = {
        "gen": lambda: solve_problems(
            problems=generate_problems(repository.load_configurations(args.file)),
            heuristic_type=args.heuristic,
            use_variant=args.variant,
        ),
        "man": lambda: solve_problems(
            generate_problems([handler.config]),
            handler.heuristic_type,
            handler.use_variant,
        ),
        "run": lambda: solve_problems(repository.load_problem(args.file),use_variant=args.variant),
    }

    try:
        command_func = command_dispatch.get(args.command)
        if command_func is None:
            raise ValueError(f"Comando non riconosciuto: {args.command}")

        command_func()

    except Exception as e:
        print(f"Si è verificato un errore: {e}")
        print(f"Tipo di errore: {type(e).__name__}")
        print(f"Traceback: {traceback.format_exc()}")


if __name__ == "__main__":
    main()
