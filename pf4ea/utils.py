import heapq
from state import State


class PriorityQueue:
    """
    Una coda prioritaria che mantiene gli elementi in ordine di priorità.
    Gli elementi vengono ordinati in base alla funzione di priorità specificata durante l'inizializzazione.
    """

    def __init__(self, state, f=lambda x: x):
        """
        Inizializza la coda prioritaria con lo stato iniziale e la funzione di priorità.
        La funzione di priorità viene utilizzata per calcolare la priorità di ogni elemento.
        L'elemento iniziale viene inserito nella coda con la sua priorità calcolata.
        """
        self.f = f
        self.queue = [(f(state), state)]  # lista di coppie (score,item)

    def add(self, item):
        """
        Aggiunge un elemento alla coda prioritaria.
        L'elemento viene inserito nella coda con la sua priorità calcolata.
        """
        pair = (self.f(item), item)
        heapq.heappush(self.queue, pair)

    def pop(self):
        """
        Rimuove e restituisce l'elemento con la priorità minima.
        """
        return heapq.heappop(self.queue)[1]

    def top(self):
        """
        Restituisce l'elemento con la priorità minima senza rimuoverlo dalla coda.
        """
        return self.queue[0][1]

    def __len__(self):
        """
        Restituisce la lunghezza della coda prioritaria.
        """
        return len(self.queue)

    def __contains__(self, key):
        """
        Verifica se la chiave è presente nella coda prioritaria.
        """
        return any([item == key for _, item in self.queue])

    def __getitem__(self, other):
        """
        Restituisce il valore associato alla chiave nella coda prioritaria.
        Solleva un KeyError se la chiave non è presente.
        """
        for value, item in self.queue:
            if item == other:
                return value
        raise KeyError(str(other) + " non è presente nella coda prioritaria")

    def __delitem__(self, key):
        """
        Rimuove la prima occorrenza della chiave dalla coda prioritaria.
        Solleva un KeyError se la chiave non è presente.
        """
        try:
            del self.queue[[item == key for _, item in self.queue].index(True)]
        except ValueError:
            raise KeyError(str(key) + " non è presente nella coda prioritaria")
        heapq.heapify(self.queue)

    def __str__(self):
        """
        Restituisce una rappresentazione stringa della coda prioritaria.
        """
        if self.is_empty():
            return "La coda è vuota."
        
        sorted_queue = sorted(self.queue, key=lambda items: items[1].time)
        string = ", ".join(
            f"<{item[1].node}, {item[1].time}, {item[0]}>" for item in sorted_queue
        )
        return string
    def is_empty(self):
        """
        Verifica se la coda prioritaria è vuota.
        """
        return len(self) == 0


# ________________________________________________________________


def calculate_agent_positions(agent_path, time):
    path_length = len(agent_path) - 1
    # controllo se il è già arrivato alla fine l'altro agente
    if path_length < time or path_length < time + 1:
        agent_current_node = agent_path[-1]
        agent_next_node = agent_current_node
    else:
        agent_current_node = agent_path[time]
        agent_next_node = agent_path[time + 1]
    return agent_current_node, agent_next_node


def is_collision_free(paths, current_node, next_node, time, cols):
    """
    Verifica se il prossimo nodo scelto è privo di collisioni con gli agenti presenti nel problema.

    Args:
        problem (Problem): L'istanza del problema.
        current_node (Node): Il nodo corrente del percorso.
        next_node (Node): Il nodo successivo del percorso.
        time (int): Il tempo corrente.

    Returns:
        bool: True se il percorso è privo di collisioni, False altrimenti.
    """
    for agent_path in paths:
        agent_current_position, agent_next_position = calculate_agent_positions(
            agent_path, time
        )
        if check_collision(
                current_node,
                next_node,
                agent_current_position,
                agent_next_position,
                cols,
        ):
            return False

    return True


def check_collision(
        current_node, next_node, current_position, next_position, grid_cols
):
    """
    Verifica se si verifica una collisione tra due nodi nel grid.

    Parametri:
    - current_node: Il nodo corrente.
    - next_node: Il nodo successivo.
    - current_position: La posizione corrente.
    - next_position: La posizione successiva.
    - grid_cols: Il numero di colonne nel grid.

    Restituisce:
    - True se si verifica una collisione, False altrimenti.
    """
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


def is_free_path(problem, current_node, time, predecessors):
    """
    Verifica se esiste un percorso libero nel problema specificato, partendo dal nodo corrente.

    Args:
        problem (Problem): L'istanza del problema.
        current_node (int): Il nodo corrente.
        time (int): Il tempo corrente.
        predecessors (dict): Un dizionario che mappa ogni nodo al suo predecessore nel percorso.

    Returns:
        bool: True se esiste un percorso libero fino al nodo obiettivo, False altrimenti.
    """
    if time > problem.maximum_time:
        return False
    next_node = predecessors[current_node]
    if is_collision_free(problem.agent_paths, current_node, next_node, time, problem.cols):
        if next_node == problem.goal:
            return True
        else:
            return is_free_path(problem, next_node, time + 1, predecessors)


def expand(problem, parent_state):
    """
    Ritorna una lista di nodi raggiungibili da un nodo genitore.

    Args:
        problem: l'oggetto che rappresenta il problema da risolvere.
        parent_state: lo stato genitore da cui espandere i nodi.

    Yields:
        Stati figli raggiungibili dal nodo genitore.
    """
    time = parent_state.time

    for child_node, weight in problem.grid.get_adj_list(
            parent_state.node
    ).items():
        # test
        pc = parent_state.path_cost
        cost = pc + weight
        yield State(child_node, time + 1, parent=parent_state, path_cost=cost)
    # ritorno lo stato padre


def get_path_cost(path, grid):
    cost = 0
    for i in range(len(path) - 1):
        cost = cost + grid.get_edge_weight(path[i], path[i + 1])

    return cost


# ---------------------------------------------------------------
def get_coordinates(node,col):
    """
    get_coordinates: funzione per ottenere le coordinate di un certo nodo nella griglia
    param node: nodo di cui ci interessano le coordinate
    param col: colonne della griglia
    return: coordinate x,y del nodo
    """
    x_node = (node)//col
    y_node = (node)% col
    return x_node, y_node