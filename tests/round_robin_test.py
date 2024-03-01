import os

from fairdivision.round_robin import round_robin
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.checkers import is_ef1
from fairdivision.utils.importer import import_from_file


# Round Robin returns an EF1 allocation for every additive instance.
# Proven in "The unreasonable fairness of maximum Nash welfare" by Caragiannis et al.
def test_round_robin_ef1():
    for file_name in os.listdir("instances"):
        agents, items, restrictions = import_from_file(f"instances/{file_name}")
        if "additive" in restrictions:
            allocation = Allocation(agents)
            ordering = [i for i in range(1, agents.size()+1)]

            allocation, remaining_items = round_robin(agents, allocation, items, ordering)

            assert remaining_items.size() == 0
            assert is_ef1(agents, allocation) == True