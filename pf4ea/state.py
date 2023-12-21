class State:
    """
    Rappresenta uno stato nel problema.
    
    Attributes:
        node: Il nodo corrispondente allo stato.
        time: Il tempo associato allo stato.
        parent: Lo stato genitore.
        path_cost: Il costo del percorso per raggiungere lo stato.
    """
    def __init__(self, node: int, time: int, parent=None, path_cost: float = 0):
        self.time = time
        self.node = node
        self.parent = parent
        self.path_cost = path_cost

    def __ne__(self, other: 'State') -> bool:
        return other.node != self.node and other.time != self.time

    def is_parent_None(self) -> bool:
        return self.parent is None

    def _add_parent(self, parent: 'State'):
        self.parent = parent

    def __hash__(self) -> int:
        return hash((self.node, self.time))

    def __eq__(self, other: 'State') -> bool:
        """
        Viene chiamato quando si confrontano due stati con l'operatore == 
        isinstance verifica che l'oggetto sia un'istanza di State
        """
        return isinstance(other, State) and self.node == other.node and self.time == other.time

    def __lt__(self, other: 'State') -> bool:
        return self.path_cost < other.path_cost
    
    def __str__(self) -> str:
        return f"{self.node}, {self.time}"
    
    def _is_a_wait(self) -> bool:
        current = self.node
        if self.parent is None:
            return False
        p = self.parent.node
        return current == p

        