from typing import Literal

from utils.agent import Agent
from utils.agents import Agents
from utils.allocation import Allocation
from utils.item import Item
from utils.items import Items


def round_robin(
        agents: Agents, 
        allocation: Allocation, 
        items: Items, 
        ordering: list[int], 
        steps: int | Literal["inf"] = "inf") -> tuple[Allocation, Items]:
    step = 0
    while items.size() > 0 and (steps == "inf" or step < steps):
        agent = agents.get_agent(ordering[step % agents.size()])
        favorite_item = agent.get_favorite_item(items)
        
        allocation.allocate(agent, favorite_item)

        items.delete_item(favorite_item)

        step += 1

    return (allocation, items)
