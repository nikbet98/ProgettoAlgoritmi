import datetime
import os
import csv
import pickle
from utils import get_path_cost

# Ottengo il percorso della directory padre
PARENT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTANCES_DIRECTORY = os.path.join(PARENT_DIRECTORY, "benchmarks", "problems")
RESULTS_DIRECTORY = os.path.join(PARENT_DIRECTORY, "benchmarks", "report")
OUTPUT_CSV = os.path.join(PARENT_DIRECTORY, "benchmarks", "output_csv")
MEDIA_DIRECTORY = os.path.join(PARENT_DIRECTORY, "benchmarks","report","media")


def load_configurations(file_path):
    # If the file path doesn't exist, assume it's just a file name and look for it in the 'benchmarks/generators/' directory
    if not os.path.exists(file_path):
        file_path = os.path.join("benchmarks", "generators", file_path)

    with open(file_path, mode="r") as file:
        configurations = []
        reader = csv.DictReader(file)
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

    print(f"Configurazioni caricate correttamente da {file_path}.")
    return configurations


def load_problem(file_path):
    file_path = os.path.join(INSTANCES_DIRECTORY, f"{file_path}.pkl")
    with open(file_path, "rb") as to_read:
        out = pickle.load(to_read)
    print(f"Problema {file_path} caricato correttamente.")
    return out


def load_csv_to_dict(file_path):
    if not os.path.exists(file_path):
        file_path = os.path.join(OUTPUT_CSV, file_path)
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data


def read_problem(name):
    file_path = os.path.join(INSTANCES_DIRECTORY, f"{name}.pkl")
    with open(file_path, "rb") as to_read:
        out = pickle.load(to_read)
    print(f"Problema {name} caricato correttamente.")
    return out


def save_problem(problem):
    file_name = generate_name(problem) + ".pkl"
    file_path = os.path.join(INSTANCES_DIRECTORY, file_name)

    # Crea la directory se non esiste
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as file:
        pickle.dump(problem, file)

    print(f"Problema salvato correttamente nel file {file_path}.")


def save_report(problem, heuristic, result,visualizer):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    
    file_name = f"{generate_name(problem)}_{get_h_type(heuristic)}.md"
    file_path = os.path.join(RESULTS_DIRECTORY, file_name)
    file_name_img = file_name.replace(".md",f"_{timestamp}.png")
    file_name_video = file_name.replace(".md",f"_{timestamp}.mp4")
    
    visualizer.save_as_image(os.path.join(MEDIA_DIRECTORY, file_name_img))
    visualizer.save_as_video(os.path.join(MEDIA_DIRECTORY, file_name_video))

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"{problem}\n")
        file.write("\n<!-- ************************** -->\n")
        file.write(f"{result}")
        file.write("\n<!-- ************************** -->\n")
        file.write(performance_to_string(problem, heuristic, result))
        file.write(f"![immagine](./media/{file_name_img})\n")
        file.write(f"[Link al video](./media/{file_name_video})\n")


    print(f"Report salvato correttamente nel file {file_path}.")


def save_report_csv(problem, heuristic, result, input_file_name):
    input_file_name = (
        input_file_name.replace("input_", "")
        if input_file_name.startswith("input_")
        else input_file_name
    )

    output_file_name = "output_" + input_file_name
    file_path = os.path.join(OUTPUT_CSV, output_file_name)

    field_names = [
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
        "mem_grid",
        "mem_heuristic",
        "mem_open",
        "mem_closed",
        "mem_path",
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
        "path_length": len(result.path),
        "path_cost": get_path_cost(result.path, problem.grid),
        "tot_states": len(result.closed) + len(result.open),
        "percentage_visited_nodes": result.percentage_visited_nodes,
        "unique_node_visited": result.num_unique_node_visited,
        "wait": result.wait,
        "problem_time": problem.execution_time,
        "heuristic_time": heuristic.execution_time,
        "search_time": result.execution_time,
        "mem_grid": to_kbs(result.mem_grid),
        "mem_heuristic": to_kbs(result.mem_heuristic),
        "mem_open": to_kbs(result.mem_open),
        "mem_closed": to_kbs(result.mem_closed),
        "mem_path": to_kbs(result.mem_path),
    }

    with open(file_path, "a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, field_names)
        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(report_data)

    print(f"Report salvato correttamente nel file {file_path}.")


def performance_to_string(problem, heuristic, result):
    if result is None:
        return "Il risultato è None, quindi non è possibile accedere a execution_time"

    
    performance_string = (
        f"## PERFORMANCE\n"
        f"* Tempo per la generazione dell'istanza: {problem.execution_time:.10e} sec\n"
        f"* Tempo per la generazione dell'euristica: {heuristic.execution_time:.10e} sec\n"
        f"* Tempo per la ricerca della soluzione: {result.execution_time:.10e} sec\n"
        f"* Memoria griglia: {to_kbs(result.mem_grid)} kbs\n"
        f"* Memoria euristica: {to_kbs(result.mem_heuristic)} kbs\n"
        f"* Memoria closed: {to_kbs(result.mem_closed)} kbs\n"
        f"* Memoria open: {to_kbs(result.mem_open)} kbs\n"
        f"* Memoria path: {to_kbs(result.mem_path)} kbs\n"
    )

    return performance_string


def to_kbs(mem):
    return mem / 1024


def generate_name(problem):
    return f"{problem.grid.rows}x{problem.grid.cols}_{problem.grid.traversability_ratio}_{problem.grid.obstacle_agglomeration_ratio}_{problem.num_agents}_{problem.maximum_time}_{problem.init}_{problem.goal}".replace('.', '')

def get_h_type(heuristic):
    return type(heuristic).__name__
