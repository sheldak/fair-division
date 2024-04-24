import random

from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.bundle import Bundle
from fairdivision.utils.item import Item
from fairdivision.utils.items import Items


class ValuationsGenerator:
    def valuate_items(self, items):
        raise Exception(f"Valuation function not implemented")


class AdditiveGenerator(ValuationsGenerator):
    """
    A class for generating additive valuations.

    Valuations are integers taken uniformly at random from interval [`min`, `max`], where `min` and `max` are optional
    parameters given during the instantiation of the class.
    """

    def __init__(self, min: int = 0, max: int = 100):
        self.min: int = min
        self.max: int = max

    def valuate_items(self, items: Items) -> list[int]:
        """
        Returns list of valuations of `items` for `agent`.

        The valuation is generated uniformly at random.
        """

        return [random.randint(self.min, self.max) for _ in items]


class OrderedGenerator(ValuationsGenerator):
    """
    A class for generating additive valuations which valuate items in the same ranking for every agent.

    Valuations are integers taken uniformly at random from interval [`min`, `max`], where `min` and `max` are optional
    parameters given during the instantiation of the class.
    """

    def __init__(self, min: int = 0, max: int = 100):
        self.min: int = min
        self.max: int = max

    def valuate_items(self, items: Items) -> list[int]:
        """
        Returns list of valuations of `items` for `agent`.

        The valuation is generated uniformly at random. Valuations are ordered in the descending order.
        """

        return sorted([random.randint(self.min, self.max) for _ in items], reverse=True)


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
        valuations = generator.valuate_items(items)

        for item, valuation in zip(items.get_items(), valuations):
            agent.assign_valuation(item, valuation)
