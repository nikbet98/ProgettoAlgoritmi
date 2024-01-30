from dataclasses import dataclass
from typing import List, Optional
from constants import SearchFailureCodes
from utils import PriorityQueue, calculate_unique_visited, is_time_exceeded


import math
import sys
NOT_ENOUGH_TIME = "tempo non sufficiente"
NO_SOL_ERROR = "non esiste un soluzione"

class ResultFactory:
    @staticmethod
    def create_result(search_result, execution_time):
        path = [search_result.problem.init]
        path_cost = math.inf
        wait = 0

        if search_result.path is not None:
            path = search_result.path
            path_cost = search_result.path_cost
            wait = search_result.wait

        result_init_args = {
            "path": path,
            "path_cost": path_cost,
            "open": search_result.open,
            "closed": search_result.closed,
            "wait": wait,
            "use_variant": search_result.use_variant,
            "percentage_visited_nodes": search_result.calculate_visited_nodes(),
            "num_unique_node_visited" : len(calculate_unique_visited(search_result.closed)),
            "execution_time": execution_time(),
            "mem_grid": sys.getsizeof(search_result.problem.grid),
            "mem_heuristic": sys.getsizeof(search_result.heuristic),
            "mem_open": sys.getsizeof(search_result.open),
            "mem_closed": sys.getsizeof(search_result.closed),
            "mem_path": sys.getsizeof(search_result.path),
        }

        if search_result.path is None:
            result_init_args["failure_code"] = SearchFailureCodes.NO_SOLUTION_FOUND
        elif is_time_exceeded(search_result.problem.maximum_time, search_result.closed, search_result.problem):
            result_init_args["failure_code"] = SearchFailureCodes.TIME_EXCEEDED
        else:
            result_init_args["failure_code"] = SearchFailureCodes.NO_FAILURE

        return Result(**result_init_args)
    

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
    num_unique_node_visited: Optional[int] 
    path_length: int = None
    total_states: int = None
    mem_grid: float = None
    mem_heuristic: float = None
    mem_open: float = None
    mem_closed: float = None
    mem_path: float = None
    failure_code: int = SearchFailureCodes.NO_FAILURE

    # def __post_init__(self):
    #     self.path_length = len(self.path)
    #     self.num_unique_node_visited = self.calculate_num_unique_node_visited()
    #     self.total_states = len(self.open) + len(self.closed)
    #     self.mem_open = sys.getsizeof(self.open)
    #     self.mem_closed = sys.getsizeof(self.closed)
    #     self.mem_path = sys.getsizeof(self.path)

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

            headers = {
                SearchFailureCodes.NO_SOLUTION_FOUND: (
                    f"## RISULTATO DELLA RICERCA: SOLUZIONE NON TROVATA\n"
                    f"  * **Percorso trovato:** {NO_SOL_ERROR}\n"
                    f"  * **Lunghezza del percorso trovato:** INF\n"
                    f"  * **Costo del percorso:** INF\n"
                ),
                SearchFailureCodes.TIME_EXCEEDED: (
                    f"## RISULTATO DELLA RICERCA: SOLUZIONE NON TROVATA\n"
                    f"  * **Percorso trovato:** {NOT_ENOUGH_TIME}\n"
                    f"  * **Lunghezza del percorso trovato:** INF\n"
                    f"  * **Costo del percorso:** INF\n"
                ),
                SearchFailureCodes.NO_FAILURE: (
                    f"## RISULTATO DELLA RICERCA: SOLUZIONE TROVATA\n"
                    f"  * **Percorso trovato:** {self.path}\n"
                    f"  * **Lunghezza del percorso trovato:** {self.path_length}\n"
                    f"  * **Costo del percorso:** {self.path_cost: .2f}\n"
                ),
            }

            return (
                headers[self.failure_code] +
                f"  * **Totale stati generati:** {self.total_states}\n"
                f"  * **Numero azioni Wait:** {self.wait}\n"
                f"  * **Percentuale di griglia visitata:** {self.percentage_visited_nodes:.2f}\n"
                f"  * **Nodi unici visitati:** {self.num_unique_node_visited}\n"
            )

    def calculate_num_unique_node_visited(self):
        if len(self.closed) == 0:
            return 0
        unique = calculate_unique_visited(self.closed)
        return len(unique)


