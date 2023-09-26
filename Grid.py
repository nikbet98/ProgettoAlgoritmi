from cell import Cell
import random

class Grid:
    def __init__(self, rows, cols,obstacle_percentage, clustering_factor):
        self.rows = rows
        self.cols = cols
        self.obstacle_percentage = obstacle_percentage
        self.clustering_factor = clustering_factor
        self.grid = [[Cell(i, j) for j in range(cols)] for i in range(rows)]
        self.populateNeighbors(self)
        self.populateObstacles(self)

    def getCell(self, i, j):
        if i < 0 or j < 0 or i >= self.rows or j >= self.cols:
            return None
        return self.grid[i][j]
    
    def populateNeighbors(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j].addNeighbors(self,self.grid)

    def populateObstacles(self):
        num_obstacles = int(self.obstacle_percentage * self.rows * self.cols)
        print(str(num_obstacles))
        # cluster_size = int(self.clustering_factor * self.rows * self.cols / num_obstacles)
        cluster_size = 2
        
        # Add obstacles randomly
        for idx in range(num_obstacles):
            # Add obstacles in clusters

            current = self.grid[0][0]
            cluster = []

            while True:
                i = random.randint(0,self.rows) 
                j = random.randint(0,self.cols)
                current = self.grid[i][j]
                if current.obstacle == False and current.neighboring_obstacles:
                    break

        while cluster_size > 0:
            unvisitedNeighbors = current.neighbors

            if (not unvisitedNeighbors.isEmpty()):

                while True:
                    selected = unvisitedNeighbors[random.randint(0,len(unvisitedNeighbors))]
                    if not selected.neighboring_obstacles.filter(lambda x: x not in cluster).isEmpty():
                        break

                current.obstacle = True
                cluster.append(current)
                
                for i in range(len(unvisitedNeighbors)):
                    unvisitedNeighbors[i].neighbors.remove(current)
                    unvisitedNeighbors[i].neighboring_obstacles.append(current)

                current = selected
                cluster_size -= 1
            else:
            
                break
         

    def __str__(self):
        s = ""
        for i in range(self.rows):
            for j in range(self.cols):
                s += str(self.grid[i][j].obstacle) + " "
            s += "\n"
        return s    