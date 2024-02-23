from utils.agent import Agent
from utils.agents import Agents
from utils.bundle import Bundle
from utils.item import Item
from utils.items import Items


class Allocation:
    def __init__(self, agents: Agents):
        self.allocation: dict[Agent, Bundle] = {}
        self.initialize_allocation(agents)

    def __iter__(self):
        return self.get_allocation().__iter__()

    def initialize_allocation(self, agents: Agents) -> None:
        for agent in agents:
            bundle = Bundle(Items())
            bundle.assign_agent(agent)
            self.allocation[agent] = bundle

    def allocate(self, agent: Agent, item: Item) -> None:
        self.allocation[agent].add_item(item)

    def for_agent(self, agent: Agent) -> Bundle:
        if agent in self.allocation:
            return self.allocation[agent]
        else:
            raise Exception(f"Agent {agent} has no bundle")
        
    def get_allocation(self) -> list[tuple[Agent, Bundle]]:
        return list(self.allocation.items())
