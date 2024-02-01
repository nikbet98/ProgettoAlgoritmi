from state import State
from typing import Callable, Any
import heapq


class PriorityQueue:
    """
    Una coda prioritaria che mantiene gli elementi in ordine di priorità.
    Gli elementi vengono ordinati in base alla funzione di priorità specificata durante l'inizializzazione.
    """

    def __init__(self, item: State, f: Callable[[Any], Any] = lambda x: x):
        """
        Inizializza la coda prioritaria con lo stato iniziale e la funzione di priorità.
        La funzione di priorità viene utilizzata per calcolare la priorità di ogni elemento.
        L'elemento iniziale viene inserito nella coda con la sua priorità calcolata.
        """
        self.f = f
        self.queue = [(f(item), item)]  # lista di coppie (score,item)

    def add(self, item: State):
        """
        Aggiunge un elemento alla coda prioritaria.
        L'elemento viene inserito nella coda con la sua priorità calcolata.
        """
        pair = (self.f(item), item)
        heapq.heappush(self.queue, pair)

    def pop(self) -> State:
        """
        Rimuove e restituisce l'elemento con la priorità minima.
        """
        return heapq.heappop(self.queue)[1]

    def top(self) -> State:
        """
        Restituisce l'elemento con la priorità minima senza rimuoverlo dalla coda.
        Solleva un'eccezione se la coda è vuota.
        """
        if not self.queue:
            raise Exception(
                "Impossibile ottenere l'elemento in cima da una coda vuota."
            )
        return self.queue[0][1]

    def __len__(self) -> int:
        """
        Restituisce la lunghezza della coda prioritaria.
        """
        return len(self.queue)

    def __contains__(self, other: State) -> bool:
        """
        Verifica se la chiave è presente nella coda prioritaria.
        """
        return any([other == item for _, item in self.queue])

    def __getitem__(self, other: State) -> Any:
        """
        Restituisce il valore associato alla chiave nella coda prioritaria.
        Solleva un KeyError se la chiave non è presente.
        """
        for value, item in self.queue:
            if item == other:
                return value
        raise KeyError(str(other) + " non è presente nella coda prioritaria")

    def __delitem__(self, other: State):
        """
        Rimuove la prima occorrenza della chiave dalla coda prioritaria.
        Solleva un KeyError se la chiave non è presente.
        """
        try:
            del self.queue[[item == other for _, item in self.queue].index(True)]
        except ValueError:
            raise KeyError(str(other) + " non è presente nella coda prioritaria")
        heapq.heapify(self.queue)

    def __str__(self) -> str:
        """
        Restituisce una rappresentazione stringa della coda prioritaria.
        """
        if self.is_empty():
            return "La coda è vuota."

        sorted_queue = sorted(self.queue, key=lambda items: items[1].time)
        string = ", ".join(
            f"<{item[1].node}, {item[1].time}, {item[0]: .2f}>" for item in sorted_queue
        )
        return string

    def is_empty(self) -> bool:
        """
        Verifica se la coda prioritaria è vuota.
        """
        return len(self) == 0


# ________________________________________________________________


from typing import List, Tuple


def calculate_agent_locations(path: List[int], time: int) -> Tuple[int, int]:
    path_length = len(path) - 1
    if time >= path_length:
        node = next_node = path[-1]
    else:
        node = path[time]
        next_node = path[time + 1]
    return node, next_node


def is_free_collision(
    agent_paths: List[List[int]], node: int, next_node: int, time: int, cols: int
) -> bool:
    """
    Verifica se ci sono collisioni tra il percorso degli agenti e il nodo successivo.

    Args:
        agent_paths (List[List[int]]): Lista dei percorsi degli agenti.
        node (int): Nodo corrente.
        next_node (int): Nodo successivo.
        time (int): Tempo corrente.
        cols (int): Numero di colonne nella griglia.

    Returns:
        bool: True se non ci sono collisioni libere, False altrimenti.
    """
    for path in agent_paths:
        agent_location, agent_next_location = calculate_agent_locations(path, time)
        if check_collision(
            node,
            next_node,
            agent_location,
            agent_next_location,
            cols,
        ):
            return False
    return True


def check_collision(
    node: int, next_node: int, agent_location: int, agent_next_location: int, cols: int
) -> bool:
    return any(
        [
            agent_next_location == next_node,
            agent_next_location == node and agent_location == next_node,
            node - 1 == agent_next_location and agent_location == next_node,
            agent_location - cols == next_node and node - cols == agent_next_location,
            node == agent_next_location - 1 and agent_location == next_node - 1,
            node + cols == agent_next_location and agent_location + cols == next_node,
        ]
    )


def is_path_free(problem, node: int, time: int, predecessors: List[int]) -> bool:
    while time < problem.maximum_time:
        next_node = predecessors[node]
        if is_free_collision(problem.agent_paths, node, next_node, time, problem.cols):
            if problem.is_goal(next_node):
                return True
            node = next_node
            time += 1
        else:
            return False
    return False


def expand(problem, parent_state):
    time = parent_state.time

    for child_node, weight in problem.grid.get_adj_list(parent_state.node).items():
        pc = parent_state.path_cost
        cost = pc + weight
        yield State(child_node, time + 1, parent=parent_state, path_cost=cost)


def get_path_cost(path: List[int], grid) -> int:
    cost = 0
    edge_weights = {}
    for i in range(len(path) - 1):
        if (path[i], path[i + 1]) not in edge_weights:
            edge_weights[(path[i], path[i + 1])] = grid.get_edge_weight(
                path[i], path[i + 1]
            )
        cost += edge_weights[(path[i], path[i + 1])]
    return cost


def get_coordinates(node: int, col: int) -> Tuple[int, int]:
    x_node = (node) // col
    y_node = (node) % col
    return x_node, y_node


# Funzione per vedere se l'errore è stato causato dal tempo non sufficiente
def is_time_exceeded(max_time, closed_list, problem):
    unique_visited = calculate_unique_visited(closed_list)
    for state in closed_list:
        # prendo in considerazione solo gli stati al limite del tempo
        if state.time == max_time:
            neighborhood = expand(problem, state)
            # guardo se nel loro vicinato c'è qualche nodo che non è mai stato visitato
            for n in neighborhood:
                if n.node not in unique_visited:
                    return True
    return False


def calculate_unique_visited(closed):
    nodes = list()
    for state in closed:
        node = state.node
        if node not in nodes:
            nodes.append(node)
    return nodes
