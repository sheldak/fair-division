from fairdivision.all_allocations import all_allocations
from fairdivision.utils.generators import generate_agents, generate_items
from fairdivision.utils.importers import import_allocation_from_dict


EXPECTED_ALLOCATIONS = [
    {
        1: [1, 2],
        2: [],
        3: []
    },
    {
        1: [2],
        2: [1],
        3: []
    },
    {
        1: [2],
        2: [],
        3: [1]
    },
    {
        1: [1],
        2: [2],
        3: []
    },
    {
        1: [],
        2: [1, 2],
        3: []
    },
    {
        1: [],
        2: [2],
        3: [1]
    },
    {
        1: [1],
        2: [],
        3: [2]
    },
    {
        1: [],
        2: [1],
        3: [2]
    },
    {
        1: [],
        2: [],
        3: [1, 2]
    }
]


def test_all_allocations():
    agents = generate_agents(3)
    items = generate_items(2)

    for index, allocation in enumerate(all_allocations(agents, items)):
        expected_allocation = import_allocation_from_dict(agents, items, EXPECTED_ALLOCATIONS[index])

        assert allocation == expected_allocation
