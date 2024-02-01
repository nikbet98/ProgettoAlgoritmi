import random
import os
from typing import List, Optional
from utils import is_free_collision
from heuristic import *
from gridGraph import GridGraph


class Agents:
    def __init__(self, max_time: int, num_paths: int):
        self.max_time = max_time
        self.paths: List[List[int]] = []
        self.num_paths = num_paths

    def generate_paths(
        self, grid: GridGraph, available_nodes: List[int]
    ) -> List[List[int]]:
        random.shuffle(available_nodes)
        cols = grid.get_dim()[1]

        for _ in range(self.num_paths):
            if not available_nodes:
                print("Non ci sono più nodi disponibili")
                break

            path = self._generate_single_path(grid, available_nodes, cols)
            if path is not None:
                self.paths.append(path)

        return self.paths

    def _generate_single_path(
        self, grid: GridGraph, available_nodes: List[int], cols: int
    ) -> Optional[List[int]]:
        current_node = available_nodes.pop()
        path = [current_node]

        mu = (1 + self.max_time) / 2
        sigma = self.max_time / 4
        agent_path_duration = int(random.gauss(mu, sigma))

        for time in range(agent_path_duration):
            if not available_nodes:
                break

            neighbors = list(grid.get_adj_list(current_node))
            random.shuffle(neighbors)

            for next_node in neighbors:
                if is_free_collision(self.paths, current_node, next_node, time, cols):
                    path.append(next_node)
                    current_node = next_node
                    break

        return path

    def __str__(self) -> str:
        return "\n".join(str(path) for path in self.paths)


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
