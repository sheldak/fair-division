from io import TextIOWrapper

from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.generator import generate_agents, generate_items
from fairdivision.utils.items import Items


RESTRICTIONS = ["additive"]

def import_from_file(file_path: str) -> tuple[Agents, Items, list[str]]:
    with open(file_path, "r") as file:
        lines = split_into_lines(file)

        restrictions = parse_restrictions(lines[0])
        n, m = parse_agents_and_items(lines[1])

        if len(lines) < n + 2:
            raise Exception(f"There should be {n} lines with valuations, found {len(lines) - 2}")

        agents = generate_agents(n)
        items = generate_items(m)

        if "additive" in restrictions:
            for i in range(2, n + 2):
                agent_number = i - 1
                parse_valuations(lines[i], agents.get_agent(agent_number), items)
        
        return agents, items, restrictions


def parse_restrictions(line: str) -> list[str]:
    restrictions = list(filter(lambda restriction: restriction in RESTRICTIONS, split_and_strip(line)))

    return restrictions


def parse_agents_and_items(line: str) -> tuple[int, int]:
    line_as_list = split_and_strip(line)
    if len(line_as_list) != 2:
        raise Exception(f"Expected a number of agents and a number of items in the second line, got {line}")
    
    return int(line_as_list[0]), int(line_as_list[1])


def parse_valuations(line: str, agent: Agent, items: Items) -> None:
    valuations = [int(valuation) for valuation in split_and_strip(line)]

    if len(valuations) != items.size():
        raise Exception(f"Expected {items.size()} valuations in every line, found a line with {len(valuations)}")
    
    for i in range(len(valuations)):
        item_number = i + 1
        agent.assign_valuation(items.get_item(item_number), valuations[i])


def split_into_lines(file: TextIOWrapper) -> list[str]:
    stripped_lines = [line.strip() for line in file.read().split("\n")]

    return list(filter(lambda line: len(line) > 0, stripped_lines))


def split_and_strip(line: str) -> list[str]:
    return [word.strip() for word in line.split(" ")]


def import_allocation_from_dict(agents: Agents, items: Items, allocation_dict: dict[int, list[int]]) -> Allocation:
    allocation = Allocation(agents)
    
    for agent_index, bundle_list in allocation_dict.items():
        agent = agents.get_agent(agent_index)

        for item_index in bundle_list:
            allocation.allocate(agent, items.get_item(item_index))

    return allocation