import math
import random
from constants import *
from typing import Dict, List, Optional, Set, Tuple


class GridGraph:
    def __init__(self, rows: int, cols: int, traversability_ratio: float, obstacle_agglomeration_ratio: float):
        """
        Inizializza una griglia di nodi con le dimensioni specificate.
        :param rows: Il numero di righe della griglia.
        :param cols: Il numero di colonne della griglia.
        :param traversability_ratio: La percentuale di attraversabilità della griglia.
        :param obstacle_agglomeration_ratio: La percentuale di agglomerazione degli ostacoli nella griglia.
        """

        self.rows = rows
        self.cols = cols
        self.size = rows * cols
        self.traversability_ratio = traversability_ratio

        self.obstacle_agglomeration_ratio = obstacle_agglomeration_ratio
        self.nodes: List[int] = list(range(0, self.size))
        self.adj_list: List[Dict[int, float]] = [{} for node in self.nodes]
        self.num_obstacles = self.calculate_num_obstacles()
        self.generate_neighbors()
        self.generate_obstacles()

    def generate_neighbors(self):
        """
        Genera gli elenchi di adiacenza per ogni nodo nella griglia.
        """
        for current_node in self.nodes:
            self.connect_adjacent_nodes(current_node)

    def connect_adjacent_nodes(self, node: int):
        """
        Connette il nodo specificato ai suoi nodi adiacenti nella griglia.
        """
        row = (node) // self.cols
        col = (node) % self.cols

        # Definisco le direzioni dei nodi
        directions = [
            (-1, 0),  # nord
            (1, 0),  # sud
            (0, -1),  # ovest
            (0, 1),  # est
            (-1, -1),  # nord-ovest
            (-1, 1),  # nord-est
            (1, -1),  # sud-ovest
            (1, 1),  # sud-est
        ]

        # connetto i nodi adiacenti in base alle direzioni
        for direction_row, direction_col in directions:
            new_row, new_col = row + direction_row, col + direction_col
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                neighbor = new_row * self.cols + new_col
                weight = WEIGHT_CARDINAL_DIRECTION
                if direction_row != 0 and direction_col != 0:  # ci stiamo muovendo in diagonale
                    weight = WEIGHT_DIAGONAL_DIRECTION
                self.add_edge(node, neighbor, weight)
        self.add_edge(node, node, WEIGHT_CARDINAL_DIRECTION)

    def generate_obstacles(self):
        """
        Genera gli ostacoli nella griglia in base alla percentuale di attraversabilità e di agglomerazione degli ostacoli.
        """
        if self.num_obstacles != 0:  # se il numero di ostacoli è nullo non tentare di generare gli ostacoli
            obstacles = self.build_obstacles()
            for node in obstacles:
                self.set_as_obstacle(node)

    def calculate_num_obstacles(self) -> int:
        return round(self.size * (1 - self.traversability_ratio))

    def build_obstacles(self) -> Set[int]:
        """
        Genera gli ostacoli nella griglia in base alla percentuale di agglomerazione degli ostacoli.
        """
        obstacles: Set[int] = set()
        cluster_size = self.calculate_cluster_size()
        num_clusters = self.calculate_num_clusters(cluster_size)
        for i in range(num_clusters):
            start = self.find_start_node(obstacles)
            if start is not None:
                cluster = self.generate_obstacle_cluster(cluster_size, obstacles, cluster=[start])
                obstacles.update(cluster)
        return obstacles

    def calculate_cluster_size(self) -> int:
        if self.obstacle_agglomeration_ratio == 0:
            return 1
        return math.ceil(self.num_obstacles * self.obstacle_agglomeration_ratio)
        # return round(self.num_obstacles * self.obstacle_agglomeration_ratio)

    def calculate_num_clusters(self, cluster_size: int) -> int:
        if cluster_size == 1:
            return self.num_obstacles
        return round(self.num_obstacles / cluster_size)

    def find_start_node(self, obstacles: Set[int]) -> int:
        """
        Trova un nodo di partenza per generare un nuovo cluster di ostacoli.
        """
        available = [node for node in self.nodes if
                     node not in obstacles and self.are_neighbors_obstacle_free(node, obstacles)]
        if not available:
            return None
        start = random.choice(available)
        return start

    def are_neighbors_obstacle_free(self, node: int, obstacles: Set[int]) -> bool:
        neighbors = self.get_adj_list(node)
        for neighbor in neighbors:
            if neighbor in obstacles:
                return False
        return True

    def generate_obstacle_cluster(self, dim_cluster: int, obstacles: Set[int], cluster: List[int]) -> List[int]:
        """
        Genera un nuovo cluster di ostacoli a partire dal nodo specificato.
        """
        while len(cluster) < dim_cluster:
            available = []
            for node in cluster[::-1]:
                neighbors = self.get_adj_list(node)
                available = [node for node in neighbors if
                             node not in cluster and
                             self.are_neighbors_obstacle_free(node, obstacles)]
                if available:
                    break
            if not available:
                return cluster
            next_node = random.sample(available, 1)[0]
            cluster.append(next_node)
        if len(cluster) == dim_cluster:
            return cluster
        return cluster
    
    def set_as_obstacle(self, node: int) -> None:
        neighbors = list(self.adj_list[node].keys())
        for neighbor in neighbors:
            self.delete_edge(node, neighbor)

    def add_edge(self, node1: int, node2: int, weight: float = 1.0) -> None:
        self.adj_list[node1][node2] = weight

    def delete_edge(self, node1: int, node2: int) -> None:
        self.adj_list[node1].pop(node2)
        if node1 != node2:
            self.adj_list[node2].pop(node1)

    def get_adj_list(self, node: int) -> Dict[int, float]:
        return self.adj_list[node]

    def __str__(self) -> str:
        dict_string = ""
        for idx in self.nodes:
            dict_string += "node " + str(idx) + ": " + str(self.adj_list[idx]) + "\n"
        return dict_string

    def get_dim(self) -> Tuple[int, int]:
        return (self.rows, self.cols)

    def get_size(self) -> int:
        return self.size

    def get_obstacles(self) -> List[int]:
        obstacles = []
        for node in self.nodes:
            if self.get_adj_list(node) == {}:
                obstacles.append(node)
        return obstacles

    def get_edge_weight(self, node1: int, node2: int) -> float:
        return self.adj_list[node1][node2]

    def get_free_nodes(self) -> List[int]:
        return [node for node in self.nodes if self.get_adj_list(node) != {}]
    
    def obstacles_to_string(self) -> str:
        obstacles = self.get_obstacles()
        string = ""
        for node in obstacles:
            string += str(node) + " "
        return string
    
if __name__ == "__main__":
    grid = GridGraph(10, 10, 0.8, 0.5)
    print(grid)