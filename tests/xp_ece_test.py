import os

from fairdivision.algorithms.xp_ece import xp_ece, get_efx_preserving_agent
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.checkers import is_efx0
from fairdivision.utils.generators import generate_agents, generate_items
from fairdivision.utils.importers import import_allocation_from_dict, import_from_file


ALLOCATION = {
    1: [1],
    2: [2, 3],
}


def test_xp_ece_efx():
    for file_name in os.listdir("instances"):
        if file_name != "efx_ece_stuck.txt":
            agents, items, restrictions = import_from_file(f"instances/{file_name}")
            print(file_name)
            if "additive" in restrictions:
                allocation = xp_ece(agents, items)

                assert is_efx0(agents, allocation) == True


def test_get_efx_preserving_agent_one_agent_empty_bundle():
    agents = generate_agents(2)
    items = generate_items(2)

    agents.get_agent(1).assign_valuation(items.get_item(1), 1)
    agents.get_agent(1).assign_valuation(items.get_item(2), 1)
    agents.get_agent(2).assign_valuation(items.get_item(1), 1)
    agents.get_agent(2).assign_valuation(items.get_item(2), 1)

    allocation = Allocation(agents)

    allocation.allocate(agents.get_agent(1), items.get_item(1))

    items_left = items.copy()
    items_left.remove_item(items.get_item(1))

    tie_break_order = agents.get_agents()
    tie_break_order_reversed = list(reversed(agents.get_agents()))

    assert agents.get_agent(2) == get_efx_preserving_agent(agents, items_left, tie_break_order, allocation)
    assert agents.get_agent(2) == get_efx_preserving_agent(agents, items_left, tie_break_order_reversed, allocation)


def test_get_efx_preserving_agent_one_agent_non_empty_bundle():
    agents = generate_agents(2)
    items = generate_items(4)

    agents.get_agent(1).assign_valuation(items.get_item(1), 5)
    agents.get_agent(1).assign_valuation(items.get_item(2), 2)
    agents.get_agent(1).assign_valuation(items.get_item(3), 2)
    agents.get_agent(1).assign_valuation(items.get_item(4), 2)


    agents.get_agent(2).assign_valuation(items.get_item(1), 5)
    agents.get_agent(2).assign_valuation(items.get_item(2), 1)
    agents.get_agent(2).assign_valuation(items.get_item(3), 1)
    agents.get_agent(2).assign_valuation(items.get_item(4), 1)

    allocation = import_allocation_from_dict(agents, items, ALLOCATION)

    items_left = items
    items_left.remove_item(items.get_item(1))
    items_left.remove_item(items.get_item(2))
    items_left.remove_item(items.get_item(3))

    tie_break_order = agents.get_agents()

    assert agents.get_agent(2) == get_efx_preserving_agent(agents, items_left, tie_break_order, allocation)


def test_get_efx_preserving_agent_more_agents_all_empty():
    agents = generate_agents(2)
    items = generate_items(2)

    agents.get_agent(1).assign_valuation(items.get_item(1), 1)
    agents.get_agent(1).assign_valuation(items.get_item(2), 1)
    agents.get_agent(2).assign_valuation(items.get_item(1), 1)
    agents.get_agent(2).assign_valuation(items.get_item(2), 1)

    allocation = Allocation(agents)

    tie_break_order = agents.get_agents()
    tie_break_order_reversed = list(reversed(agents.get_agents()))

    assert agents.get_agent(1) == get_efx_preserving_agent(agents, items, tie_break_order, allocation)
    assert agents.get_agent(2) == get_efx_preserving_agent(agents, items, tie_break_order_reversed, allocation)


def test_get_efx_preserving_agent_more_agents_none_empty():
    agents = generate_agents(2)
    items = generate_items(4)

    agents.get_agent(1).assign_valuation(items.get_item(1), 5)
    agents.get_agent(1).assign_valuation(items.get_item(2), 2)
    agents.get_agent(1).assign_valuation(items.get_item(3), 3)
    agents.get_agent(1).assign_valuation(items.get_item(4), 1)


    agents.get_agent(2).assign_valuation(items.get_item(1), 5)
    agents.get_agent(2).assign_valuation(items.get_item(2), 2)
    agents.get_agent(2).assign_valuation(items.get_item(3), 3)
    agents.get_agent(2).assign_valuation(items.get_item(4), 1)

    allocation = import_allocation_from_dict(agents, items, ALLOCATION)

    items_left = items
    items_left.remove_item(items.get_item(1))
    items_left.remove_item(items.get_item(2))
    items_left.remove_item(items.get_item(3))

    tie_break_order = agents.get_agents()
    tie_break_order_reversed = list(reversed(agents.get_agents()))

    assert agents.get_agent(1) == get_efx_preserving_agent(agents, items_left, tie_break_order, allocation)
    assert agents.get_agent(2) == get_efx_preserving_agent(agents, items_left, tie_break_order_reversed, allocation)


def test_get_efx_preserving_agent_no_agents():
    agents = generate_agents(2)
    items = generate_items(4)

    agents.get_agent(1).assign_valuation(items.get_item(1), 5)
    agents.get_agent(1).assign_valuation(items.get_item(2), 3)
    agents.get_agent(1).assign_valuation(items.get_item(3), 3)
    agents.get_agent(1).assign_valuation(items.get_item(4), 2)

    agents.get_agent(2).assign_valuation(items.get_item(1), 5)
    agents.get_agent(2).assign_valuation(items.get_item(2), 2)
    agents.get_agent(2).assign_valuation(items.get_item(3), 2)
    agents.get_agent(2).assign_valuation(items.get_item(4), 1)

    allocation = import_allocation_from_dict(agents, items, ALLOCATION)

    items_left = items
    items_left.remove_item(items.get_item(1))
    items_left.remove_item(items.get_item(2))
    items_left.remove_item(items.get_item(3))

    tie_break_order = agents.get_agents()

    assert get_efx_preserving_agent(agents, items_left, tie_break_order, allocation) is None
