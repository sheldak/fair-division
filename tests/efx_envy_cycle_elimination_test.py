import os

from fairdivision.algorithms.efx_envy_cycle_elimination import efx_envy_cycle_elimination
from fairdivision.utils.checkers import is_efx
from fairdivision.utils.importers import import_from_file


def test_efx_envy_cycle_elimination_efx():
    for file_name in os.listdir("instances"):
        if file_name != "efx_ece_stuck.txt":
            agents, items, restrictions = import_from_file(f"instances/{file_name}")
            print(file_name)
            if "additive" in restrictions:
                allocation = efx_envy_cycle_elimination(agents, items)

                assert is_efx(agents, allocation) == True
