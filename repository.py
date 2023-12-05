import csv
import pickle
from heuristic import DiagonalDistance, HeuristicRelaxPath
from utils import get_path_cost

INSTANCES = "./instances/"
RESULTS = "./results/"


def load_csv(file):
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            config = row
    return config


def generate_name(problem):
    return (str(problem.grid.rows) + "x"
            + str(problem.grid.cols) + "_"
            + str(problem.grid.traversability_ratio) + "_"
            + str(problem.grid.obstacle_agglomeration_ratio) + "_"
            + str(problem.num_agents) + "_"
            + str(problem.maximum_time) + "_"
            + str(problem.init) + "_"
            + str(problem.goal))


def write_problem(problem):
    file_name = generate_name(problem)
    with open(INSTANCES + file_name, "wb") as to_write:
        pickle.dump(problem, to_write)


def write_result(problem, heuristic, times, path, path_cost, open_list, closed_list, wait):
    name = generate_name(problem) + "_" + str(get_h_type(heuristic)) + ".txt"
    with open(RESULTS + name, 'w') as to_write:
        to_write.write("INFORMAZIONI SUL PROBLEMA" + '\n')
        to_write.write(problem.print_info())
        to_write.write("------------------------------------------" + '\n')
        to_write.write("RISULTATO DELLA RICERCA" + '\n')
        to_write.write("Percorso trovato: " + str(path) + '\n')
        to_write.write("Lunghezza del percorso trovato: " + str(len(path)) + '\n')
        to_write.write("Costo del percorso: " + str(path_cost) + '\n')
        to_write.write("Stati nella lista Open: " + str(open_list) + '\n')
        to_write.write("Stati nella lista Closed: " + str(closed_list) + '\n')
        to_write.write("Totale stati generati: " + str(open_list + closed_list) + '\n')
        to_write.write("Numero azioni Wait: " + str(wait) + '\n')
        to_write.write("------------------------------------------" + '\n')
        to_write.write("TEMPISTICHE" + '\n')
        to_write.write("Tempo per la generazione dell'istanza: " + str(times[0]) + '\n')
        to_write.write("Tempo per la generazione dell'euristica: " + str(times[1]) + '\n')
        to_write.write("Tempo per la ricerca della soluzione: " + str(times[2]) + '\n')


def get_h_type(heuristic):
    return type(heuristic).__name__


def read_problem(name):
    with open(INSTANCES + name, 'rb') as to_read:
        out = pickle.load(to_read)
    return out
