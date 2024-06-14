import networkx as nx # type: ignore
import os

from fairdivision.algorithms.all_allocations import all_allocations
from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.items import Items


def get_maximin_shares(agents: Agents, items: Items) -> dict[Agent, int]:
    """
    Returns a dictionary mapping each agent to her maximin share value.

    The maximin share of an agent is the highest valuation that the agent can receive from her allocated bundle if she
    were to split all items into a number of bundles equal to the number of agents and receive the worst bundle.
    """

    maximin_shares = dict([(agent, 0) for agent in agents])

    for possible_allocation in all_allocations(agents, items):
        for agent in agents:
            worst_valuation = min([agent.get_valuation(bundle) for _, bundle in possible_allocation.get_allocation()])
            maximin_shares[agent] = max(maximin_shares[agent], worst_valuation)

    return maximin_shares


def export_to_file(agents: Agents, items: Items, file_path: str) -> None:
    """
    Exports Agents, Items and a list of valuations to the file `file_path`.

    The file will follow the standard of fair division instance described in the README.md file.
    """

    with open(file_path, "a") as file:
        file.write("additive\n")
        file.write(f"{agents.size()} {items.size()}\n")

        for agent in agents:
            file.write(f"{agent.get_valuation(items.get_items()[0])}")

            for item in items.get_items()[1:]:
                file.write(f" {agent.get_valuation(item)}")

            if agent != agents.get_agents()[-1]:
                file.write("\n")


def print_envy_graph(graph: nx.DiGraph) -> None:
    """
    Pretty prints adjacency list of `graph` .

    For example:

        GRAPH
        Agent(1): [Agent(2), Agent(3)]
        Agent(2): [Agent(3)]
        Agent(3): []

    """

    print("GRAPH")
    for envious, envied in graph.adj.items():
        print(f"{envious}: {[agent for agent, _attr in envied.items()]}")

    print()


def print_allocation(allocation: Allocation) -> None:
    """
    Pretty prints `allocation`.

    For example:

        ALLOCATION
        Agent(1): Bundle([1, 2])
        Agent(2): Bundle([3, 4])
        Agent(3): Bundle([5])

    """

    print("ALLOCATION")
    for agent, bundle in allocation:
        print(f"{agent}: {bundle}")

    print()


def print_valuations(agents: Agents, items: Items) -> None:
    """
    Prints valuations of single items for all agents in a table.

    For example:
        ```
           | g1  | g2  | g3  | g4  |
        ---|-----|-----|-----|-----|
        a1 | 10  | 20  | 30  | 40  |
        a2 | 50  | 60  | 70  | 100 |
        ```
    """

    max_value = 0
    for agent in agents:
        for item in items:
            max_value = max(max_value, agent.get_valuation(item))

    row_length = number_length(agents.size()) + 1
    column_length = number_length(max(max_value, items.size() * 10))

    table = f"{generate_header(items, row_length, column_length)}\n"

    for agent_index in agents.get_indices():
        agent = agents.get_agent(agent_index)
        table += f"{generate_row(agent, items, row_length, column_length)}\n"

    print(table)
    

# -- PRIVATE FUNCTIONS --

def generate_header(items: Items, row_length: int, column_length: int) -> str:
    # first line
    header = " " * row_length + " |"

    for item_index in items.get_indices():
        item_length = number_length(item_index) + 1
        empty = " " * (column_length - item_length)

        header += f" g{item_index}{empty} |"

    # second line
    header += "\n" + "-" * row_length + "-|"
    for _ in items:
        dashes = "-" * column_length
        header += f"-{dashes}-|"

    return header


def generate_row(agent: Agent, items: Items, row_length: int, column_length: int) -> str:
    agent_index = agent.get_index()

    agent_length = number_length(agent_index) + 1
    empty = " " * (row_length - agent_length)

    row = f"a{agent_index}{empty} |"

    for item_index in items.get_indices():
        item = items.get_item(item_index)
        valuation = agent.get_valuation(item)

        valuation_length = number_length(valuation)
        empty = " " * (column_length - valuation_length)

        row += f" {valuation}{empty} |"

    return row


def number_length(number: int) -> int:
    if number == 0:
        return 1

    length = 0
    
    while number > 0:
        length += 1
        number //= 10

    return length
