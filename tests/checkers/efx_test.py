from fairdivision.utils.checkers import is_efx, is_efx0, highest_efx_approximation, highest_efx0_approximation, efx_satisfied_fraction, efx0_satisfied_fraction
from fairdivision.utils.importers import import_from_file, import_allocation_from_dict


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


def test_efx_positive():
    agents, items, _ = import_from_file("instances/with_efx.txt")
    allocation = import_allocation_from_dict(agents, items, EFX_ALLOCATION)

    assert is_efx(agents, allocation) == True
    assert highest_efx_approximation(agents, allocation) == 1.0
    assert efx_satisfied_fraction(agents, allocation) == 1.0

    assert is_efx0(agents, allocation) == True
    assert highest_efx0_approximation(agents, allocation) == 1.0
    assert efx0_satisfied_fraction(agents, allocation) == 1.0


def test_efx_negative():
    agents, items, _ = import_from_file("instances/with_efx.txt")
    allocation = import_allocation_from_dict(agents, items, NOT_EFX_ALLOCATION)

    assert is_efx(agents, allocation) == (False, (agents.get_agent(1), agents.get_agent(2)))
    assert highest_efx_approximation(agents, allocation) == 0.667
    assert efx_satisfied_fraction(agents, allocation) == 0.667

    assert is_efx0(agents, allocation) == (False, (agents.get_agent(1), agents.get_agent(2)))
    assert highest_efx0_approximation(agents, allocation) == 0.667
    assert efx0_satisfied_fraction(agents, allocation) == 0.667

EFX_BUT_NOT_EFX0_ALLOCATION = {
    1: [1, 2],
    2: [3, 4]
}

def test_efx_but_not_efx0():
    agents, items, _ = import_from_file("instances/with_zero.txt")
    allocation = import_allocation_from_dict(agents, items, EFX_BUT_NOT_EFX0_ALLOCATION)

    assert is_efx(agents, allocation) == True
    assert highest_efx_approximation(agents, allocation) == 1.0
    assert efx_satisfied_fraction(agents, allocation) == 1.0

    assert is_efx0(agents, allocation) == (False, (agents.get_agent(2), agents.get_agent(1)))
    assert highest_efx0_approximation(agents, allocation) == 0.667
    assert efx0_satisfied_fraction(agents, allocation) == 0.5
