from collections import deque
from dataclasses import dataclass
import math
import sys
import time
from typing import List, Optional
from state import State
from utils import PriorityQueue, expand, is_free_collision, is_path_free
from gridGraph import GridGraph


@dataclass
class Result:
    path: Optional[List[int]]
    path_cost: Optional[float]
    open: PriorityQueue
    closed: set
    wait: int
    use_variant: bool
    execution_time: float
    percentage_visited_nodes: float
    num_unique_node_visited: Optional[int] = None
    path_length: int = None
    total_states: int = None
    mem_grid: float = None
    mem_heuristic: float = None
    mem_open: float = None
    mem_closed: float = None
    mem_path: float = None

    def __post_init__(self):
        self.path_length = len(self.path)
        self.num_unique_node_visited = self.calculate_num_unique_node_visited()
        self.total_states = len(self.open) + len(self.closed)
        self.mem_open = sys.getsizeof(self.open)
        self.mem_closed = sys.getsizeof(self.closed)
        self.mem_path = sys.getsizeof(self.path)

    def __str__(self):
        if (
            self.path is None
            or self.open is None
            or self.closed is None
            or self.wait is None
        ):
            return "La ricerca non è stata ancora eseguita."
        else:
            # Convert self.closed to a list and sort it by time
            # closed_sorted = sorted(list(self.closed), key=lambda state: state.time)
            # closed_str = [
            #     f"<{str(state)}, {self.f_score(state):.2f}>" for state in closed_sorted
            # ]
            return (
                f"## RISULTATO DELLA RICERCA\n"
                f"  * **Percorso trovato:** {self.path}\n"
                f"  * **Lunghezza del percorso trovato:** {self.path_length}\n"
                f"  * **Costo del percorso:** {self.path_cost: .2f}\n"
                # f"  * **Stati nella lista self.open:** {self.open}\n"
                # f"  * **Stati nella lista Closed:** {closed_str}\n"
                f"  * **Totale stati generati:** {self.total_states}\n"
                f"  * **Numero azioni Wait:** {self.wait}\n"
                f" **Percentuale di griglia visitata:** {self.percentage_visited_nodes:.2f}\n"
                f" **Nodi unici visitati:** {self.num_unique_node_visited}\n"
            )

    def calculate_num_unique_node_visited(self):
        nodes = list()
        if len(self.closed) == 0:
            return 0
        
        for state in self.closed:
            node = state.node
            if node not in nodes:
                nodes.append(node)
        return len(nodes)


class ReachGoal:
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
        # Assign the function to call to a variable
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
                return Result(
                    path=self.path,
                    path_cost=self.path_cost,
                    open=self.open,
                    closed=self.closed,
                    wait=self.wait,
                    use_variant=self.use_variant,
                    percentage_visited_nodes=self.calculate_visited_nodes(),
                    execution_time=self.__execution_time(),
                    mem_grid=sys.getsizeof(self.problem.grid),
                    mem_heuristic=sys.getsizeof(self.heuristic),
                )

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

        return Result(
            path=[self.problem.init],
            path_cost=math.inf,
            open=self.open,
            closed=self.closed,
            wait= 0,
            use_variant=self.use_variant,
            percentage_visited_nodes=self.calculate_visited_nodes(),
            execution_time=self.__execution_time(),
            mem_grid=sys.getsizeof(self.problem.grid),
            mem_heuristic=sys.getsizeof(self.heuristic),
        )

    def _ReachGoal_variant(self):
        predecessors = self.heuristic.predecessors
        f_score = lambda state: state.path_cost + self.heuristic(state.node)
        init = State(self.problem.init, 0)
        self.open = PriorityQueue(init, f=f_score)
        self.closed = set()

        if predecessors[init.node] is None:
            return Result(
                path=[self.problem.init],
                path_cost=math.inf,
                open=self.open,
                closed=self.closed,
                wait= 0,
                use_variant=self.use_variant,
                percentage_visited_nodes=self.calculate_visited_nodes(),
                execution_time=self.__execution_time(),
                mem_grid=sys.getsizeof(self.problem.grid),
                mem_heuristic=sys.getsizeof(self.heuristic),
            )

        while self.open:
            current_state = self.open.pop()
            time = current_state.time
            self.closed.add(current_state)

            if current_state.time > self.problem.maximum_time:
                return Result(
                    path=[init.node],
                    path_cost=math.inf,
                    open=self.open,
                    closed=self.closed,
                    wait= 0,
                    use_variant=self.use_variant,
                    percentage_visited_nodes=self.calculate_visited_nodes(),
                    execution_time=self.__execution_time(),
                    mem_grid=sys.getsizeof(self.problem.grid),
                    mem_heuristic=sys.getsizeof(self.heuristic),
                )

            if self.problem.is_goal(current_state.node):  # current_state[1] is the node
                self.path, self.wait = self.ReconstructPath(init, current_state)
                self.path_cost = current_state.path_cost
                return Result(
                    path=self.path,
                    path_cost=self.path_cost,
                    open=self.open,
                    closed=self.closed,
                    wait=self.wait,
                    use_variant=self.use_variant,
                    percentage_visited_nodes=self.calculate_visited_nodes(),
                    execution_time=self.__execution_time(),
                    mem_grid=sys.getsizeof(self.problem.grid),
                    mem_heuristic=sys.getsizeof(self.heuristic),
                )

            current_node = current_state.node
            path_free = is_path_free(self.problem, current_node, time, predecessors)

            if path_free:
                path_from_current = self.heuristic.return_path(
                    predecessors[current_state.node], self.problem.goal
                )
                path_to_current, self.wait = self.ReconstructPath(init, current_state)

                return Result(
                    path=path_to_current + path_from_current,
                    path_cost=current_state.path_cost
                    + self.heuristic.distances[current_state.node],
                    open=self.open,
                    closed=self.closed,
                    wait=self.wait,
                    use_variant=self.use_variant,
                    percentage_visited_nodes=self.calculate_visited_nodes(),
                    execution_time=self.__execution_time(),
                    mem_grid=sys.getsizeof(self.problem.grid),
                    mem_heuristic=sys.getsizeof(self.heuristic),
                )

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
        return Result(
            path=[self.problem.init],
            path_cost=math.inf,
            open=self.open,
            closed=self.closed,
            wait=0,
            use_variant=self.use_variant,
            percentage_visited_nodes=self.calculate_visited_nodes(),
            execution_time=self.__execution_time(),
            mem_grid=sys.getsizeof(self.problem.grid),
            mem_heuristic=sys.getsizeof(self.heuristic),
        )

    def calculate_visited_nodes(self):
        return (
            len(self.closed)
            / (self.problem.grid.get_size() - self.problem.grid.num_obstacles)
            * 100
        )
