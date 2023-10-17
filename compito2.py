import math
def euristic(grid,init,goal):
    row,col=grid.get_dim()
    x_init = (init-1)//col
    y_init = (init-1)% col
    x_goal = (goal-1)//col
    y_goal = (goal-1)% col

    dx = abs(x_init-x_goal)
    dy = abs(y_init-y_goal)
    return dx+dy + (math.sqrt - 2)*min(dx,dy)

def ReachGoal(grid,paths,init,goal,max_time):
    P = {}
    t = 0
    closed = set()
    g_cost = {(init,0): 0}
    f_score = {(init,0): euristic(grid,init,goal)}
    current = (f_score[(init,0)],init)
    open = [current]
    heapq.heapify(open)
    while open:
        current = open.pop(0)
        closed.add(current)
        
        if current[1] == goal:
            return ReconstructPath(init,goal,P,t)
        
        if t < max_time:
            for neighbors in grid.get_adj_list(current[1]):
                for n in neighbors:
                    if (n,t+1) not in closed:
                        traversable = True
                        for path in paths:
                        # check if the path is traversable
                                traversable = False
                        if traversable:
                            if g_cost(current) + grid.get_adj_list[current(1)][n] < g_cost[(n,t+1)]:
                                g_cost[(n,t+1)] = g_cost[current] + grid.get_adj_list[current(1)][n]
                                P[(n,t+1)] = current
                                f_score[(n,t+1)] = g_cost[(n,t+1)] + euristic(grid,n,goal)
                                open.append((f_score[(n,t+1)],n))
                                heapq.heapify(open)

                                
                     
                    
