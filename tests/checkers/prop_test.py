from fairdivision.utils.checkers import is_prop, highest_prop_approximation, prop_satisfied_factor
from fairdivision.utils.importers import import_from_file, import_allocation_from_dict

PROP_ALLOCATION = {
    1: [1],
    2: [2, 3],
    3: [4]
}

NOT_PROP_ALLOCATION = {
    1: [4],
    2: [2],
    3: [1, 3]
}


def test_prop_positive():
    agents, items, _ = import_from_file("instances/with_ef.txt")
    allocation = import_allocation_from_dict(agents, items, PROP_ALLOCATION)

    assert is_prop(agents, items, allocation) == True
    assert highest_prop_approximation(agents, items, allocation) == 1.0
    assert prop_satisfied_factor(agents, items, allocation) == 1.0


def test_prop_negative():
    agents, items, _ = import_from_file("instances/with_ef.txt")
    allocation = import_allocation_from_dict(agents, items, NOT_PROP_ALLOCATION)

    assert is_prop(agents, items, allocation) == (False, agents.get_agent(1))
    assert highest_prop_approximation(agents, items, allocation) == 0.5
    assert prop_satisfied_factor(agents, items, allocation) == 0.333
