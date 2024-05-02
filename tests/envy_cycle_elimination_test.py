import os

from fairdivision.algorithms.envy_cycle_elimination import envy_cycle_elimination
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.checkers import is_ef1, is_efx, highest_efx_approximation, highest_mms_approximation
from fairdivision.utils.importers import import_from_file


# Envy Cycle Elimination returns an EF1 allocation for every additive instance.
# Shown in "On approximately fair allocations of indivisible goods" by Lipton et al.
def test_envy_cycle_elimination_ef1():
    for file_name in os.listdir("instances"):
        agents, items, restrictions = import_from_file(f"instances/{file_name}")
        if "additive" in restrictions:
            allocation = envy_cycle_elimination(agents, items)

            assert is_ef1(agents, allocation) == True


# Envy Cycle Elimination returns an 1/2-EFX allocation for every additive instance.
# Shown in "Maximin-aware allocations of indivisible goods" by Chan et al.
def test_envy_cycle_elimination_efx_approximation():
    for file_name in os.listdir("instances"):
        agents, items, restrictions = import_from_file(f"instances/{file_name}")
        if "additive" in restrictions:
            allocation = envy_cycle_elimination(agents, items)

            assert highest_efx_approximation(agents, allocation) >= 1/2

# Envy Cycle Elimination returns an 1/2-MMS allocation for every additive instance.
# Shown in "Fair Division of Indivisible Goods: Recent Progress and Open Questions" by Amanatidis et al.
def test_envy_cycle_elimination_mms_approximation():
    for file_name in os.listdir("instances"):
        agents, items, restrictions = import_from_file(f"instances/{file_name}")
        if "additive" in restrictions:
            allocation = envy_cycle_elimination(agents, items)

            assert highest_mms_approximation(agents, items, allocation) >= 1/2


# Envy Cycle Elimination returns an EFX allocation for an ordered additive instance.
# Shown in "Almost envy-freeness with general valuations" by Plaut and Roughgarden.
def test_envy_cycle_elimination_ordered_efx():
    agents, items, _ = import_from_file(f"instances/ordered.txt")
    allocation = envy_cycle_elimination(agents, items)

    assert is_efx(agents, allocation) == True
