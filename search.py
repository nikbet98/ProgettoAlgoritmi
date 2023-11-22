import math
from state import State
from utils import PriorityQueue, expand, is_collision_free, is_free_path
from gridGraph import GridGraph


def ReconstructPath(init, goal_state):
    path = [goal_state.get_node()]
    current_state = goal_state
    while current_state.get_node() != init.get_node():
        next_state = current_state.get_parent()
        path.append(next_state.get_node())
        current_state = next_state

    # test
    path.reverse()
    print(path)
    return path


def ReachGoal(problem, heuristic):
    """
    Trova il percorso ottimo per raggiungere l'obiettivo nel problema specificato.

    Args:
        problem: L'istanza del problema specificato.
        heuristic: La funzione euristica utilizzata per valutare lo stato.

    Returns:
        Il percorso ottimo per raggiungere l'obiettivo, rappresentato come una lista di stati.
        Se non è possibile raggiungere l'obiettivo, restituisce None.
    """
    waited = 0

    f_score = lambda state: state.get_path_cost() + heuristic(state.get_node())

    init = State(problem.init, 0)
    open = PriorityQueue(init, f=f_score)
    closed = list()

    while open:
        current_state = open.pop()
        time = current_state.time

        if not current_state.is_parent_None() and current_state == current_state.parent.node:
            waited += 1
            
        if time > problem.maximum_time:
            return None
        
        # test
        print("current state =", current_state.node, "time =", time)
        # test
        closed.append(current_state)

        if current_state.is_goal(problem.goal):  # current_state[1] is the node
            return ReconstructPath(init, current_state)

        for child_state in expand(problem, current_state):
            if child_state not in closed:
                current_node = current_state.get_node()
                child_node = child_state.get_node()

                # check if the path is traversable
                traversable = is_collision_free(problem.agent_paths, current_node, child_node,time,problem.cols)

                if traversable:
                    if child_state not in open:
                        open.add(child_state)
                    elif f_score(child_state) < open[child_state]:
                        del open[child_state]
                        open.add(child_state)

        # test
        print("open list :")
        print(open)
        print("closed list :")
        string_closed_list = ", ".join(
            f"< ({state.node},{state.time}),{f_score(state)}>" for state in closed
        )
        print(string_closed_list)
        print("_______________________")
        # test

    return None


def ReachGoal_variant(problem, heuristic):
    predecessors = heuristic.get_predecessors()

    f_score = lambda state: state.get_path_cost() + heuristic(state.get_node())

    init = State(problem.init, 0)
    open = PriorityQueue(init, f=f_score)
    closed = list()

    while open:
        current_state = open.pop()
        time = current_state.time

        if current_state.time > problem.max_time:
            return None
        
        closed.append(current_state)

        if current_state.is_goal(problem.goal):  # current_state[1] is the node
            return ReconstructPath(init, current_state)

        current_node = current_state.get_node()
        path_free = is_free_path(problem, current_node, time, predecessors)

        if path_free:
    
            path_from_current = heuristic.return_path(
                predecessors[current_state.get_node()], problem.goal
            )
            path_to_current = ReconstructPath(init, current_state)

            return path_to_current + path_from_current

        for child_state in expand(problem, current_state):
            if child_state not in closed:
                current_node = child_state.get_node()
                child_node = current_state.get_node()
                # check if the path is traversable
                traversable = is_collision_free(problem, current_node,child_node, time)

                if traversable:
                    if child_state not in open:
                        open.add(child_state)
                    elif f_score(child_state) < open[child_state]:
                        del open[child_state]
                        open.add(child_state)
    return None





