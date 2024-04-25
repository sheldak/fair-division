from __future__ import annotations
from typing import Iterator

from fairdivision.utils.item import Item


class Items:
    """
    A class representating a collection of items.

    Contains items in two structures:
      - a dictionary that has item's index as a key, and the corresponding item as value
      - a list of items sorted in an ascending order of their indices
    """

    def __init__(self, items_list: list[Item] = []):
        self.items: dict[int, Item] = {}
        self.sorted_items: list[Item] = []
        self.__initialize_items(items_list)

    def __eq__(self, other):
        return self.get_items() == other.get_items()

    def __iter__(self) -> Iterator[Item]:
        return self.get_items().__iter__()
    
    def __contains__(self, item):
        return item.get_index() in self.items
    
    def __repr__(self):
        return f"Items({self.get_items()})"
    
    def __str__(self):
        return repr(self)
    
    def copy(self) -> Items:
        return Items(self.get_items().copy())

    def __initialize_items(self, items_list: list[Item]) -> None:
        for item in items_list:
            self.items[item.get_index()] = item

        self.sorted_items = sorted(items_list, key=lambda item: item.get_index())

    def add_item(self, item: Item) -> None:
        self.items[item.get_index()] = item
        self.sorted_items = sorted(self.sorted_items + [item], key=lambda item: item.get_index())

    def get_item(self, index: int) -> Item:
        if index in self.items:
            return self.items[index]
        else:
            raise Exception(f"{self.items} does not contain item with index {index}")

    def remove_item(self, index_or_item: int | Item) -> None:
        if isinstance(index_or_item, int):
            self.items.pop(index_or_item)
            self.sorted_items = list(filter(lambda item: item.get_index() != index_or_item, self.sorted_items))
        elif isinstance(index_or_item, Item):
            self.items.pop(index_or_item.get_index())
            self.sorted_items.remove(index_or_item)
        else:
            raise Exception(f"To delete an item from items, index or Item object was expected, got {index_or_item}")

    def get_items(self) -> list[Item]:
        return self.sorted_items
    
    def get_indices(self) -> list[int]:
        return list(map(lambda item: item.get_index(), self.sorted_items))
    
    def size(self) -> int:
        return len(self.items)
