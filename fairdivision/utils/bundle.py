from __future__ import annotations
from typing import Iterator, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from fairdivision.utils.agent import Agent

from fairdivision.utils.item import Item
from fairdivision.utils.items import Items


class Bundle:
    """
    A class representating a bundle of Items.

    It is an object that should be allocated to Agents. Contains Items and the Agent to which
    it is allocated.
    """
     
    def __init__(self, items: Items):
        self.items: Items = items
        self.agent: Optional[Agent] = None

    def __hash__(self):
        curr_hash = 0
        for item in self.items:
            curr_hash += item.__hash__()

        return hash(curr_hash)

    def __eq__(self, other):
        return self.get_items() == other.get_items() and self.get_agent() == other.get_agent()

    def __repr__(self):
        items = self.items.get_indices()
        return f"Bundle({items})"
    
    def __str__(self):
        return repr(self)
    
    def __iter__(self) -> Iterator[Item]:
        return self.items.__iter__()
    
    def __contains__(self, item):
        return item in self.items
    
    def copy(self) -> Bundle:
        return Bundle(self.items.copy())

    def add_item(self, item: Item) -> None:
        self.items.add_item(item)
    
    def delete_item(self, index_or_item: int | Item) -> None:
        self.items.delete_item(index_or_item)

    def get_items(self) -> Items:
        return self.items
    
    def assign_agent(self, agent: Agent) -> None:
        self.agent = agent

    def get_agent(self) -> Optional[Agent]:
        return self.agent

    def size(self) -> int:
        return self.items.size()
