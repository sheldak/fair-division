from fairdivision.algorithms.envy_cycle_elimination import envy_cycle_elimination
from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.generators import generate_items
from fairdivision.utils.items import Items


# Implementation of Algorithm 1 from "New Fairness Concepts for Allocating Indivisible Item" by Caragiannis et al.
def ordered_picking(agents: Agents, items: Items) -> Allocation:
    """
    Returns an allocation for the given `agents` and `items`.

    In the beginning, an ordered instance is made by creating new items where their number matches the number of 
    original `items` and valuations of every agent are non-increasing as we move from the first item to the last in the
    order. The valuations for the new items are sorted valuations of the original `items` for every agent.

    Next, Envy-Cycle-Elimination is called on the ordered instance to produce an allocation.

    Finally, according to the allocation returned by Envy-Cycle-Elimination, a picking sequence is determined. The
    final allocation is created when `agents` are picking their favorite items from the original `items` in order
    in which they would pick items in the allocation for the ordered instance if they were picking in the 
    non-increasing order of valuations.

    The allocation has two main properties.
    
    It is epistemic envy free up to any positively valued good (EEFX) according to "New Fairness Concepts 
    for Allocating Indivisible Item" by Caragiannis et al.

    It is 2/3 maximin share fair (2/3-MMS) according to "Approximation Algorithms for Maximin Fair Division" by Barman
    and Krishnamurthy.
    """

    ordered_items = generate_items(items.size(), items.size() + 1)
    assign_valuations_in_order(agents, items, ordered_items)

    allocation_for_ordered = envy_cycle_elimination(agents, Allocation(agents), ordered_items)

    picking_sequence = get_picking_sequence(ordered_items, allocation_for_ordered)

    return pick_items(agents, items, picking_sequence)


def assign_valuations_in_order(agents: Agents, items: Items, ordered_items: Items) -> None:
    """
    Each agent has valuations assigned to all the items from `ordered_items`.

    For each agent valuations of the original `items` are sorted in the non-increasing order. Next `ordered_items` get
    these valuations in the same order. `items` and `ordered_items` are assumed to be of the same size.
    """

    if items.size() != ordered_items.size():
        raise Exception(f"Items and ordered_items should be of the same size. Found {items.size()} and {ordered_items.size()}")
    
    for agent in agents:
        items_valuations = sorted([agent.get_valuation(item) for item in items], reverse=True)
        
        for item, valuation in zip(ordered_items, items_valuations):
            agent.assign_valuation(item, valuation)


def get_picking_sequence(ordered_items: Items, allocation_for_ordered: Allocation) -> list[Agent]:
    """
    Creates a list of agents (where they can repeat) being a sequence in which they should pick items.

    The picking sequence represents an order in which the agents should pick the items to produce the same allocation
    as `allocation_for_ordered` when picking the items from `ordered_items` from the most valuable to the least.
    """

    picker_of = {}
    for agent, bundle in allocation_for_ordered.get_allocation():
        for item in bundle:
            picker_of[item] = agent

    picking_sequence = []
    for item in ordered_items:
        picking_sequence.append(picker_of[item])

    return picking_sequence


def pick_items(agents: Agents, items: Items, picking_sequence: list[Agent]) -> Allocation:
    """
    Creates an allocation where `agents` are picking favorite items in the order determined by `picking_sequence`.
    """

    allocation = Allocation(agents)
    items_left = items.copy()

    for picking_agent in picking_sequence:
        favorite_item = picking_agent.get_favorite_item(items_left)
        allocation.allocate(picking_agent, favorite_item)
        items_left.remove_item(favorite_item)

    return allocation
