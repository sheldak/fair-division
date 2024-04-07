from typing import Literal

from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.items import Items


# Implementation of Algorithm 2 from "Multiple birds with one stone: Beating 1/2 for EFX and GMMS via envy cycle
# elimination" by Amanatidis et al.
def round_robin(
        agents: Agents, 
        allocation: Allocation, 
        items: Items, 
        ordering: list[int], 
        steps: int | Literal["inf"] = "inf") -> tuple[Allocation, Items]:
    """
    Returns an allocation for the given `agents`, `items` and partial `allocation`.

    Gives favourite unallocated item to each agent in the order specified by `ordering`. Terminates if either there are
    no more items to distribute, or `steps` items have been assigned by the algorithm.
    """

    items_left = items.copy()
    
    step = 0
    while items_left.size() > 0 and (steps == "inf" or step < steps):
        agent = agents.get_agent(ordering[step % agents.size()])
        favorite_item = agent.get_favorite_item(items_left)
        
        allocation.allocate(agent, favorite_item)

        items_left.delete_item(favorite_item)

        step += 1

    return (allocation, items_left)
