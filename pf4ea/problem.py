from typing import List, Tuple, Optional
import time
import random
from gridGraph import GridGraph
from agents import Agents


# Factory Pattern
class ProblemFactory:
    @staticmethod
    def create_problem(config):
        start_time = time.process_time()
        problem_instance = Problem(**config)
        problem_instance.execution_time = time.process_time() - start_time
        return problem_instance


class Problem:
    def __init__(
        self,
        rows: int,
        cols: int,
        traversability_ratio: float,
        obstacle_agglomeration_ratio: float,
        num_agents: int,
        maximum_time: int,
        init: Optional[int] = None,
        goal: Optional[int] = None,
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
        self.execution_time = None

    def _get_parameters(self) -> List[Tuple[str, float]]:
        parameters = [
            ("Dimensioni della griglia", f"{self.grid.rows}x{self.grid.cols}"),
            ("Traversabilità della griglia", self.traversability_ratio),
            ("Agglomerazione ostacoli", self.obstacle_agglomeration_ratio),
            ("Numero Agenti", self.num_agents),
            ("Tempo max", self.maximum_time),
            ("Nodo iniziale", self.init),
            ("Nodo Finale", self.goal),
        ]
        return parameters

    def __str__(self) -> str:
        string = (
            "## INFORMAZIONI SUL PROBLEMA\n| **Parametri** | Valori |\n| --- | --- |\n"
        )
        for param, value in self._get_parameters():
            string += f"| **{param}** | {value} |\n"

        string += "\n **Percorso agenti**:\n"
        for i, path in enumerate(self.agents.paths, start=1):
            string += f"- Agente {i:02}: {path}\n"

        return string

    def info(self) -> str:
        string = "## INFORMAZIONI SUL PROBLEMA\n+---------------------+---------+\n"
        for param, value in self._get_parameters():
            string += f"| {param} | {value} |\n"
        string += "+---------------------+---------+\n"
        return string

    def is_goal(self, node: int) -> bool:
        return node == self.goal
