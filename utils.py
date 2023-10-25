import heapq
from state import State


class PriorityQueue:
    def __init__(self,items=(),f = lambda x:x):
        self.key = f
        self.items = [] # lista di coppie (score,item)
        for item in items:
            self.add(item)

    def add(self,item):
        """Aggiunge un item alla coda."""
        pair = (self.key(item),item)
        heapq.heappush(self.items,pair)
    
    # def append(self,item):
    #     Aggiunge un item alla coda.
    #     pair = (self.key(item),item)
    #     heapq.heappush(self.items,pair)
    

    def pop(self):
        """pop() ritorna l'item con il valore minimo di f."""
        return heapq.heappop(self.heap)[1]
    
    def top(self):
        """top() ritorna l'item con il valore minimo di f."""
        return self.items[0][1]
    
    def __len__(self):
        return len(self.items)
    
    def __contains__(self, key):
        """Return True se la key è nella PriorityQueue."""
        """__contains è un metodo speciale che viene chiamato quando si usa l'operatore in."""
        return any([item == key for _, item in self.heap])

    def __getitem__(self, other):
        """Ritorna il primo valore associato con la key nella PriorityQueue.
        solleva un KeyError se la key non è presente."""
        for value, item in self.heap:
            if item == other:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        """Cancella la prima occorrenza della key."""
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)
    
# ________________________________________________________________

def expand(grid,state,time):
    """Ritorna una lista di nodi raggiungibili da node."""
    for node,weight in grid.get_adj_list(state.get_node).items():
        cost = state.path_cost + weight
        yield State(node,time,parent=node,path_cost=cost)

# ________________________________________________________________
