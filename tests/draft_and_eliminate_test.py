from math import sqrt
import os

from fairdivision.algorithms.draft_and_eliminate import draft_and_eliminate
from fairdivision.utils.checkers import is_ef1, highest_efx_approximation
from fairdivision.utils.importers import import_from_file


PHI = (1 + sqrt(5)) / 2


# Draft and Eliminate returns an EF1 allocation for every additive instance.
# Shown in "Multiple birds with one stone: Beating 1/2 for EFX and GMMS via envy cycle
# elimination" by Amanatidis et al.
def test_draft_and_eliminate_ef1():
    for file_name in os.listdir("instances"):
        agents, items, restrictions = import_from_file(f"instances/{file_name}")
        if "additive" in restrictions:
            allocation = draft_and_eliminate(agents, items)

            assert is_ef1(agents, allocation) == True


# Draft and Eliminate returns a 0.618-EFX allocation for every additive instance.
# Shown in "Multiple birds with one stone: Beating 1/2 for EFX and GMMS via envy cycle
# elimination" by Amanatidis et al.
def test_draft_and_eliminate_efx_approximation():
    for file_name in os.listdir("instances"):
        agents, items, restrictions = import_from_file(f"instances/{file_name}")
        if "additive" in restrictions:
            allocation = draft_and_eliminate(agents, items)

            assert highest_efx_approximation(agents, allocation) >= PHI - 1
