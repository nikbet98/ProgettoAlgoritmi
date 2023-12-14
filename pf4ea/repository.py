import os
import csv
import pickle
import yaml
from heuristic import DiagonalDistance, HeuristicRelaxPath
from utils import get_path_cost

# Ottengo il percorso della directory padre
PARENT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTANCES_DIRECTORY = os.path.join(PARENT_DIRECTORY, "benchmarks", "instances")
RESULTS_DIRECTORY = os.path.join(PARENT_DIRECTORY, "benchmarks", "results")


def load_configurations(file):
    with open(file, mode="r") as csv_file:
        configurations = []
        reader = csv.DictReader(csv_file)
        for row in reader:
            config = {}
            for k, v in row.items():
                config[k] = v
                if k in ['rows', 'cols', 'num_agents', 'maximum_time']:
                    config[k] = int(v)
                elif k in ['traversability_ratio', 'obstacle_agglomeration_ratio']:
                    float_value = float(v)
                    if 0 <= float_value <= 1:
                        config[k] = float_value
                    else:
                        raise ValueError(f"{k} must be between 0 and 1.")
            configurations.append(config)

    print(f"Configurazioni caricate correttamente da {file}.")
    return configurations


def load_problem(name):
    file_path = os.path.join(INSTANCES_DIRECTORY, f"{name}.pkl")
    with open(file_path, "rb") as to_read:
        out = pickle.load(to_read)
    print(f"Problema {name} caricato correttamente.")
    return out


def read_problem(name):
    file_path = os.path.join(INSTANCES_DIRECTORY, f"{name}.pkl")
    with open(file_path, "rb") as to_read:
        out = pickle.load(to_read)
    print(f"Problema {name} caricato correttamente.")
    return out


def save_problem(problem):
    file_name = generate_name(problem)
    file_path = os.path.join(INSTANCES_DIRECTORY, file_name)

    # Crea la directory se non esiste
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as file:
        pickle.dump(problem, file)

    print(f"Problema salvato correttamente nel file {file_path}.")


def save_report(problem, solver, heuristic, problem_time, search_time, heuristic_time):
    name = f"{generate_name(problem)}_{get_h_type(heuristic)}.md"
    file_path = os.path.join(RESULTS_DIRECTORY, name)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"{problem}")
        file.write(f"{problem.grid.obstacles_to_string()}")
        file.write("\n<!-- ************************** -->\n")
        file.write(f"{solver}")
        file.write("\n<!-- ************************** -->\n")
        file.write(performance_to_string(problem_time, heuristic_time, search_time))

    print(f"Report salvato correttamente nel file {file_path}.")


def performance_to_string(problem_time, heuristic_time, search_time):
    performance_string = (
        f"## PERFORMANCE\n"
        f"* Tempo per la generazione dell'istanza: {problem_time:.10e} sec\n"
        f"* Tempo per la generazione dell'euristica: {heuristic_time:.10e} sec\n"
        f"* Tempo per la ricerca della soluzione: {search_time:.10e} sec\n"
    )
    return performance_string


def generate_name(problem):
    return f"{problem.grid.rows}x{problem.grid.cols}_{problem.grid.traversability_ratio}_{problem.grid.obstacle_agglomeration_ratio}_{problem.num_agents}_{problem.maximum_time}_{problem.init}_{problem.goal}"


def get_h_type(heuristic):
    return type(heuristic).__name__
