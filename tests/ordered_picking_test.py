import os

from fairdivision.algorithms.ordered_picking import ordered_picking

from fairdivision.utils.checkers import highest_mms_approximation, is_eefx
from fairdivision.utils.importers import import_from_file


# Ordered Picking returns an EEFX allocation for every additive instance.
# Shown in "New Fairness Concepts for Allocating Indivisible Items" by Caragiannis et al.
def test_ordered_picking_eefx():
    for file_name in os.listdir("instances"):
        agents, items, restrictions = import_from_file(f"instances/{file_name}")
        if "additive" in restrictions:
            allocation = ordered_picking(agents, items)

            assert is_eefx(agents, items, allocation) == True


# Ordered Picking returns an 2/3-MMS allocation for every additive instance.
# Shown in "Approximation Algorithms for Maximin Fair Division" by Barman and Krishnamurthy.
def test_ordered_picking_mms_approximation():
    for file_name in os.listdir("instances"):
        agents, items, restrictions = import_from_file(f"instances/{file_name}")
        if "additive" in restrictions:
            allocation = ordered_picking(agents, items)

            assert highest_mms_approximation(agents, items, allocation) >= 0.667
