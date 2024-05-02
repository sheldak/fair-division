from typing import Literal, Optional

from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.items import Items


# Implementation of Algorithm 2 from "Multiple birds with one stone: Beating 1/2 for EFX and GMMS via envy cycle
# elimination" by Amanatidis et al.
def round_robin(
        agents: Agents, 
        items: Items, 
        allocation: Optional[Allocation] = None, 
        ordering: Optional[list[int]] = None, 
        steps: int | Literal["inf"] = "inf") -> tuple[Allocation, Items]:
    """
    Returns an allocation for the given `agents`, `items` and optional partial `allocation`.

    Gives favourite unallocated item to each agent in the order optionally specified by `ordering`. If not specified,
    the ordering is lexicographical. Terminates if either there are no more items to distribute, or `steps` items have
    been assigned by the algorithm.
    """

    items_left = items.copy()

    if allocation is None:
        allocation = Allocation(agents)

    if ordering is None:
        ordering = agents.get_indices()
    
    step = 0
    while items_left.size() > 0 and (steps == "inf" or step < steps):
        agent = agents.get_agent(ordering[step % agents.size()])
        favorite_item = agent.get_favorite_item(items_left)
        
        allocation.allocate(agent, favorite_item)

        items_left.remove_item(favorite_item)

        step += 1

    return (allocation, items_left)
