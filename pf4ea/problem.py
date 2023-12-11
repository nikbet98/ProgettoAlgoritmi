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

        self.agents = Agents(maximum_time, num_agents)

        init, goal = random.sample(empty_nodes, 2)

        self.cols = cols
        self.init = init
        self.goal = goal
        self.num_agents = num_agents
        self.maximum_time = maximum_time
        self.traversability_ratio = traversability_ratio
        self.obstacle_agglomeration_ratio = obstacle_agglomeration_ratio

        self.agent_paths = self.agents.generate_paths(self.grid, empty_nodes)

    def __str__(self):
        parameters = [
            ("Dimensioni della griglia", f"{self.grid.rows}x{self.grid.cols}"),
            ("Traversabilità della griglia", self.traversability_ratio),
            ("Agglomerazione ostacoli", self.obstacle_agglomeration_ratio),
            ("Numero Agenti", self.num_agents),
            ("Tempo max", self.maximum_time),
            ("Nodo iniziale", self.init),
            ("Nodo Finale", self.goal)
        ]

        string = "## INFORMAZIONI SUL PROBLEMA\n| **Parametri** | Valori |\n| --- | --- |\n"
        for param, value in parameters:
            string += f"| **{param}** | {value} |\n"

        string += "\n **Percorso agenti**:\n"
        for i, path in enumerate(self.agent_paths, start=1):
            string += f"- Agente {i:02}: {path}\n"

        return string
    
    def info(self):
        parameters = [
            ("Dimensioni della griglia", f"{self.grid.rows}x{self.grid.cols}"),
            ("Traversabilità della griglia", self.traversability_ratio),
            ("Agglomerazione ostacoli", self.obstacle_agglomeration_ratio),
            ("Numero Agenti", self.num_agents),
            ("Tempo max", self.maximum_time),
            ("Nodo iniziale", self.init),
            ("Nodo Finale", self.goal)
        ]

        string = "## INFORMAZIONI SUL PROBLEMA\n+---------------------+---------+\n"
        for param, value in parameters:
            string += f"| {param} | {value} |\n"
        string += "+---------------------+---------+\n"
        return string
    
    def is_goal(self,node):
        return node == self.goal
        
