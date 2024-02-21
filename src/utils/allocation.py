from utils.bundle import Bundle
from utils.items import Items


class Allocation:
    def __init__(self, agents):
        self.allocation = {}
        self.initialize_allocation(agents)

    def __iter__(self):
        return self.get_allocation().__iter__()

    def initialize_allocation(self, agents):
        for agent in agents:
            bundle = Bundle(Items())
            bundle.assign_agent(agent)
            self.allocation[agent] = bundle

    def allocate(self, agent, item):
        self.allocation[agent].add_item(item)

    def for_agent(self, agent):
        if agent in self.allocation:
            return self.allocation[agent]
        else:
            raise Exception(f"Agent {agent} has no bundle")
        
    def get_allocation(self):
        return list(self.allocation.items())
