import os

from fairdivision.algorithms.round_robin import round_robin
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.checkers import is_ef1, highest_mms_approximation
from fairdivision.utils.helpers import get_maximin_shares
from fairdivision.utils.importers import import_from_file


# Round Robin returns an EF1 allocation for every additive instance.
# Shown in "The unreasonable fairness of maximum Nash welfare" by Caragiannis et al.
def test_round_robin_ef1():
    for file_name in os.listdir("instances"):
        agents, items, restrictions = import_from_file(f"instances/{file_name}")
        if "additive" in restrictions:
            allocation = Allocation(agents)
            ordering = [i for i in range(1, agents.size()+1)]

            allocation, remaining_items = round_robin(agents, allocation, items, ordering)

            assert remaining_items.size() == 0
            assert is_ef1(agents, allocation) == True


# Round Robin returns an 1/2-MMS allocation for every additive instance if there is no item that any agent values at
# least 1/2 of their maximin share.
# Shown in "Approximation algorithms for computing maximin share allocations" by Amanatidis et al.
def test_round_robin_mms_approximation():
    for file_name in os.listdir("instances"):
        agents, items, restrictions = import_from_file(f"instances/{file_name}")
        if "additive" in restrictions:
            valid_instance = True
            maximin_share = get_maximin_shares(agents, items)

            for agent in agents:
                for item in items:
                    if agent.has_valuation(item) > 0.5 * maximin_share[agent]:
                        valid_instance = False

            if valid_instance:
                allocation = Allocation(agents)
                ordering = [i for i in range(1, agents.size()+1)]

                allocation, remaining_items = round_robin(agents, allocation, items, ordering)

                assert remaining_items.size() == 0
                assert highest_mms_approximation(agents, items, allocation) >= 1/2
