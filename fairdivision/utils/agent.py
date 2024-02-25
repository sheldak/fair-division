from fairdivision.utils.bundle import Bundle
from fairdivision.utils.item import Item
from fairdivision.utils.items import Items


class Agent:
    def __init__(self, index: int):
        self.index: int = index
        self.valuations: dict[Item | Bundle, int] = {}

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

    def assign_valuation(self, item: Item, valuation: int) -> None:
        self.valuations[item] = valuation

    def has_valuation(self, item_or_bundle: Item | Bundle) -> bool:
        return item_or_bundle in self.valuations

    def get_valuation(self, item_or_bundle: Item | Bundle) -> int:
        if isinstance(item_or_bundle, Item) or isinstance(item_or_bundle, Bundle):
            if item_or_bundle in self.valuations:
                return self.valuations[item_or_bundle]
            else:
                raise Exception(f"Agent {self} has no valuation for {item_or_bundle}")
        else:
            raise Exception(f"Agent can only have valuation for Item or Bundle. Got {item_or_bundle}")

    def get_favorite_item(self, items: Items) -> Item:
        if items.size() > 0:
            favorite_item = items.get_items()[0]
            
            for item in items:
                if self.get_valuation(item) > self.get_valuation(favorite_item):
                    favorite_item = item

            return favorite_item
        else:
            raise Exception("Cannot return a favourite item if there are no items")