import os
import csv
import pickle
import yaml
from heuristic import DiagonalDistance, HeuristicRelaxPath
from utils import get_path_cost

# Ottengo il percorso della directory padre
PARENT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTANCES_DIRECTORY = os.path.join(PARENT_DIRECTORY, "benchmarks", "instances")
RESULTS_DIRECTORY = os.path.join(PARENT_DIRECTORY, "benchmarks", "report")


def load_configurations(file):
    # If the file path doesn't exist, assume it's just a file name and look for it in the 'benchmarks/generators/' directory
    if not os.path.exists(file):
        file = os.path.join('benchmarks', 'generators', file)

    with open(file, mode="r") as csv_file:
        configurations = []
        reader = csv.DictReader(csv_file)
        for row in reader:
            config = {}
            for k, v in row.items():
                config[k] = v
                if k in ["rows", "cols", "num_agents", "maximum_time"]:
                    config[k] = int(v)
                elif k in ["traversability_ratio", "obstacle_agglomeration_ratio"]:
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
    file_name = f"{generate_name(problem)}_{get_h_type(heuristic)}.md"
    file_path = os.path.join(RESULTS_DIRECTORY, file_name)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"{problem}")
        file.write(f"{problem.grid.obstacles_to_string()}")
        file.write("\n<!-- ************************** -->\n")
        file.write(f"{solver}")
        file.write("\n<!-- ************************** -->\n")
        file.write(performance_to_string(problem_time, heuristic_time, search_time))

    print(f"Report salvato correttamente nel file {file_path}.")


def save_report_csv(
    problem, solver, heuristic, problem_time, search_time, heuristic_time, input_file_name
):  
    input_file_name = input_file_name.replace('input_', '') if input_file_name.startswith('input_') else input_file_name

    output_file_name = 'output_' + input_file_name
    file_path = os.path.join(RESULTS_DIRECTORY, output_file_name)

    fieldnames = [
        "rows",
        "cols",
        "traversability_ratio",
        "obstacle_agglomeration_ratio",
        "num_agents",
        "maximum_time",
        "init",
        "goal",
        "h_type",
        "path_length",
        "path_cost",
        "tot_states",
        "percentage_visited_nodes",
        "unique_node_visited",
        "wait",
        "problem_time",
        "heuristic_time",
        "search_time",
    ]

    report_data = {
        "rows": problem.grid.rows,
        "cols": problem.grid.cols,
        "traversability_ratio": problem.grid.traversability_ratio,
        "obstacle_agglomeration_ratio": problem.grid.obstacle_agglomeration_ratio,
        "num_agents": problem.num_agents,
        "maximum_time": problem.maximum_time,
        "init": problem.init,
        "goal": problem.goal,
        "h_type": get_h_type(heuristic),
        "path_length": len(solver.path),
        "path_cost": get_path_cost(solver.path, problem.grid),
        "tot_states": len(solver.closed)+len(solver.open),
        "percentage_visited_nodes": solver.calculate_visited(),
        "unique_node_visited": len(solver.unique_node_visited()),
        "wait": solver.wait,
        "problem_time": problem_time,
        "heuristic_time": heuristic_time,
        "search_time": search_time,
    }

    with open(file_path, "a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames)
        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(report_data)

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
