import math
from state import State
from utils import PriorityQueue, expand
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


def ReachGoal(grid, paths, init, goal_node, max_time, heuristic):
    waited = 0
    cols = grid.get_dim()[1]
    f_score = lambda state: state.get_path_cost() + heuristic(state.get_node())
    open = PriorityQueue(init, f=f_score)
    closed = list()

    while open:
        current_state = open.pop()
        if current_state.node == current_state.parent.node:
            waited += 1
            
        if current_state.time > max_time:
            return None
        # test
        print("current state =", current_state.node, "time =", current_state.time)
        # test
        closed.append(current_state)

        if current_state.is_goal(goal_node):  # current_state[1] is the node
            return ReconstructPath(init, current_state)

        for child_state in expand(grid, current_state, time):
            if child_state not in closed:
                current_node = current_state.get_node()
                child_node = child_state.get_node()

                # check if the path is traversable
                traversable = is_collision_free(
                    current_node, child_node, paths, time, cols
                )

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


def ReachGoal_variant(grid, paths, init, goal, max_time, heuristic):
    cols = grid.get_dim()[1]
    predecessors = heuristic.get_predecessors()
    f_score = lambda state: state.get_path_cost() + heuristic(state.get_node())

    open = PriorityQueue(init, f=f_score)
    closed = list()

    while open:
        current_state = open.pop()
        time = current_state.time
        if current_state.time > max_time:
            return None
        closed.append(current_state)

        if current_state.is_goal(goal):  # current_state[1] is the node
            return ReconstructPath(init, current_state)

        current_node = current_state.get_node()
        path_free = collision_free_path(
            current_node, paths, time, goal, max_time, predecessors, cols
        )
        if path_free:
            path_from_current = heuristic.return_path(
                predecessors[current_state.get_node()], goal
            )
            path_to_current = ReconstructPath(init, current_state)
            return path_to_current + path_from_current

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
    return None


def calculate_positions(agent_path, time):
    path_length = len(agent_path) - 1
    # controllo se il è già arrivato alla fine l'altro agente
    if path_length < time or path_length < time + 1:
        current_position = agent_path[-1]
        next_position = current_position
    else:
        current_position = agent_path[time]
        next_position = agent_path[time + 1]
    return current_position, next_position


def is_collision_free(current_node, next_node, agent_paths, time, grid_cols):
    for agent_path in agent_paths:
        current_position, next_position = calculate_positions(agent_path, time)
        if check_collision(
            current_node, next_node, current_position, next_position, grid_cols
        ):
            return False

    return True


def check_collision(
    current_node, next_node, current_position, next_position, grid_cols
):
    # incroci semplici e diagonali
    return any(
        [
            next_position == next_node,
            next_position == current_node and current_position == next_node,
            current_node - 1 == next_position and current_position == next_node,
            current_position - grid_cols == next_node
            and current_node - grid_cols == next_position,
            current_node == next_position - 1 and current_position == next_node - 1,
            current_node + grid_cols == next_position
            and current_position + grid_cols == next_node,
        ]
    )


def collision_free_path(
    current_node, agent_paths, time, goal_node, max_time, predecessors, grid_cols
):
    if time > max_time:
        return False
    next_node = predecessors[current_node]
    if is_collision_free(current_node, next_node, agent_paths, time, grid_cols):
        if next_node == goal_node:
            return True
        else:
            return collision_free_path(
                next_node,
                agent_paths,
                time + 1,
                goal_node,
                max_time,
                predecessors,
                grid_cols,
            )
