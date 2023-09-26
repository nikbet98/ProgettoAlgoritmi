moves = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

class Cell:

    
    def __init__(self, i, j,grid=None):

        self.grid = grid
        self.i = i
        self.j = j
        self.neighbors = []
        self.neighboring_obstacles = []
        # self.previous = None
        self.obstacle = False
    
    
    def addNeighbors(self, grid):
        self.neighbors = []
        # Add neighbors
        for i in range(len(moves)):
            cell = grid.getCell(self.i + moves[i][0], self.j + moves[i][1])
            if cell != None:
                self.neighbors.append(cell)
    
     
    """
    if i < rows-1:
      self.neighbors.append(grid[i+1][j])
        if i > 0:
            self.neighbors.append(grid[i-1][j])
        if j < cols-1:
            self.neighbors.append(grid[i][j+1])
        if j > 0:
            self.neighbors.append(grid[i][j-1])
        if i > 0 and j > 0:
            self.neighbors.append(grid[i-1][j-1])
        if i < rows-1 and j > 0:
            self.neighbors.append(grid[i+1][j-1])
        if i > 0 and j < cols-1:
            self.neighbors.append(grid[i-1][j+1])
        if i < rows-1 and j < cols-1:
            self.neighbors.append(grid[i+1][j+1])
    """

    def __str__(self):
        return "(" + str(self.i) + "," + str(self.j) + ")"