from fairdivision.utils.checkers import is_eefx
from fairdivision.utils.importers import import_from_file, import_allocation_from_dict


EEFX_ALLOCATION = {
    1: [5],
    2: [1, 4],
    3: [2, 3]
}

NOT_EEFX_ALLOCATION = {
    1: [1, 3],
    2: [4, 5],
    3: [2]
}


def test_eefx_positive():
    agents, items, _ = import_from_file("instances/with_efx.txt")
    allocation = import_allocation_from_dict(agents, items, EEFX_ALLOCATION)

    assert is_eefx(agents, items, allocation) == True


def test_eefx_negative():
    agents, items, _ = import_from_file("instances/with_efx.txt")
    allocation = import_allocation_from_dict(agents, items, NOT_EEFX_ALLOCATION)

    assert is_eefx(agents, items, allocation) == (False, agents.get_agent(3))
