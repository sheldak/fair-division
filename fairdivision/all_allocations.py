from typing import Iterator

from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.items import Items


class AllAllocations:
    """
    A class that can be iterated over to return all possible allocations of `Items` to `Agents`.
    """

    def __init__(self, agents: Agents, items: Items):
        self.agents: Agents = agents
        self.items: Items = items

        self.agents_indices: list[int] = agents.get_indices()

        self.allocation_index: int = 0
        self.allocations_number: int = self.agents.size() ** self.items.size()

    def __iter__(self):
        return self

    def __next__(self):
        if self.allocation_index < self.allocations_number:
            allocation = self.__current_allocation()            

            self.allocation_index += 1

            return allocation
        else:
            raise StopIteration

    def __current_allocation(self):
        """
        Creates `Allocation` out of current `self.allocation_index`.

        There are `n^m` possible allocations of `m` items to `n` agents - each of `m` items has to be assigned to
        exactly one of `n` agents. Each of these allocations is represented by a number - `self.allocation_index`.

        `self.allocation_index` is an integer from the interval `[0, n^m - 1]`. If we represent it in base `n`, then
        each `i`-th digit tell us which of the `n` agents is endowed with item being in the `i`-th position of the
        items list. 
        """

        allocation = Allocation(self.agents)

        allocation_index = self.allocation_index

        for item in self.items:
            endowed_agent_index = self.agents_indices[allocation_index % self.agents.size()]
            endowed_agent = self.agents.get_agent(endowed_agent_index)

            allocation.allocate(endowed_agent, item)

            allocation_index //= self.agents.size()

        return allocation


def all_allocations(agents: Agents, items: Items) -> Iterator[Allocation]:
    """
    Returns an iterator giving all possible allocations of `items` to `agents`.
    """

    return iter(AllAllocations(agents, items))