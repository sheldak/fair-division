from fairdivision.utils.checkers import is_ef
from fairdivision.utils.importers import import_from_file, import_allocation_from_dict


EF_ALLOCATION = {
    1: [2, 3],
    2: [4],
    3: [1]
}

NOT_EF_ALLOCATION = {
    1: [1],
    2: [2, 3],
    3: [4]
}

def test_ef_positive():
    agents, items, _ = import_from_file("instances/with_ef.txt")
    allocation = import_allocation_from_dict(agents, items, EF_ALLOCATION)

    assert is_ef(agents, allocation) == True

def test_ef_negative():
    agents, items, _ = import_from_file("instances/with_ef.txt")
    allocation = import_allocation_from_dict(agents, items, NOT_EF_ALLOCATION)

    assert is_ef(agents, allocation) == (False, (agents.get_agent(1), agents.get_agent(2)))