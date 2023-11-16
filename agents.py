import math
import random
from compito2 import is_collision_free, ReachGoal, ReachGoal_variant
from heuristic import *
from state import State


# ------
def generate_paths(grid, max_time, num_paths):
    paths = []

    available_nodes = grid.get_free_nodes()

    for _ in range(num_paths):
        if not available_nodes:
            print("Non ci sono più nodi disponibili")
            break

        path = generate_single_path(grid, max_time, available_nodes, paths)
        if path != None:
            paths.append(path)

    return paths


def generate_single_path(grid, max_time, available_nodes, paths):
    path = None
    while path == None:
        init_node = random.choice(available_nodes)
        available_nodes.remove(init_node)
        init_state = State(init_node, 0)

        goal_node = random.choice(available_nodes)
        available_nodes.remove(goal_node)
        if available_nodes == []: return None

        h = DiagonalDistance(
            grid, goal_node, weigh_cardinal_direction=1, weight_diagonal_direction=2
        )

        path = ReachGoal(grid, paths, init_state, goal_node, max_time, h)
        
    return path

