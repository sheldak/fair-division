from fairdivision.utils.checkers import is_mms, highest_mms_approximation
from fairdivision.utils.importers import import_from_file, import_allocation_from_dict

MMS_ALLOCATION = {
    1: [4, 5],
    2: [2, 3],
    3: [1]
}

NOT_MMS_ALLOCATION = {
    1: [3, 4],
    2: [2, 5],
    3: [1]
}


def test_mms_positive():
    agents, items, _ = import_from_file("instances/with_efx.txt")
    allocation = import_allocation_from_dict(agents, items, MMS_ALLOCATION)

    assert is_mms(agents, items, allocation) == True
    assert highest_mms_approximation(agents, items, allocation) == 1


def test_mms_negative():
    agents, items, _ = import_from_file("instances/with_efx.txt")
    allocation = import_allocation_from_dict(agents, items, NOT_MMS_ALLOCATION)

    assert is_mms(agents, items, allocation) == (False, agents.get_agent(1))
    assert highest_mms_approximation(agents, items, allocation) == 0.667
