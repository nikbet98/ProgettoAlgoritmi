class State:
    def __init__(self, node, time, parent=None, path_cost=0):
        self.time = time
        self.node = node
        self.parent=parent
        self.path_cost=path_cost

    def __ne__(self,other):
        return other.node != self.node and other.time != self.time

    def is_goal(self, goal):
        return self.node == goal
    
    def get_node(self):
        return self.node
    
    def get_path_cost(self):
        return self.path_cost
    
    def det_parent(self):
        return self.parent
    def add_parent(self, parent):
        self.parent = parent
    
    def add_path_cost(self, path_cost):
        self.path_cost = path_cost

    def get_parent(self):
        return self.parent
    
    def __eq__(self, other):
        """viene chiamato quando si confrontano due stai con l'operatore =="""
        """isinstance verifica che l'oggetto sia una istanza di State"""
        return isinstance(other,State) and self.node == other.node and self.time == other.time

    def __lt__(self, other):
        return self.path_cost < other.get_path_cost()

        