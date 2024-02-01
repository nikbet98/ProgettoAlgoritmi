from collections import deque
import sys
import time
from result import Result, ResultFactory
from state import State
from utils import (
    PriorityQueue,
    expand,
    is_free_collision,
    is_path_free,
    calculate_unique_visited,
)


class PathFinder:
    def __init__(self, problem, heuristic, use_variant=False):
        """
        Inizializza un nuovo oggetto risolutore per il problema PF4EA.

        :param problem: Il problema da risolvere.
        :param heuristic: L'euristica da utilizzare per valutare i nodi.
        :param use_variant: Indica se utilizzare la variante di ReachGoal.
        """
        self.problem = problem
        self.heuristic = heuristic
        self.use_variant = use_variant
        self.f_score = lambda state: state.path_cost + self.heuristic(state.node)
        self.path = None
        self.open = None
        self.closed = None
        self.wait = None
        self.path_cost = None
        self.__start_time = time.process_time()

    def __execution_time(self) -> float:
        return time.process_time() - self.__start_time

    def search(self):
        search_algorithm = (
            self._ReachGoal_variant() if self.use_variant else self._ReachGoal()
        )
        return search_algorithm

    """
    #EFFICIENZA
    list.reverse() ha complessità O(n)
    con deque  (coda a due estremità) gli elementi li aggiungiamo in testa
    con tempo costante O(1). Non c'è bisogno di invertire la coda alla fine.
    """

    def ReconstructPath(self, init: State, goal: State):
        path = deque([goal.node])
        current_state = goal
        wait = 0
        while current_state.node != init.node:
            next_state = current_state.parent
            path.appendleft(next_state.node)
            if current_state.node == next_state.node:
                wait += 1
            current_state = next_state
        return list(path), wait

    def _ReachGoal(self) -> Result:
        """
        Trova il percorso ottimo per raggiungere l'obiettivo nel problema specificato.
        """

        init = State(self.problem.init, 0)
        self.open = PriorityQueue(init, f=self.f_score)
        self.closed = set()

        while self.open:
            current_state = self.open.pop()
            time = current_state.time

            if time > self.problem.maximum_time:
                continue

            self.closed.add(current_state)

            if self.problem.is_goal(current_state.node):
                self.path, self.wait = self.ReconstructPath(init, current_state)
                self.path_cost = current_state.path_cost

                return ResultFactory.create_result(self, self.__execution_time)

            for child_state in expand(self.problem, current_state):
                if child_state not in self.closed:
                    current_node = current_state.node
                    child_node = child_state.node

                    traversable = is_free_collision(
                        self.problem.agent_paths,
                        current_node,
                        child_node,
                        time,
                        self.problem.cols,
                    )

                    if traversable:
                        if child_state not in self.open:
                            self.open.add(child_state)
                        elif self.f_score(child_state) < self.open[child_state]:
                            del self.open[child_state]
                            self.open.add(child_state)

        return ResultFactory.create_result(self, self.__execution_time)

    def _ReachGoal_variant(self):
        predecessors = self.heuristic.predecessors
        init = State(self.problem.init, 0)
        self.open = PriorityQueue(init, f=self.f_score)
        self.closed = set()

        if predecessors[init.node] is None:
            return ResultFactory.create_result(self, self.__execution_time)

        while self.open:
            current_state = self.open.pop()
            time = current_state.time
            self.closed.add(current_state)

            if current_state.time > self.problem.maximum_time:
                continue

            if self.problem.is_goal(current_state.node):  # current_state[1] is the node
                self.path, self.wait = self.ReconstructPath(init, current_state)
                self.path_cost = current_state.path_cost

                return ResultFactory.create_result(self, self.__execution_time)

            current_node = current_state.node
            path_free = is_path_free(self.problem, current_node, time, predecessors)

            if path_free:
                path_from_current = self.heuristic.return_path(
                    predecessors[current_state.node], self.problem.goal
                )
                path_to_current, self.wait = self.ReconstructPath(init, current_state)
                self.path = path_to_current + path_from_current
                self.path_cost = (
                    current_state.path_cost
                    + self.heuristic.distances[current_state.node]
                )

                return ResultFactory.create_result(self, self.__execution_time)

            for child_state in expand(self.problem, current_state):
                if child_state not in self.closed:
                    current_node = child_state.node
                    child_node = current_state.node

                    traversable = is_free_collision(
                        self.problem.agent_paths,
                        current_node,
                        child_node,
                        time,
                        self.problem.cols,
                    )

                    if traversable:
                        if child_state not in self.open:
                            self.open.add(child_state)
                        elif self.f_score(child_state) < self.open[child_state]:
                            del self.open[child_state]
                            self.open.add(child_state)

        return ResultFactory.create_result(self, self.__execution_time)

    def calculate_visited_nodes(self):
        return (
            len(calculate_unique_visited(self.closed))
            / (self.problem.grid.get_size() - self.problem.grid.num_obstacles)
            * 100
        )
