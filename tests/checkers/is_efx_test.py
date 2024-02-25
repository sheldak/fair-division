from fairdivision.utils.checkers import is_efx
from fairdivision.utils.importer import import_from_file, import_allocation_from_dict


EFX_ALLOCATION = {
    1: [4, 5],
    2: [2, 3],
    3: [1]
}

NOT_EFX_ALLOCATION = {
    1: [3, 4],
    2: [2, 5],
    3: [1]
}


def test_ef1_positive():
    agents, items, _ = import_from_file("instances/with_efx.txt")
    allocation = import_allocation_from_dict(agents, items, EFX_ALLOCATION)

    assert is_efx(agents, allocation)

def test_ef1_negative():
    agents, items, _ = import_from_file("instances/with_efx.txt")
    allocation = import_allocation_from_dict(agents, items, NOT_EFX_ALLOCATION)

    assert is_efx(agents, allocation) == (False, (agents.get_agent(1), agents.get_agent(2)))
