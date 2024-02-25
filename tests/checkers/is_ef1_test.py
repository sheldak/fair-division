from fairdivision.utils.checkers import is_ef1
from fairdivision.utils.importer import import_from_file, import_allocation_from_dict


EF1_ALLOCATION = {
    1: [3, 4],
    2: [2, 5],
    3: [1]
}

NOT_EF1_ALLOCATION = {
    1: [3],
    2: [4, 5],
    3: [1, 2]
}

def test_ef1_positive():
    agents, items, _ = import_from_file("instances/with_efx.txt")
    allocation = import_allocation_from_dict(agents, items, EF1_ALLOCATION)

    assert is_ef1(agents, allocation)

def test_ef1_negative():
    agents, items, _ = import_from_file("instances/with_efx.txt")
    allocation = import_allocation_from_dict(agents, items, NOT_EF1_ALLOCATION)

    assert is_ef1(agents, allocation) == (False, (agents.get_agent(1), agents.get_agent(3)))
