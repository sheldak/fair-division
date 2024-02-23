import random

from utils.agent import Agent
from utils.agents import Agents
from utils.bundle import Bundle
from utils.item import Item
from utils.items import Items


class ValuationsGenerator:
    def __init__(self, additive: bool = True, min: int = 0, max: int = 100):
        self.additive: bool = additive
        self.min: int = min
        self.max: int = max

    def valuate(self, agent: Agent, item_or_bundle: Item | Bundle) -> int:
        if self.additive:
            return self.valuate_additively(agent, item_or_bundle)
        else:
            if agent.has_valuation(item_or_bundle):
                return agent.get_valuation(item_or_bundle)
            else:
                return random.randint(self.min, self.max)
    
    def valuate_additively(self, agent: Agent, item_or_bundle: Item | Bundle) -> int:
        if isinstance(item_or_bundle, Item):
            return self.valuate_item(agent, item_or_bundle)
        elif isinstance(item_or_bundle, Bundle):
            valuation = 0

            for item in item_or_bundle.items:
                valuation += self.valuate_item(agent, item)

            return valuation
        else:
            raise Exception(f"Can only valuate item or bundle, got {item_or_bundle}")

    def valuate_item(self, agent: Agent, item: Item) -> int:
        if agent.has_valuation(item):
            return agent.get_valuation(item)
        else:
            return random.randint(self.min, self.max)


def generate_agents(n: int) -> Agents:
    agents = []

    for i in range(1, n+1):
        agents.append(Agent(i))

    return Agents(agents)


def generate_items(m: int) -> Items:
    items = []

    for i in range(1, m+1):
        items.append(Item(i))

    return Items(items)


def generate_valuations(agents: Agents, items: Items, generator: ValuationsGenerator) -> None:
    for agent in agents:
        for item in items:
            valuation = generator.valuate(agent, item)
            agent.assign_valuation(item, valuation)
    