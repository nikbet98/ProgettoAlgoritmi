import math
from state import State
from utils import PriorityQueue, expand
from gridGraph import GridGraph


def ReconstructPath(init, goal_state):
    path = [goal_state]
    state = goal_state.get_parent()
    while state != init:
        path.append(state)
    return path.reverse()


def ReachGoal(grid, paths, init, goal, max_time,heuristic):

    time = 0
    f_score = lambda state: state.get_path_cost() + heuristic(state.get_node())

    open = PriorityQueue(init, f=f_score)
    closed = list()

    while open:
        current_state = open.pop()
        closed.append(current_state)

        if current_state.is_goal(goal):  # current_state[1] is the node
            return ReconstructPath(init, current_state)


        if time < max_time:
            for child_state in expand(grid, current_state, time):
                if child_state not in closed:
                    n = child_state.get_node()
                    v = current_state.get_node()
                    # check if the path is traversable
                    traversable = is_collision_free(v, n, paths, time, grid.get_dim()[1])

                    if traversable:
                        if child_state not in open:
                            open.add(child_state)
                        elif f_score(child_state) < open[child_state]:
                            del open[child_state]
                            open.add(child_state)
        time += 1
    return None

def ReachGoal_variant(grid, paths, init, goal, max_time, heuristic):

    time = 0
    cols = grid.get_dim()[1]
    predecessors = heuristic.get_predecessors()
    def f_score(state): return state.get_path_cost() + heuristic(state.get_node())

    open = PriorityQueue(init, f=f_score)
    closed = set()

    while open:
        current_state = open.pop()
        closed.add(current_state)

        if current_state.is_goal(goal):  # current_state[1] is the node
            return ReconstructPath(init, current_state)

        if collision_free_path(current_state, paths, time, goal, max_time, predecessors, cols):
            return ReconstructPath(init, current_state).append(ReconstructPath(State(predecessors(current_state.get_node()),time+1), State(goal)))
        if time < max_time:
            for child_state in expand(grid, current_state, time):
                if child_state not in closed:
                    n = child_state.get_node()
                    v = current_state.get_node()
                    # check if the path is traversable
                    traversable = is_collision_free(v, n, paths, time, cols)

                    if traversable:
                        if child_state not in open:
                            open.add(child_state)
                        elif f_score(child_state) < open[child_state]:
                            del open[child_state]
                            open.add(child_state)
        time += 1
    return None

def is_collision_free(current, next_node, paths, time, cols):
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

def collision_free_path(current_state, paths, time, goal, max_time, predecessors, cols):
    if time > max_time:
        return False
    next = predecessors[current_state]
    if is_collision_free(current_state.get_node(), next.get_node(), paths, time, goal.get_node(), cols):
        if next == goal:
            return True
        else:
            collision_free_path(next, paths, time+1, goal, max_time, predecessors, cols)