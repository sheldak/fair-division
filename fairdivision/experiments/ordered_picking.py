import random

from fairdivision.algorithms.ordered_picking import ordered_picking
from fairdivision.utils.checkers import *
from fairdivision.utils.generators import *
from fairdivision.utils.helpers import print_allocation, print_valuations


worst_mms = 1.0
tries = 1000

n = 10
m = 100

for i in range(tries):
    agents = generate_agents(n)
    items = generate_items(m)

    # seed = 74273
    seed = random.randint(1, 100_000_000)
    random.seed(seed)

    generator = AdditiveGenerator()

    generate_valuations(agents, items, generator)

    allocation = ordered_picking(agents, items)

    highest_mms = highest_mms_approximation(agents, items, allocation)

    if highest_mms < worst_mms:
        print(f"seed: {seed}\n")
        print(f"n={n}, m={m}\n")

        print_valuations(agents, items)

        print_allocation(allocation)

        print(f"highest MMS: {highest_mms}-MMS")

        worst_mms = highest_mms

    if not is_ef1(agents, allocation):
        print(f"seed: {seed}\n")
        print(f"n={n}, m={m}\n")

        print_valuations(agents, items)

        print_allocation(allocation)

        print(f"highest MMS: {highest_mms}-MMS")

        print("!!! NOT EF1 !!!")
        break
