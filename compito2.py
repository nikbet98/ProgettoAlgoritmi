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
        
    #test
    path.reverse()
    print(path)
    return path


def ReachGoal(grid, paths, init, goal, max_time,heuristic):

    time = 0
    #test
    f_score = lambda state: state.get_path_cost() + heuristic(state.get_node())
    #test
    open = PriorityQueue(init, f=f_score)
    closed = list()

    while open and time < max_time: # non possiamo spostare l'if a riga 31 nel while? while open.is_empty() and time < maximum_time:
        current_state = open.pop()
        #test
        print("current state =",current_state.node,"time =",current_state.time)
        #test
        closed.append(current_state)

        if current_state.is_goal(goal):  # current_state[1] is the node
            return ReconstructPath(init, current_state)


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
                        
        print("open list :")
        print(open)
        print("closed list :")
        string_closed_list = ', '.join(f"< ({state.node},{state.time}),{f_score(state)}>" for state in closed)
        print(string_closed_list)
        print("_______________________")

        time += 1


    return None

def ReachGoal_variant(grid, paths, init, goal, max_time, heuristic):

    time = 0
    cols = grid.get_dim()[1]
    predecessors = heuristic.get_predecessors()
    f_score = lambda state: state.get_path_cost() + heuristic(state.get_node())

    open = PriorityQueue(init, f = f_score)
    closed = list()

    while open and time < max_time:
        current_state = open.pop()
        closed.append(current_state)

        if current_state.is_goal(goal):  # current_state[1] is the node
            return ReconstructPath(init, current_state)

        current_node = current_state.get_node()
        path_free = collision_free_path(current_node, paths, time, goal, max_time, predecessors, cols)
        if path_free:
            path_from_current = heuristic.return_path(predecessors[current_state.get_node()], goal)
            path_to_current = ReconstructPath(init, current_state)
            return path_to_current.append(path_from_current)

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
        path_lenght = len(path)-1
        # controllo se il è già arrivato alla fine l'altro agente
        if(path_lenght < time or path_lenght < time + 1): 
            p = path[-1]
            p_next = p
        else:
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

def collision_free_path(current_node, paths, time, goal, max_time, predecessors, cols):
    if time > max_time:
        return False
    next_node = predecessors[current_node]
    if is_collision_free(current_node, next_node, paths, time, cols):
        if next_node == goal:
            return True
        else:
            return collision_free_path(next_node, paths, time+1, goal, max_time, predecessors, cols)