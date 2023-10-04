import random

"""
Non è strano che un grafo sia caratterizzato da righe, colone, dimensione, etc?
Non è più naturale pensare ada griglia?
Proposte: GridGraph
"""
class gridGraph:
  def __init__(self, row, col, traversability, cluster_agl):
    self.row = row
    self.col = col
    self.size  = row*col
    self.nodes = range(1,self.size+1)

    self.adj_list = buildGridGraph(self, traversability, cluster_agl)

  def buildGridGraph(self):
    graph = {node: dict() for node in self.nodes}
    self.makeGridGraph()
    self.generateObstacle(traversability, cluster_agl)
    return graph

  def getSize(self):
    return (self.row, self.col)
    
  def checkNeighbors(self, node, obstacle):
    neighbors = self.getAdjList(node)
    for neighbor in neighbors:
      if neighbor in obstacle:
        return False
    return True


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
    for key in self.adj_list.keys():
      s
      #print("node",key,": ", self.adj_list[key])

  def makeGridGraph(self):
    for node in self.nodes:
      #aggiungi diagonali
      self.add_diagonal_edge(node)
      #aggiungi cardinali
      self.add_cardinal_edge(node)

  def checkCardinalNeighbor(self, node):
    resto_c = node % self.col
    if resto_c != 1: #check per quello a dx
      self.addEdge(node,node-1,1)
    if node-self.col > 0: #check per quello sopra
      self.addEdge(node, node-self.col,1)
    if resto_c != 0: #check per quello a sx
      self.addEdge(node,node+1,1)
    if node+self.col <= self.size: #check per quello sotto
      self.addEdge(node,node+self.col,1)

  def add_diagonal_edge(self,node):
    resto_r = node % self.row
    resto_c = node % self.col
    w=2
    if resto_c != 1 and node-self.col > 0:
      self.addEdge(node, node-self.col-1,w)
    if resto_c != 0 and node-self.col > 0:
      self.addEdge(node, node-self.col+1,w)
    if resto_c != 1 and node+self.col <= self.size:
      self.addEdge(node, node+self.col-1,w)
    if resto_c != 0 and node+self.col <= self.size:
      self.addEdge(node, node+self.col+1,w)

  def setAsObstacle(graph, node):
    neighbors = list(graph.adj_list[node].keys())
    for idx in neighbors:
      graph.deleteEdge(node,idx)

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
    temp = list(k for k in range(1,self.size +1) if k not in obstacle)
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
    total_obstacle = round(self.size*(1-traversability))
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
 
