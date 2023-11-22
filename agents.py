import math
import random
from search import ReachGoal, ReachGoal_variant
from utils import is_collision_free
from heuristic import *
from state import State


class Agents:
    """
    Classe che rappresenta un insieme di agenti che generano percorsi casuali su una griglia.

    Args:
        max_time (int): Il tempo massimo percorribile da ciascun agente.
        num_paths (int): Il numero di percorsi da generare.

    Attributes:
        max_time (int): Il tempo massimo percorribile da ciascun agente.
        paths (list): Lista dei percorsi generati dagli agenti.
        num_paths (int): Il numero di percorsi da generare.

    Methods:
        generate_paths(grid): Genera i percorsi casuali sulla griglia specificata.
        generate_single_path(grid, available_nodes, cols): Genera un singolo percorso casuale sulla griglia.

    """

    def __init__(self, max_time, num_paths):
        self.max_time = max_time
        self.paths = []
        self.num_paths = num_paths

    def generate_paths(self,grid, available_nodes):
        """
        Genera i percorsi casuali sulla griglia specificata.

        Args:
            grid (Grid): La griglia su cui generare i percorsi.

        Returns:
            list: Lista dei percorsi generati dagli agenti.

        """
        random.shuffle(available_nodes)

        cols = grid.get_dim()[1]

        for _ in range(self.num_paths):
            if not available_nodes:
                print("Non ci sono più nodi disponibili")
                break

            path = self.generate_single_path(grid, available_nodes, cols)
            if path is not None:
                self.paths.append(path)

        return self.paths

    def generate_single_path(self, grid, available_nodes, cols):
        """
        Genera un singolo percorso casuale sulla griglia.

        Args:
            grid (Grid): La griglia su cui generare il percorso.
            available_nodes (list): Lista dei nodi disponibili sulla griglia.
            cols (int): Il numero di colonne della griglia.

        Returns:
            list: Il percorso generato.

        """
        
        current_node = available_nodes.pop()
        path = [current_node]

        agent_path_duration = random.randint(1, self.max_time)
        random.shuffle(available_nodes)

        for time in range(agent_path_duration):
            
            if available_nodes == []:
                break

            neighbors = grid.get_adj_list(current_node)
            next_node = random.choice(list(neighbors))

            while not is_collision_free(self.paths,current_node, next_node, time,cols):
                next_node = random.choice(list(neighbors))

            path.append(next_node)
            current_node = next_node

        return path




# ------
# def generate_paths(grid, max_time, num_paths):
#     paths = []

#     available_nodes = grid.get_free_nodes()

#     for _ in range(num_paths):
#         if not available_nodes:
#             print("Non ci sono più nodi disponibili")
#             break

#         path = generate_single_path(grid, max_time, available_nodes, paths)
#         if path != None:
#             paths.append(path)

#     return paths


# def generate_single_path(grid, max_time, available_nodes, paths):
#     path = None
#     while path == None:
#         init_node = random.choice(available_nodes)
#         available_nodes.remove(init_node)
#         init_state = State(init_node, 0)

#         goal_node = random.choice(available_nodes)
#         available_nodes.remove(goal_node)
#         if available_nodes == []: return None

#         h = DiagonalDistance(
#             grid, goal_node, weigh_cardinal_direction=1, weight_diagonal_direction=2
#         )

#         path = ReachGoal(grid, paths, init_state, goal_node, max_time, h)
        
#     return path

