import random

# costanti
WEIGHT_CARDINAL_DIRECTION = 1
WEIGHT_DIAGONAL_DIRECTION = 2

class GridGraph:
  def __init__(self, rows, cols, traversability_ratio, obstacle_agglomeration_ratio):
    import random

    """
    Inizializza una griglia di nodi con le dimensioni specificate.
    """
    self.rows = rows
    self.cols = cols
    self.size = rows * cols
    self.traversability_ratio = traversability_ratio

    self.obstacle_agglomeration_ratio = obstacle_agglomeration_ratio
    self.nodes = range(0,self.size)
    self.adj_list = [{} for node in self.nodes]
    self.generate_neighbors()
    self.generate_obstacles()

  def generate_neighbors(self):
    """
    Genera gli elenchi di adiacenza per ogni nodo nella griglia.
    """
    for current_node in self.nodes:
      self.connect_adjacent_nodes(current_node)

  def connect_adjacent_nodes(self, node):
    """
    Connette il nodo specificato ai suoi nodi adiacenti nella griglia.
    """
    row = (node) // self.cols
    col = (node) % self.cols

      # Definisco le direzioni dei nodi
    directions = [
      (-1, 0), # nord
      (1, 0),  # sud
      (0, -1), # ovest 
      (0, 1),  # est
      (-1, -1),# nord-ovest
      (-1, 1), # nord-est
      (1, -1), # sud-ovest
      (1, 1),  # sud-est
    ]

    # connetto i nodi adiacenti in base alle direzioni
    for direction_row, direction_col in directions:
      new_row, new_col = row + direction_row, col + direction_col
      if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
        neighbor = new_row * self.cols + new_col
        weight = WEIGHT_CARDINAL_DIRECTION
        if direction_row != 0 and direction_col != 0: # ci stiamo muovendo in diagonale
          weight = WEIGHT_DIAGONAL_DIRECTION
        self.add_edge(node, neighbor, weight)

  def generate_obstacles(self):
    """
    Genera gli ostacoli nella griglia in base alla percentuale di attraversabilità e di agglomerazione degli ostacoli.
    """
    num_obstacles = self.calculate_num_obstacles()
    if num_obstacles != 0: # se il numero di ostacoli è nullo non tentare di generare gli ostacoli
      obstacles = self.build_obstacles(num_obstacles)
      for node in obstacles:
        self.set_as_obstacle(node)

  def calculate_num_obstacles(self):
    return round(self.size * (1 - self.traversability_ratio))

  def build_obstacles(self, num_obstacles):
    """
    Genera gli ostacoli nella griglia in base alla percentuale di agglomerazione degli ostacoli.
    """
    obstacles = set()
    cluster_size = self.calculate_cluster_size(num_obstacles)
    num_clusters = self.calculate_num_clusters(num_obstacles, cluster_size)
    for i in range(num_clusters):
      start = self.find_start_node(obstacles)
      if start is not None:
        cluster = self.generate_obstacle_cluster(cluster_size, obstacles, start, cluster=[])
        obstacles.update(cluster)
    return obstacles

  def calculate_cluster_size(self, num_obstacles):
    if self.obstacle_agglomeration_ratio == 0:
      return 1
    return round(num_obstacles * self.obstacle_agglomeration_ratio)

  def calculate_num_clusters(self, num_obstacles, cluster_size):
    if cluster_size == 1:
      return num_obstacles
    return round(num_obstacles / cluster_size)

  def find_start_node(self, obstacles):
    """
    Trova un nodo di partenza per generare un nuovo cluster di ostacoli.
    """
    available = [node for node in self.nodes if node not in obstacles and self.are_neighbors_obstacle_free(node, obstacles)]
    if not available:
      return None
    start = random.choice(available)
    return start

  def are_neighbors_obstacle_free(self, node, obstacles):
    neighbors = self.get_adj_list(node)
    for neighbor in neighbors:
      if neighbor in obstacles:
        return False
    return True

  def generate_obstacle_cluster(self, dim_cluster, obstacles, start, cluster):
    """
    Genera un nuovo cluster di ostacoli a partire dal nodo specificato.
    """
    if len(cluster) == dim_cluster:
      return cluster
    neighbors = self.get_adj_list(start)
    available = [node for node in neighbors if node not in cluster and self.are_neighbors_obstacle_free(node, obstacles)]
    if not available:
      return cluster
    next_node = random.sample(available, 1)[0]
    cluster.append(next_node)
    return self.generate_obstacle_cluster(dim_cluster, obstacles, next_node, cluster)

  def set_as_obstacle(self, node):
    neighbors = list(self.adj_list[node].keys())
    for neighbor in neighbors:
      self.delete_edge(node, neighbor)

  def add_edge(self, node1, node2, weight=1):
    self.adj_list[node1][node2] = weight

  def delete_edge(self, node1, node2):
    self.adj_list[node1].pop(node2)
    self.adj_list[node2].pop(node1)

  def get_adj_list(self, node):
    return self.adj_list[node]

  def __str__(self):
    dict_string = ""
    for idx in self.nodes:
      dict_string += "node " + str(idx) + ": " + str(self.adj_list[idx]) + "\n"
    return dict_string

  def get_dim(self):
    return (self.rows, self.cols)
  
  def get_size(self):
    return self.size
  
  def get_obstacles(self):
    return self.nodes.filter(lambda node: self.get_adj_list(node) == {})
 
  def get_edge_weight(self, node1, node2):
    return self.adj_list[node1][node2]