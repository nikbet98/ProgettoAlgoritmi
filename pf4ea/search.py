from collections import deque
import math
import time
from state import State
from utils import PriorityQueue, expand, is_free_collision, is_path_free
from gridGraph import GridGraph



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

    def search(self):
        # Assign the function to call to a variable
        search_algorithm = self._ReachGoal_variant if self.use_variant else self._ReachGoal
        return self._measure_time(search_algorithm)

    def _measure_time(self, algorithm):
        start_time = time.time()
        solution = algorithm()
        elapsed_time = time.time() - start_time
        return solution, elapsed_time


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


    def _ReachGoal(self):
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
                return self.path

            for child_state in expand(self.problem, current_state):
                if child_state not in self.closed:
                    current_node = current_state.node
                    child_node = child_state.node

                    # check if the path is traversable
                    traversable = is_free_collision(self.problem.agent_paths, current_node, child_node, time, self.problem.cols)

                    if traversable:
                        if child_state not in self.open:
                            self.open.add(child_state)
                        elif f_score(child_state) < self.open[child_state]:
                            del self.open[child_state]
                            self.open.add(child_state)

        return self.path

    def _ReachGoal_variant(self):
        predecessors = self.heuristic.predecessors

        wait = 0

        f_score = lambda state: state.path_cost+ self.heuristic(state.node)

        init = State(self.problem.init, 0)
        self.open = PriorityQueue(init, f=f_score)
        self.closed = set()

        while self.open:
            current_state = self.open.pop()
            time = current_state.time
            self.closed.add(current_state)
            if (not current_state.is_parent_None()) and (current_state.node == current_state.parent.node):
                wait += 1

            if current_state.time > self.problem.maximum_time:
                return None, len(self.open), len(self.closed), wait

            if self.problem.is_goal(current_state.node):  # current_state[1] is the node
                self.path_cost = current_state.path_cost
                return self.path

            current_node = current_state.node
            path_free = is_path_free(self.problem, current_node, time, predecessors)

            if path_free:
                path_from_current = self.heuristic.return_path(
                    predecessors[current_state.node], self.problem.goal
                )
                path_to_current, wait = self.ReconstructPath(init, current_state)

                return path_to_current + path_from_current, len(self.open), len(self.closed), wait

            for child_state in expand(self.problem, current_state):
                if child_state not in self.closed:
                    current_node = child_state.node
                    child_node = current_state.node
                    # check if the path is traversable
                    traversable = is_free_collision(self.problem.agent_paths, current_node, child_node, time, self.problem.cols)

                    if traversable:
                        if child_state not in self.open:
                            self.open.add(child_state)
                        elif f_score(child_state) < self.open[child_state]:
                            del self.open[child_state]
                            self.open.add(child_state)
        return None, len(self.open), len(self.closed), wait


    def __str__(self):
        if self.path is None or self.open is None or self.closed is None or self.wait is None:
            return "La ricerca non è stata ancora eseguita."
        else:
            # Convert self.closed to a list and sort it by time
            closed_sorted = sorted(list(self.closed), key=lambda state: state.time)
            closed_str = [f"<{str(state)}, {self.f_score(state):.2f}>" for state in closed_sorted]            
            return  (f"## RISULTATO DELLA RICERCA\n"
                    f"  * **Percorso trovato:** {self.path}\n"
                    f"  * **Lunghezza del percorso trovato:** {len(self.path)}\n"
                    f"  * **Costo del percorso:** {self.path_cost: .2f}\n"
                    f"  * **Stati nella lista self.open:** {self.open}\n"
                    f"  * **Stati nella lista Closed:** {closed_str}\n"
                    f"  * **Totale stati generati:** {str(len(self.open) + len(self.closed))}\n"
                    f"  * **Numero azioni Wait:** {self.wait}\n")
                    f" **Percentuale di nodi visitati:** {self.percentage_visited_nodes:.2f}%\n"
            )
            
        