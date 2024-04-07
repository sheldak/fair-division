import random

from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.bundle import Bundle
from fairdivision.utils.item import Item
from fairdivision.utils.items import Items


class ValuationsGenerator:
    def valuate(self, agent, item_or_bundle):
        raise Exception(f"Valuation function not implemented")


class AdditiveGenerator(ValuationsGenerator):
    """
    A class for generating additive valuations.

    Valuations are integers taken uniformly at random from interval [`min`, `max`], where `min` and `max` are optional
    parameters given during the instantiation of the class.
    """

    def __init__(self, additive: bool = True, min: int = 0, max: int = 100):
        self.additive: bool = additive
        self.min: int = min
        self.max: int = max

    def valuate(self, agent: Agent, item_or_bundle: Item | Bundle) -> int:
        """
        Returns valuation of `item_or_bundle` for `agent`.

        If `agent` already has a valuation for `item_or_bundle`, it is returned. Otherwise, the valuation is generated
        uniformly at random.
        """

        if isinstance(item_or_bundle, Item):
            return self.__valuate_item(agent, item_or_bundle)
        elif isinstance(item_or_bundle, Bundle):
            valuation = 0

            for item in item_or_bundle.items:
                valuation += self.__valuate_item(agent, item)

            return valuation
        else:
            raise Exception(f"Can only valuate item or bundle, got {item_or_bundle}")

    def __valuate_item(self, agent: Agent, item: Item) -> int:
        if agent.has_valuation(item):
            return agent.get_valuation(item)
        else:
            return random.randint(self.min, self.max)


def generate_agents(n: int) -> Agents:
    """
    Generates `n` agents and put them into `Agents` object.

    Indices of agents are from `1` to `n` inclusive.
    """

    agents = []

    for i in range(1, n+1):
        agents.append(Agent(i))

    return Agents(agents)


def generate_items(m: int, start_index: int = 1) -> Items:
    """
    Generates `m` items and put them into `Items` object.

    Indices of items are from `1` to `m` inclusive.
    """

    items = []

    for i in range(start_index, start_index + m):
        items.append(Item(i))

    return Items(items)


def generate_valuations(agents: Agents, items: Items, generator: ValuationsGenerator) -> None:
    """
    Generates and assigns valuations of `items` for `agents` using provided `generator`.
    """

    for agent in agents:
        for item in items:
            valuation = generator.valuate(agent, item)
            agent.assign_valuation(item, valuation)
