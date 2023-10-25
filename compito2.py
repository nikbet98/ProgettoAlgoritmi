import math
from state import State
from utils import PriorityQueue, expand, Heuristic
from gridGraph import GridGraph


def ReconstructPath(init, goal):
    path = [goal]
    state = goal.get_parent()
    while state != init:
        path.append(state)
    return path.reverse()


def ReachGoal(grid, paths, init, goal, max_time):

    time = 0
    heuristic = Heuristic(grid, goal)
    def f_score(state): return state.get_path_cost + heuristic.diagonal(state)

    open = PriorityQueue(init, f=f_score)
    closed = set()

    while open:
        current_state = open.pop()
        closed.add(current_state)

        if current_state.is_goal(goal):  # current_state[1] is the node
            return ReconstructPath(init, goal, current_state)

        if time < max_time:
            for child_state in expand(grid, current_state, time):
                if child_state not in closed:
                    n = child_state.get_node()
                    v = current_state.get_node()
                    # check if the path is traversable
                    traversable = check_traversable(v, n, paths, time, grid.get_dim()[1])

                    if traversable:
                        if child_state not in open:
                            open.append(child_state)
                        elif f_score(child_state) < open[child_state]:
                            del open[child_state]
                            open.append(child_state)
    return None

def check_traversable(current, next_node, paths, time, cols):
    for path in paths:
        p = path[time]
        p_next = path[time+1]

        # incroci semplici
        if p_next == next_node:
            return False
        if p_next == current and p == next_node:
            return False

        # incroci diagonali
        if current - 1 == p_next and p == next_node:
            return False
        if p - cols == next_node and current - cols == p_next:
            return False
        if current == p_next - 1 and p == next_node - 1:
            return False
        if current + cols == p_next and p + cols == next_node:
            return False

    return True
