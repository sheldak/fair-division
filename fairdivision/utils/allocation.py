from typing import Iterator

from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.bundle import Bundle
from fairdivision.utils.item import Item
from fairdivision.utils.items import Items


class Allocation:
    """
    A class representating an allocation of Items in Bundles to Agents.

    Contains the allocation and manages all changes to it.
    """

    def __init__(self, agents: Agents):
        self.allocation: dict[Agent, Bundle] = {}
        self.__initialize_allocation(agents)

    def __eq__(self, other):
        return self.get_allocation() == other.get_allocation()

    def __iter__(self) -> Iterator[tuple[Agent, Bundle]]:
        return self.get_allocation().__iter__()
    
    def __repr__(self):
        return f"Allocation({self.allocation})"
    
    def __str__(self):
        return repr(self)

    def __initialize_allocation(self, agents: Agents) -> None:
        for agent in agents:
            bundle = Bundle(Items())
            bundle.assign_agent(agent)
            self.allocation[agent] = bundle

    def allocate(self, agent: Agent, item: Item) -> None:
        self.allocation[agent].add_item(item)

    def allocate_bundle(self, agent: Agent, bundle: Bundle) -> None:
        self.allocation[agent] = bundle

        previous_owner = bundle.get_agent()
        if previous_owner in self.allocation and self.allocation[previous_owner] == bundle:
            self.allocation[previous_owner] = Bundle(Items())

        bundle.assign_agent(agent)

    def for_agent(self, agent: Agent) -> Bundle:
        if agent in self.allocation:
            return self.allocation[agent]
        else:
            raise Exception(f"Agent {agent} has no bundle")
        
    def get_allocation(self) -> list[tuple[Agent, Bundle]]:
        return list(self.allocation.items())
