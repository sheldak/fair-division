from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.items import Items


def print_allocation(allocation: Allocation) -> None:
    """
    Pretty prints `allocation`.

    For example:

        Agent(1): Bundle([1, 2])
        Agent(2): Bundle([3, 4])
        Agent(3): Bundle([5])
    """

    for agent, bundle in allocation:
        print(f"{agent}: {bundle}")


def print_valuations(agents: Agents, items: Items, max_value: int) -> None:
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