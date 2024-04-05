from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fairdivision.utils.allocation import Allocation

from fairdivision.utils.bundle import Bundle
from fairdivision.utils.item import Item
from fairdivision.utils.items import Items


class Agent:
    """
    A class representating an agent.

    Contains information about agent's valuations of items.
    """

    def __init__(self, index: int, valuations_additive: bool = True):
        self.index: int = index
        self.valuations: dict[Item | Bundle, int] = {}
        self.valuations_additive: bool = valuations_additive

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
        if isinstance(item_or_bundle, Bundle) and self.valuations_additive:
            valuation = 0
            for item in item_or_bundle:
                valuation += self.valuations[item]

            return valuation
        elif isinstance(item_or_bundle, Item) or isinstance(item_or_bundle, Bundle):
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

    def envies(self, other: Agent, allocation: Allocation) -> bool:
        self_valuation = self.get_valuation(allocation.for_agent(self))
        other_valuation = self.get_valuation(allocation.for_agent(other))

        return other_valuation > self_valuation
