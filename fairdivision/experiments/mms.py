import random

from fairdivision.algorithms.all_allocations import all_allocations

from fairdivision.utils.checkers import *
from fairdivision.utils.generators import *
from fairdivision.utils.helpers import print_allocation, print_valuations, get_maximin_shares


worst_mms = 1.0
tries = 1000

n = 3
m = 10

for i in range(tries):
    agents = generate_agents(n)
    items = generate_items(m)

    # seed = 74273
    seed = random.randint(1, 100_000_000)
    random.seed(seed)

    generator = AdditiveGenerator()

    generate_valuations(agents, items, generator)

    maximin_shares = get_maximin_shares(agents, items)
    highest_mms_with_allocation = (0.0, Allocation(agents))

    for allocation in all_allocations(agents, items):
        alpha = 1.0

        for agent in agents:
            valuation = agent.get_valuation(allocation.for_agent(agent))

            if valuation < maximin_shares[agent]:
                alpha = min(alpha, valuation / maximin_shares[agent])

        if alpha > highest_mms_with_allocation[0]:
            highest_mms_with_allocation = (alpha, allocation)

        if highest_mms_with_allocation[0] == 1.0:
            break

    highest_mms, allocation = highest_mms_with_allocation
    highest_mms = round(highest_mms, 3)

    print(f"{i}: {highest_mms}")

    if highest_mms < worst_mms:
        print(f"seed: {seed}\n")
        print(f"n={n}, m={m}\n")

        print_valuations(agents, items)

        print_allocation(allocation)

        print(f"highest MMS: {highest_mms}-MMS")

        worst_mms = highest_mms
