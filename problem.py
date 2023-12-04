import random
from gridGraph import GridGraph
from agents import Agents


class Problem:
    """
    Rappresenta un problema di ricerca su un grafo.

    Args:
        rows (int): Il numero di righe del grafo.
        cols (int): Il numero di colonne del grafo.
        traversability_ratio (float): La percentuale di nodi attraversabili nel grafo.
        obstacle_agglomeration_ratio (float): La percentuale di agglomerazione degli ostacoli nel grafo.
        num_agents (int): Il numero di agenti presenti nel problema.
        maximum_time (int): Il tempo massimo disponibile per completare il problema.

    Attributes:
        graph (GridGraph): Il grafo su cui viene eseguita la ricerca.
        agent_paths (list): La lista dei percorsi degli agenti generati.

    """

    def __init__(
            self,
            rows,
            cols,
            traversability_ratio,
            obstacle_agglomeration_ratio,
            num_agents,
            maximum_time,
            init=None,
            goal=None
    ):
        self.grid = GridGraph(
            rows, cols, traversability_ratio, obstacle_agglomeration_ratio
        )
        empty_nodes = self.grid.get_free_nodes()

        agents = Agents(maximum_time, num_agents)

        init, goal = random.sample(empty_nodes, 2)

        self.cols = cols
        self.init = init
        self.goal = goal
        self.num_agents = num_agents
        self.maximum_time = maximum_time
        self.traversability_ratio = traversability_ratio
        self.obstacle_agglomeration_ratio = obstacle_agglomeration_ratio

        self.agent_paths = agents.generate_paths(self.grid, empty_nodes)

    def print_info(self):
        out = ("Dimensioni della griglia: " + str(self.grid.rows) + "x" + str(self.grid.cols) + '\n'
               + "Traversabilità della griglia: " + str(self.traversability_ratio) + '\n'
               + "Agglomerazione ostacoli: " + str(self.obstacle_agglomeration_ratio) + '\n'
               + "Numero Agenti: " + str(self.num_agents) + '\n'
               + "Percorso agenti:" + '\n'
               + self.print_agents_path()
               + "Tempo max: " + str(self.maximum_time) + '\n'
               + "Nodo iniziale: " + str(self.init) + '\n'
               + "Nodo Finale: " + str(self.goal)+ '\n')
        return out

    def print_agents_path(self):
        out = ""
        for path in self.agent_paths:
            out = out + str(path) + '\n'
        return out
