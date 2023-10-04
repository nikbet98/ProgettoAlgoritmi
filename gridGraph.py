import random

# costanti
WEIGHT_CARDINAL_DIRECTION = 1
WEIGHT_DIAGONAL_DIRECTION = 2
"""
Non è strano che un grafo sia caratterizzato da righe, colone, dimensione, etc?
Non è più naturale pensare ada griglia?
Proposte: GridGraph
"""
class GridGraph:
  def __init__(self, rows, cols, traversability, obstacle_density):
    self.rows = rows
    self.cols = cols
    self.size  = rows * cols
    self.traversability = traversability
    self.obstacle_density = obstacle_density
    self.nodes = range(1,self.size + 1)
    self.adj_list = {node: {} for node in self.nodes}
    self.generateNeighbors()
    self.generateObstacles()

  def generateNeighbors(self):
    for current_node in self.nodes:
      self.connectAdjacentNodes(current_node)

  def connectAdjacentNodes(self, node):
    row = (node - 1) // self.cols
    col = (node - 1) % self.cols

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
    for direction_row,direction_col in directions:
      new_row, new_col = row + direction_row, col + direction_col
      if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
        neighbor = new_row * self.cols + new_col + 1
        weight = WEIGHT_CARDINAL_DIRECTION
        if direction_row != 0 and direction_col != 0: # ci stiamo muovendo in diagonale
          weight = WEIGHT_DIAGONAL_DIRECTION
        self.addEdge(node, neighbor, weight)
  """
      # nodi cardinali
      if col != 0:
          self.add_edge(node, node - 1, WEIGHT_CARDINAL_DIRECTION)
      if col != self.cols - 1:
          self.add_edge(node, node + 1, WEIGHT_CARDINAL_DIRECTION)
      if row != 0:
          self.add_edge(node, node - self.cols, WEIGHT_CARDINAL_DIRECTION)
      if row != self.rows - 1:
          self.add_edge(node, node + self.cols, WEIGHT_CARDINAL_DIRECTION)
      
      # nodi diagonali
      if col != 0 and row != 0:
          self.add_edge(node, node - self.cols - 1, 2, WEIGHT_DIAGONAL_DIRECTION)
      if col != self.cols - 1 and row != 0:
          self.add_edge(node, node - self.cols + 1, 2, WEIGHT_DIAGONAL_DIRECTION)
      if col != 0 and row != self.rows - 1:
          self.add_edge(node, node + self.cols - 1, 2, WEIGHT_DIAGONAL_DIRECTION)
      if col != self.cols - 1 and row != self.rows - 1:
          self.add_edge(node, node + self.cols + 1, 2, WEIGHT_DIAGONAL_DIRECTION)
  """

  def generateObstacles(self):
      # Calcolo il numero di ostacoli in base alle dimensioni della griglia e alla percentuale di attraversabilità
      num_obstacles = self.calculateNumObstacles()

      # Genera gli ostacoli
      obstacles = self.buildObstacles(num_obstacles)

      # Imposta gli ostacoli nella griglia
      for node in obstacles:
        self.setAsObstacle(node)
      

  def calculateNumObstacles(self):
    num_obstacles = round(self.size * (1 - self.traversability))
    return num_obstacles
    

  def buildObstacles(self, num_obstacles):
      obstacles = set()

      if self.obstacle_density == 0:
        cluster_size = 1
        num_clusters = num_obstacles
      else:
        cluster_size = round(num_obstacles * self.obstacle_density)
        num_clusters = round(num_obstacles / cluster_size)
      
      for i in range(num_clusters):
        start = self.findStart(obstacles)

        if start is not None:
          cluster = self.generateObstacleCluster(cluster_size, obstacles, start,cluster = [])
          obstacles.update(cluster)
      return obstacles
    

  def findStart(self, obstacles):
    available = [node for node in self.nodes if node not in obstacles and self.areNeighborsObstacleFree(node, obstacles)]

    if not available:
      return None
    start = random.choice(available)
    return start
    
  def areNeighborsObstacleFree(self, node, obstacle):
    neighbors = self.getAdjList(node)
    for neighbor in neighbors:
      if neighbor in obstacle:
        return False
    return True
      
  def generateObstacleCluster(self, dim_cluster, obstacle, start,cluster):
    if len(cluster) == dim_cluster:
      return cluster
      
    neighbors = self.getAdjList(start)
    available = [node for node in neighbors if node not in cluster and self.areNeighborsObstacleFree(node, obstacle)]
      
    if not available: # controllo se available è vuoto restituendo True o False
      return cluster
      
    next_node = random.choice(available) 
    cluster.append(next_node)

    return self.generateObstacleCluster(dim_cluster, obstacle, next, cluster)


  def setAsObstacle(self, node):
    neighbors = list(self.adj_list[node].keys())
    for neighbor in neighbors:
      self.deleteEdge(node,neighbor)


  def addEdge(self, node1, node2, weight=1):
    self.adj_list[node1].update({node2: weight})


  def deleteEdge(self, node1, node2):
    #da una parte
    self.adj_list[node1].pop(node2)

    #dall'altra parte
    self.adj_list[node2].pop(node1)


  def getAdjList(self, node):
    return self.adj_list[node]


  def __str__(self):
    dict_string = ""
    for key, value in self.adj_list.items():
      dict_string += "node " + str(key) + ": " + str(self.adj_list[key]) + "\n"
      
    return dict_string
      # print("node",key,": ", self.adj_list[key])


  def findAvailable(self, node, obstacle):
    available=list()
    neighbors = self.adj_list[node]
    for n in neighbors:
      if n not in obstacle:
        available.append(n)
    return available
      
  def getDim(self):
    return (self.rows, self.cols)