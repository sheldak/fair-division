import random

from utils.agent import Agent
from utils.agents import Agents
from utils.bundle import Bundle
from utils.item import Item
from utils.items import Items


class ValuationsGenerator:
    def __init__(self, additive=True, min=0, max=100):
        self.additive = additive
        self.min = min
        self.max = max

    def valuate(self, agent, item_or_bundle):
        if self.additive:
            return self.valuate_additively(agent, item_or_bundle)
        else:
            if agent.has_valuation(item_or_bundle):
                return agent.get_valuation(item_or_bundle)
            else:
                return random.randint(self.min, self.max)
    
    def valuate_additively(self, agent, item_or_bundle):
        if isinstance(item_or_bundle, Item):
            return self.valuate_item(agent, item_or_bundle)
        elif isinstance(item_or_bundle, Bundle):
            valuation = 0

            for item in item_or_bundle.items:
                valuation += self.valuate_item(agent, item)

            return valuation
        else:
            raise Exception(f"Can only valuate item or bundle, got {item_or_bundle}")

    def valuate_item(self, agent, item):
        if agent.has_valuation(item):
            return agent.get_valuation(item)
        else:
            return random.randint(self.min, self.max)


def generate_agents(n):
    agents = []

    for i in range(1, n+1):
        agents.append(Agent(i))

    return Agents(agents)


def generate_items(m):
    items = []

    for i in range(1, m+1):
        items.append(Item(i))

    return Items(items)


def generate_valuations(agents, items, generator):
    for agent in agents:
        for item in items:
            valuation = generator.valuate(agent, item)
            agent.assign_valuation(item, valuation)
    