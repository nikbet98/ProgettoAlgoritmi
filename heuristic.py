import math
import heapq
from abc import ABC, abstractmethod


class Heuristic(ABC):

    def __init__(self, grid, goal):
        self.grid = grid
        self.goal = goal

    @abstractmethod
    def __call__(self, node):
        pass


class DiagonalDistance(Heuristic):
    def __init__(self, grid, goal):
        super().__init__(grid, goal)
        self.diagonals = self.get_estimates()

    def get_estimates(self):
        diagonals = []
        for node in self.grid.get_nodes():
            diagonals.append(self.diagonal_distance(node))
        return diagonals

    def estimates(self, node):
        node_id = node.get_id()
        goal_id = self.goal.get_id()
        x_node = node_id // self.cols
        y_node = node_id % self.cols
        x_goal = goal_id // self.cols
        y_goal = goal_id % self.cols

        dx = abs(x_node - x_goal)
        dy = abs(y_node - y_goal)
        return dx + dy + (math.sqrt(2) - 2) * min(dx, dy)

    def __call__(self, node):
        return self.estimates[node.get_id()]

class BackwardDijkstra(Heuristic):
    def __init__(self, grid, goal):
        super().__init__(grid, goal)
        distances = self.get_estimate()


    def get_estimate(self):
        # Inizializzazione dei valori dei nodi
        distances = {node: float('inf') for node in graph.nodes}
        distances[goal] = 0

        # Inizializzazione della coda di priorità
        pq = [(0, goal)]

        while pq:
            # Estrazione del nodo con la distanza minima
            current_distance, current_node = heapq.heappop(pq)

            # Se la distanza estratta è maggiore della distanza attuale, ignorare il nodo
            if current_distance > distances[current_node]:
                continue

            # Aggiornamento delle distanze dei nodi adiacenti
            for neighbor,_ in graph.get_adj_list(current_node).items():
                distance = current_distance + 1
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
        print(distances)
        return distances
    
    def __call__(self, node):
        return self.distances[node.get_id()]
    

""" DA QUI IN POI E' DA SISTEMARE"""
    def __init__(self, grid, goal):
        super().__init__(grid, goal)
        self.dikstra = []
        for node in self.grid.get_nodes():
            self.dikstra.append(self.dikstra_distance(node))

    def dikstra_distance(self, node):
        node_id = node.get_id()
        goal_id = self.goal.get_id()
        x_node = node_id // self.cols
        y_node = node_id % self.cols
        x_goal = goal_id // self.cols
        y_goal = goal_id % self.cols

        dx = abs(x_node - x_goal)
        dy = abs(y_node - y_goal)
        return dx + dy

    def __call__(self, node):
        return self.dikstra[node.get_id()]
class EuclideanDistance(Heuristic):

    def __init__(self, grid, goal):
        super().__init__(grid, goal)

    def __call__(self, node):
        node_id = node.get_id()
        goal_id = self.goal.get_id()
        x_node = node_id // self.cols
        y_node = node_id % self.cols
        x_goal = goal_id // self.cols
        y_goal = goal_id % self.cols

        dx = abs(x_node - x_goal)
        dy = abs(y_node - y_goal)
        return math.sqrt(dx**2 + dy**2)


class ManhattanDistance(Heuristic):
    def __init__(self, grid, goal):
        super().__init__(grid, goal)

    def __call__(self, node):
        pass
