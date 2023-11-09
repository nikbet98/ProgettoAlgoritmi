import heapq
from state import State


class PriorityQueue:
    def __init__(self, state, f=lambda x: x):
        self.f = f
        self.queue = [(f(state), state)]  # lista di coppie (score,item)

    def add(self, item):
        """Aggiunge un item alla coda."""
        #test
        print("new node in open =",item.get_node(),"f =",self.f(item))
        #test
        pair = (self.f(item), item)
        heapq.heappush(self.queue, pair)

    # def append(self,item):
    #     Aggiunge un item alla coda.
    #     pair = (self.f(item),item)
    #     heapq.heappush(self.queue,pair)

    def pop(self):
        """pop() ritorna l'item con il valore minimo di f."""
        return heapq.heappop(self.queue)[1]

    def top(self):
        """top() ritorna l'item con il valore minimo di f."""
        return self.queue[0][1]

    def __len__(self):
        return len(self.queue)

    def __contains__(self, key):
        """Return True se la key è nella PriorityQueue."""
        """__contains è un metodo speciale che viene chiamato quando si usa l'operatore in."""
        return any([item == key for _, item in self.queue])

    def __getitem__(self, other):
        """Ritorna il primo valore associato con la key nella PriorityQueue.
        solleva un KeyError se la key non è presente."""
        for value, item in self.queue:
            if item == other:
                return value
        raise KeyError(str(other) + " is not in the priority queue")

    def __delitem__(self, key):
        """Cancella la prima occorrenza della key."""
        try:
            del self.queue[[item == key for _, item in self.queue].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.queue)


    def __str__(self):
        string_open_list = ', '.join(f"< ({item[1].node},{item[1].time}),{item[0]}>" for item in self.queue)
        return string_open_list

    def is_empty(self):
        return len(self) == 0
# ________________________________________________________________


def expand(grid, parent_state, time):
    print("_______________________")
    print("time =",time)
    print("nodi espansi dal nodo ,",parent_state.get_node(),":")
    """Ritorna una lista di nodi raggiungibili da node."""
    for child_node, weight in grid.get_adj_list(parent_state.get_node()).items():
        #test
        p = parent_state.get_node()
        pc = parent_state.get_path_cost()
        cost = pc + weight
        print("p = ",p,"child = ",child_node,"path cost = ",cost)
        yield State(child_node, time + 1, parent = parent_state, path_cost=cost)
        # test  
# ________________________________________________________________
