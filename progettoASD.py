import random

# costanti
WEIGHT_CARDINAL_MOVES = 1
WEIGHT_DIAGONAL_MOVES= 2


# commit di prova
# faccio un branch su dev
class Graph:
  def __init__(self, r, c, traversability, cluster_agl):
    self.row = r
    self.col = c
    self.n = r*c
    self.nodes = range(1,self.n+1)

    self.adj_list = {node: dict() for node in self.nodes}
    self.create_grid()
    self.generateObstacle(traversability, cluster_agl)

  def getDim(self):
    return (self.row, self.col)
    
  def checkNeighbors(self, node, obstacle):
    neighbors = self.getAdjList(node)
    for neighbor in neighbors:
      if neighbor in obstacle:
        return False
    return True

  def add_edge(self, node1, node2, weight=1):
      self.adj_list[node1].update({node2: weight})

  def delete_edge(self, node1, node2):
    #da una parte
    self.adj_list[node1].pop(node2)

    #dall'altra parte
    self.adj_list[node2].pop(node1)

  def getAdjList(self, node):
    return self.adj_list[node]

  def print_adj_list(self):
    for key in self.adj_list.keys():
      print("node",key,": ", self.adj_list[key])

  def create_grid(self):
    for node in self.nodes:
      #aggiungi diagonali
      self.add_diagonal_edge(node)
      #aggiungi cardinali
      self.add_cardinal_edge(node)

  def checkCardinalNeighbor(self, node):
    resto_c = node % self.col
    if resto_c != 1 or node-self.col > 0 or resto_c != 0 or node+self.col <= self.n:
      return node
    return None  

  def checkDiagonalNeighbor(self, node):
    resto_c = node % self.col
    if (resto_c != 1 or resto_c != 0) and (node-self.col > 0 or node+self.col <= self.n):
      return node
    return None

  def add_cardinal_edge(self, node):    
    cardinalMoves = [-1,-self.col,+1,+self.col]

    for i in range(len(cardinalMoves)):
      neighbor = self.checkCardinalNeighbor(node+cardinalMoves[i])
      if neighbor != None:
        self.add_edge(node,neighbor,WEIGHT_CARDINAL_MOVES)

  def add_diagonal_edge(self,node):
    diagonalMoves = [-self.col-1,-self.col+1,+self.col-1,+self.col+1]
    
    for i in range(len(diagonalMoves)):
      neighbor = self.checkDiagonalNeighbor(node+diagonalMoves[i])
      if neighbor != None:
        self.add_edge(node,neighbor,WEIGHT_DIAGONAL_MOVES)

  def setAsObstacle(graph, node):
    neighbors = list(graph.adj_list[node].keys())
    for idx in neighbors:
      graph.delete_edge(node,idx)

  def findAvailable(self, node, obstacle):
    available=list()
    neighbors = self.adj_list[node]
    for n in neighbors:
      if n not in obstacle:
        available.append(n)
    return available
  
  def generateCluster(self, dim_cluster, obstacle, start, cluster):
    if len(cluster) == dim_cluster:
      return cluster
    neighbors = self.adj_list[start]
    available = list()
    for n in neighbors:
      if n not in cluster and self.checkNeighbors(n, obstacle):
        available.append(n)
    if len(available) == 0:
      return cluster
    next = random.choice(available)
    cluster.append(next)
    return self.generateCluster(dim_cluster, obstacle, next, cluster)

  def findStart(self, obstacle):
    temp = list(k for k in range(1,self.n +1) if k not in obstacle)
    available = list()
    for t in temp:
      if self.checkNeighbors(t,obstacle):
        available.append(t)
    if len(available) == 0:
      return False
    start = random.choice(available)
    return start

  def generateObstacle(self, traversability, cluster_agl):
    obstacle = list()
    total_obstacle = round(self.n*(1-traversability))
    if cluster_agl == 0:
      dim_cluster = 1
      n_cluster = total_obstacle
    else:
       dim_cluster = round(total_obstacle*cluster_agl)
       n_cluster = round(total_obstacle/dim_cluster)
    
    #generate cluster
    for i in range(n_cluster):
      start = self.findStart(obstacle)
      if not start:
        break
      else:
        cluster = list()
        cluster.append(start)
        cluster = self.generateCluster(dim_cluster, obstacle, start, cluster)
        obstacle.extend(cluster)
    for o in obstacle:
      self.setAsObstacle(o)
 
