class Item:
    def __init__(self, index):
        self.index = index

    def __hash__(self):
        return hash(self.index)

    def __eq__(self, other):
        return self.index == other.index
    
    def __repr__(self):
        return f"Item({self.index})"
    
    def __str__(self):
        return repr(self)
    
    def get_index(self):
        return self.index