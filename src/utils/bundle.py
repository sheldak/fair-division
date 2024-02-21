class Bundle:
    def __init__(self, items):
        self.items = items
        self.agent = None

    def __hash__(self):
        curr_hash = 0
        for item in self.items:
            curr_hash += item.__hash__()

        return hash(curr_hash)

    def __eq__(self, other):
        for item in self:
            if item not in other:
                return False
            
        return self.size() == other.size()

    def __repr__(self):
        items = sorted(list(self.items.get_indices()))
        return f"Bundle({items})"
    
    def __str__(self):
        return repr(self)
    
    def __iter__(self):
        return self.items.__iter__()
    
    def __contains__(self, item):
        return item in self.items
    
    def copy(self):
        return Bundle(self.items.copy())

    def add_item(self, item):
        self.items.add_item(item)
    
    def delete_item(self, index_or_item):
        self.items.delete_item(index_or_item)

    def get_items(self):
        return self.items
    
    def assign_agent(self, agent):
        self.agent = agent

    def size(self):
        return self.items.size()