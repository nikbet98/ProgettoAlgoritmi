import math
import heapq
from abc import ABC, abstractmethod
from utils import get_coordinates

# costanti
WEIGHT_CARDINAL_DIRECTION = 1
WEIGHT_DIAGONAL_DIRECTION = math.sqrt(2)


HEURISTIC_CLASSES = {
    "h1": "DiagonalDistance",
    "h2": "ChebyshevDistance",
    "h3": "ManhattanDistance",
    "h4": "EuclideanDistance",
    "h5": "HeuristicRelaxPath",
    "h6": "BackwardDijkstra2"
}

class Heuristic(ABC):

    def __init__(self, grid, goal):
        self.grid = grid
        self.goal = goal

    @abstractmethod
    def __call__(self, node):
        pass

# -------------------------------------------------------------------------------- #

# ---------------------------------- Euristiche ---------------------------------- #
class DiagonalDistance(Heuristic):
    def __init__(self, grid, goal):
        super().__init__(grid, goal)
        self.col = self.grid.get_dim()[1]
        self.D = WEIGHT_CARDINAL_DIRECTION
        self.D2 = WEIGHT_DIAGONAL_DIRECTION
        self.goal = goal

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
        x_goal, y_goal = get_coordinates(self.goal, self.col)

        dx = abs(x_init-x_goal)
        dy = abs(y_init-y_goal)
        return self.D*(dx+dy) + (self.D2 - 2*self.D)*min(dx,dy)

    def __call__(self, init):
        return self.estimate(init)


class ChebyshevDistance(Heuristic):
    def __init__(self, grid, goal,D):
        super().__init__(grid, goal)
        self.col = self.grid.get_dim()[1]
        self.D = D
    
    def estimate(self, init):
        """
        param goal: nodo di arrivo
        param D: costo per movimento cardinale
        param D2: costo per movimento diagonale
        return: euristica secondo la formula diagonale
        """
        x_init, y_init = get_coordinates(init, self.col)
        x_goal, y_goal = get_coordinates(self.goal, self.col)

        dx = abs(x_init-x_goal)
        dy = abs(y_init-y_goal)
        return self.D*(dx+dy) + (self.D2 - 2*self.D)*min(dx,dy)    

    def __call__(self, node):
        return self.estimate(node)
    
class ManhattanDistance(Heuristic):
    def __init__(self, grid, goal,D):
        super().__init__(grid, goal)
        self.col = self.grid.get_dim()[1]
        self.D = D
    
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

        dx = abs(x_init-x_goal)
        dy = abs(y_init-y_goal)

        return self.D*(dx + dy)

    def __call__(self, init):
        return self.estimate(init)

class EuclideanDistance(Heuristic):
    def __init__(self, grid, goal,D):
        super().__init__(grid, goal)
        self.col = self.grid.get_dim()[1]
        self.D = D
    
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
        x_goal, y_goal = get_coordinates(self.goal, self.col)

        dx = abs(x_init-x_goal)
        dy = abs(y_init-y_goal)

        return self.D*math.sqrt(dx^2 + dy^2)
        
    def __call__(self, init):
        return self.estimate(init)

class HeuristicRelaxPath(Heuristic):
    def __init__(self, grid, goal):
        super().__init__(grid, goal)
        self.distances = None
        self.predecessors = None
        self.estimates()

    def estimates(self):
        # Inizializzazione dei valori dei nodi
        distances = {node: float('inf') for node in self.grid.nodes}
        distances[self.goal] = 0
        predecessors = {node: None for node in self.grid.nodes}

        # Inizializzazione della coda di priorità
        pq = [(0, self.goal)]

        while pq:
            # Estrazione del nodo con la distanza minima
            current_distance, current_node = heapq.heappop(pq)

            # Se la distanza estratta è maggiore della distanza attuale, ignorare il nodo
            if current_distance > distances[current_node]:
                continue

            # Aggiornamento delle distanze dei nodi adiacenti
            for neighbor,_ in self.grid.get_adj_list(current_node).items():
                distance = current_distance + self.grid.get_edge_weight(current_node, neighbor)
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
        
        self.__setattr__('distances',distances)
        self.__setattr__('predecessors',predecessors)
    
    def return_path(self,starting_node, end_node, path=list()):
        while starting_node != end_node:
            path.append(starting_node)
            return self.return_path(self.predecessors[starting_node], end_node, path)
        path.append(end_node)
        return path
    
    def __call__(self, node):
        return self.distances[node]
    
    def get_predecessors(self):
        return self.predecessors
    
    def relaxed_path(self,node):
        # Ricostruzione del percorso rilassato dal nodo corrente al nodo obiettivo
        path = []
        while node != self.goal:
            path.append(node)
            node = self.predecessors[node]
        path.append(self.goal)
        path.reverse()
        return path

class BackwardDijkstra(Heuristic):
    def __init__(self, grid, goal):
        super().__init__(grid, goal)
        self.distances = None
        self.predecessors = None


    def estimates(self):
        # Inizializzazione dei valori dei nodi
        distances = {node: float('inf') for node in self.grid.nodes}
        distances[self.goal] = 0
        self. predecessors = {node: None for node in self.grid.nodes}

        # Inizializzazione della coda di priorità
        pq = [(0, self.goal)]

        while pq:
            # Estrazione del nodo con la distanza minima
            current_distance, current_node = heapq.heappop(pq)

            # Se la distanza estratta è maggiore della distanza attuale, ignorare il nodo
            if current_distance > distances[current_node]:
                continue

            # Aggiornamento delle distanze dei nodi adiacenti
            for neighbor,_ in self.grid.get_adj_list(current_node).items():
                distance = current_distance + 1
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
        print(distances)
        self.__setattr__('distances',distances)
    
    def __call__(self, node):
        return self.distances[node]