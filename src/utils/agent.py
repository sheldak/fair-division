from utils.bundle import Bundle
from utils.item import Item


class Agent:
    def __init__(self, index):
        self.index = index
        self.valuations = {}

    def __hash__(self):
        return hash(self.index)

    def __eq__(self, other):
        return self.index == other.index

    def __repr__(self):
        return f"Agent({self.index})"
    
    def __str__(self):
        return repr(self)
    
    def get_index(self):
        return self.index

    def assign_valuation(self, item, valuation):
        self.valuations[item] = valuation

    def has_valuation(self, item_or_bundle):
        return item_or_bundle in self.valuations

    def get_valuation(self, item_or_bundle):
        if isinstance(item_or_bundle, Item) or isinstance(item_or_bundle, Bundle):
            if item_or_bundle in self.valuations:
                return self.valuations[item_or_bundle]
            else:
                raise Exception(f"Agent {self} has no valuation for {item_or_bundle}")
        else:
            raise Exception(f"Agent can only have valuation for Item or Bundle. Got {item_or_bundle}")
