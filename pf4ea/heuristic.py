from abc import ABC, abstractmethod
from collections import deque
from constants import *
import heapq
import math
from utils import get_coordinates
import time


class HeuristicFactory:
    @staticmethod
    def create_heuristic(problem, heuristic_type, HEURISTIC_CLASSES):
        if heuristic_type not in HEURISTIC_CLASSES:
            raise ValueError(f"Unsupported heuristic type: {heuristic_type}")

        start_time = time.process_time()
        heuristic_instance = HEURISTIC_CLASSES[heuristic_type](
            problem.grid, problem.goal
        )
        heuristic_instance.execution_time = time.process_time() - start_time

        return heuristic_instance


class Heuristic(ABC):
    def __init__(self, grid, goal):
        self.grid = grid
        self.goal = goal
        self.execution_time = None

    @abstractmethod
    def __call__(self, node):
        pass


# ---------------------------------- Euristiche ---------------------------------- #
class DiagonalDistance(Heuristic):
    def __init__(self, grid, goal):
        super().__init__(grid, goal)
        self.col = self.grid.get_dim()[1]
        self.D = WEIGHT_CARDINAL_DIRECTION
        self.D2 = WEIGHT_DIAGONAL_DIRECTION
        self.goal = goal
        self.x_goal, self.y_goal = get_coordinates(self.goal, self.col)

    def estimate(self, init):
        """
        diagonal: calcola la distanza diagonale
        param col: colonne della griglia
        param init: nodo di partenza
        param goal: nodo di arrivo
        param D: costo per movimento cardinale
        param D2: costo per movimento diagonale
        return: euristica secondo la formula diagonale
        """
        x_init, y_init = get_coordinates(init, self.col)

        dx = abs(x_init - self.x_goal)
        dy = abs(y_init - self.y_goal)
        return self.D * (dx + dy) + (self.D2 - 2 * self.D) * min(dx, dy)

    def __call__(self, init):
        return self.estimate(init)


class ChebyshevDistance(Heuristic):
    def __init__(self, grid, goal):
        super().__init__(grid, goal)
        self.col = self.grid.get_dim()[1]
        self.x_goal, self.y_goal = get_coordinates(self.goal, self.col)
        self.D = WEIGHT_CARDINAL_DIRECTION
        self.D2 = WEIGHT_DIAGONAL_DIRECTION

    def estimate(self, init):
        """
        param goal: nodo di arrivo
        param D: costo per movimento cardinale
        param D2: costo per movimento diagonale
        return: euristica secondo la formula diagonale
        """
        x_init, y_init = get_coordinates(init, self.col)

        dx = abs(x_init - self.x_goal)
        dy = abs(y_init - self.y_goal)
        return self.D * (dx + dy) + (self.D2 - 2 * self.D) * min(dx, dy)

    def __call__(self, node):
        return self.estimate(node)


class ManhattanDistance(Heuristic):
    def __init__(self, grid, goal):
        super().__init__(grid, goal)
        self.col = self.grid.get_dim()[1]
        self.x_goal, self.y_goal = get_coordinates(self.goal, self.col)
        self.D = WEIGHT_CARDINAL_DIRECTION

    def estimate(self, init):
        """
        manhattam: calcola la distanza di manhattam
        param col: colonne della griglia
        param init: nodo di partenza
        param goal: nodo di arrivo
        param D: costo per movimento cardinale
        return: euristicaa secondo la formula di manhattam
        """
        x_init, y_init = get_coordinates(init, self.col)
        x_goal, y_goal = get_coordinates(self.goal, self.col)

        dx = abs(x_init - self.x_goal)
        dy = abs(y_init - self.y_goal)

        return self.D * (dx + dy)

    def __call__(self, init):
        return self.estimate(init)


class EuclideanDistance(Heuristic):
    def __init__(self, grid, goal):
        super().__init__(grid, goal)
        self.col = self.grid.get_dim()[1]
        self.D = WEIGHT_CARDINAL_DIRECTION
        self.x_goal, self.y_goal = get_coordinates(self.goal, self.col)

    def estimate(self, init):
        """
        Calcola la distanza euclidea
        param col: colonne della griglia
        param init: nodo di partenza
        param goal: nodo di arrivo
        param D: costo per movimento cardinale
        return: euristica secondo la formula euclidea
        """

        x_init, y_init = get_coordinates(init, self.col)
        dx = abs(x_init - self.x_goal)
        dy = abs(y_init - self.y_goal)

        return self.D * math.sqrt(dx ^ 2 + dy ^ 2)

    def __call__(self, init):
        return self.estimate(init)


# -------------------------------------------------------------------------------- #
class HeuristicRelaxPath(Heuristic):
    def __init__(self, grid, goal):
        super().__init__(grid, goal)
        self.distances, self.predecessors = self.estimates()

    def estimates(self):
        # Inizializzazione dei valori dei nodi
        distances = {node: float("inf") for node in self.grid.nodes}
        distances[self.goal] = 0
        predecessors = {node: None for node in self.grid.nodes}
        pq = [(0, self.goal)]

        while pq:
            current_distance, current_node = heapq.heappop(pq)
            if current_distance > distances[current_node]:
                continue

            # Aggiornamento delle distanze dei nodi adiacenti
            adj_list = self.grid.get_adj_list(current_node)
            for neighbor, _ in adj_list.items():
                distance = current_distance + self.grid.get_edge_weight(
                    current_node, neighbor
                )
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
        return distances, predecessors

    def return_path(self, starting_node, end_node):
        path = []
        while starting_node != end_node:
            path.append(starting_node)
            starting_node = self.predecessors[starting_node]
        path.append(end_node)
        return path

    def __call__(self, node):
        return self.distances[node]

    def relaxed_path(self, node):
        """
        Ricostruzione del percorso rilassato dal nodo corrente al nodo obiettivo
        """
        path = deque()
        while node != self.goal:
            path.appendleft(node)
            node = self.predecessors[node]
        path.appendleft(self.goal)
        return list(path)


class BackwardDijkstra(Heuristic):
    def __init__(self, grid, goal):
        super().__init__(grid, goal)
        self.distances, self.predecessors = self.estimates()

    def estimates(self):
        distances = {node: float("inf") for node in self.grid.nodes}
        distances[self.goal] = 0
        predecessors = {node: None for node in self.grid.nodes}
        pq = [(0, self.goal)]

        while pq:
            current_distance, current_node = heapq.heappop(pq)
            if current_distance > distances[current_node]:
                continue
            adj_list = self.grid.get_adj_list(current_node)
            for neighbor, _ in adj_list.items():
                distance = current_distance + 1
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        return distances, predecessors

    def __call__(self, node):
        return self.distances[node]
