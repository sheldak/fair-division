import random

from fairdivision.algorithms.envy_cycle_elimination import envy_cycle_elimination
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.checkers import *
from fairdivision.utils.generators import *
from fairdivision.utils.helpers import print_allocation, print_valuations


worst_efx = 1.0
tries = 30000

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

    allocation = envy_cycle_elimination(agents, items)

    highest_efx = highest_efx_approximation(agents, allocation)

    if highest_efx < worst_efx:
        print(f"seed: {seed}\n")
        print(f"n={n}, m={m}\n")

        print_valuations(agents, items)

        print_allocation(allocation)

        print(f"highest EFX: {highest_efx}-EFX")

        worst_efx = highest_efx

    if not is_ef1(agents, allocation):
        print(f"seed: {seed}\n")
        print(f"n={n}, m={m}\n")

        print_valuations(agents, items)

        print_allocation(allocation)

        print(f"highest EFX: {highest_efx}-EFX")

        print("!!! NOT EF1 !!!")
        break
