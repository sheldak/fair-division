from __future__ import annotations

from utils.item import Item


class Items:
    def __init__(self, items_list: list[Item] = []):
        self.items: dict[int, Item] = {}
        self.initialize_items(items_list)

    def __iter__(self):
        return list(self.get_items()).__iter__()
    
    def __contains__(self, item):
        return item in self.get_items()
    
    def copy(self) -> Items:
        return Items(self.get_items().copy())

    def initialize_items(self, items_list: list[Item]) -> None:
        for item in items_list:
            self.add_item(item)

    def add_item(self, item: Item) -> None:
        self.items[item.get_index()] = item

    def get_item(self, index: int) -> Item:
        if index in self.items:
            return self.items[index]
        else:
            raise Exception(f"{self.items} does not contain item with index {index}")

    def delete_item(self, index_or_item: int | Item) -> None:
        if isinstance(index_or_item, int):
            self.items.pop(index_or_item)
        elif isinstance(index_or_item, Item):
            self.items.pop(index_or_item.get_index())
        else:
            raise Exception(f"To delete an item from items, index or Item object was expected, got {index_or_item}")

    def get_items(self) -> list[Item]:
        return list(self.items.values())
    
    def get_indices(self) -> list[int]:
        return list(self.items.keys())
    
    def size(self) -> int:
        return len(self.items)