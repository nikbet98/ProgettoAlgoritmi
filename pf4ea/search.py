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

        Args:
            problem: L'istanza del problema specificato.
            heuristic: La funzione euristica utilizzata per valutare lo stato.

        Returns:
            - Path: percorso ottimo per arrivare al goal da init, o None se non è stato trovato alcun percorso valido.
            - self.open length: lunghezza della lista self.open a fine esecuzione.
            - Closed length: lunghezza della lista closed a fine esecuzione.
            - Waited: numero delle azioni wait eseguite dall'agente.
        """

        f_score = lambda state: state.path_cost + self.heuristic(state.node)

        init = State(self.problem.init, 0)
        self.open = PriorityQueue(init, f=f_score)
        """
        #EFFICIENZA
        - list consente duplicati, set no
        - list per la ricerca di un elemento ha complessità O(n), mentre set O(1)
            questo perché i set sono implementati come tabelle hash.
        """
        self.closed = set()

        while self.open:
            current_state = self.open.pop()
            time = current_state.time

            if time > self.problem.maximum_time:
                continue

            self.closed.add(current_state)

            if self.problem.is_goal(current_state.node):  # current_state[1] is the node
                self.path, self.wait = self.ReconstructPath(init, current_state)
                self.path_cost = current_state.path_cost

                return ResultFactory.create_result(self,self.__execution_time)
                # return Result(
                #     path=self.path,
                #     path_cost=self.path_cost,
                #     open=self.open,
                #     closed=self.closed,
                #     wait=self.wait,
                #     use_variant=self.use_variant,
                #     percentage_visited_nodes=self.calculate_visited_nodes(),
                #     execution_time=self.__execution_time(),
                #     mem_grid=sys.getsizeof(self.problem.grid),
                #     mem_heuristic=sys.getsizeof(self.heuristic),
                # )

            for child_state in expand(self.problem, current_state):
                if child_state not in self.closed:
                    current_node = current_state.node
                    child_node = child_state.node

                    # check if the path is traversable
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
                        elif f_score(child_state) < self.open[child_state]:
                            del self.open[child_state]
                            self.open.add(child_state)

        return ResultFactory.create_result(self,self.__execution_time)
        # result = Result(
        #     path=[self.problem.init],
        #     path_cost=math.inf,
        #     open=self.open,
        #     closed=self.closed,
        #     wait=0,
        #     use_variant=self.use_variant,
        #     percentage_visited_nodes=self.calculate_visited_nodes(),
        #     execution_time=self.__execution_time(),
        #     mem_grid=sys.getsizeof(self.problem.grid),
        #     mem_heuristic=sys.getsizeof(self.heuristic),
        #     failure_code=SearchFailureCodes.NO_SOLUTION_FOUND,
        # )
        # controlla se l'errore è stato causato dal tempo non sufficiente
        # if check_error_time(self.problem.maximum_time, self.closed, self.problem):
        #     result.failure_code = (
        #         SearchFailureCodes.TIME_EXCEEDED
        #     )  # imposta l'errore corretto

        # return result

    def _ReachGoal_variant(self):
        predecessors = self.heuristic.predecessors
        f_score = lambda state: state.path_cost + self.heuristic(state.node)
        init = State(self.problem.init, 0)
        self.open = PriorityQueue(init, f=f_score)
        self.closed = set()

        if predecessors[init.node] is None:
            return ResultFactory.create_result(self,self.__execution_time)
        
            # return Result(
            #     path=[self.problem.init],
            #     path_cost=math.inf,
            #     open=self.open,
            #     closed=self.closed,
            #     wait=0,
            #     use_variant=self.use_variant,
            #     percentage_visited_nodes=self.calculate_visited_nodes(),
            #     execution_time=self.__execution_time(),
            #     mem_grid=sys.getsizeof(self.problem.grid),
            #     mem_heuristic=sys.getsizeof(self.heuristic),
            #     failure_code=SearchFailureCodes.NO_SOLUTION_FOUND,
            # )

        while self.open:
            current_state = self.open.pop()
            time = current_state.time
            self.closed.add(current_state)

            if current_state.time > self.problem.maximum_time:
                # If the current state is at the limit of the maximum time, it just get discarded
                continue

            if self.problem.is_goal(current_state.node):  # current_state[1] is the node
                self.path, self.wait = self.ReconstructPath(init, current_state)
                self.path_cost = current_state.path_cost

                return ResultFactory.create_result(self,self.__execution_time)
                # return Result(
                #     path=self.path,
                #     path_cost=self.path_cost,
                #     open=self.open,
                #     closed=self.closed,
                #     wait=self.wait,
                #     use_variant=self.use_variant,
                #     percentage_visited_nodes=self.calculate_visited_nodes(),
                #     execution_time=self.__execution_time(),
                #     mem_grid=sys.getsizeof(self.problem.grid),
                #     mem_heuristic=sys.getsizeof(self.heuristic),
                # )

            current_node = current_state.node
            path_free = is_path_free(self.problem, current_node, time, predecessors)

            if path_free:
                path_from_current = self.heuristic.return_path(
                    predecessors[current_state.node], self.problem.goal
                )
                path_to_current, self.wait = self.ReconstructPath(init, current_state)
                self.path = path_to_current + path_from_current
                self.path_cost  = current_state.path_cost + self.heuristic.distances[current_state.node]
                return ResultFactory.create_result(self,self.__execution_time)

            for child_state in expand(self.problem, current_state):
                if child_state not in self.closed:
                    current_node = child_state.node
                    child_node = current_state.node
                    # check if the path is traversable
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
                        elif f_score(child_state) < self.open[child_state]:
                            del self.open[child_state]
                            self.open.add(child_state)

        return ResultFactory.create_result(self,self.__execution_time)

        # result = Result(
        #     path=[self.problem.init],
        #     path_cost=math.inf,
        #     open=self.open,
        #     closed=self.closed,
        #     wait=0,
        #     use_variant=self.use_variant,
        #     percentage_visited_nodes=self.calculate_visited_nodes(),
        #     execution_time=self.__execution_time(),
        #     mem_grid=sys.getsizeof(self.problem.grid),
        #     mem_heuristic=sys.getsizeof(self.heuristic),
        #     failure_code=SearchFailureCodes.NO_SOLUTION_FOUND,
        # )
        # # controlla se l'errore è stato causato dal tempo non sufficiente
        # if check_error_time(self.problem.maximum_time, self.closed, self.problem):
        #     result.failure_code = SearchFailureCodes.TIME_EXCEEDED

        # return result

    def calculate_visited_nodes(self):
        return (
            len(calculate_unique_visited(self.closed))
            / (self.problem.grid.get_size() - self.problem.grid.num_obstacles)
            * 100
        )
