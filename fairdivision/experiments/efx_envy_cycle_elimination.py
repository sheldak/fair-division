import random

from fairdivision.algorithms.envy_cycle_elimination import envy_cycle_elimination
from fairdivision.algorithms.efx_envy_cycle_elimination import efx_envy_cycle_elimination
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.checkers import *
from fairdivision.utils.generators import *
from fairdivision.utils.helpers import print_allocation, print_valuations


worst_efx = 1.0
tries = 30000

n = 3
m = 5

for i in range(tries):
    print(i, end=" ")
    agents = generate_agents(n)
    items = generate_items(m)

    # seed = 74273
    seed = random.randint(1, 100_000_000)
    print(seed)
    random.seed(seed)

    generator = AdditiveGenerator(min=0, max=10)
    # generator = OrderedGenerator()

    generate_valuations(agents, items, generator)
    print_valuations(agents, items)

    allocation = efx_envy_cycle_elimination(agents, items)

    if not is_efx(agents, allocation) == True:
        highest_efx = highest_efx_approximation(agents, allocation)
        
        print(f"seed: {seed}\n")
        print(f"n={n}, m={m}\n")

        print_valuations(agents, items)

        print_allocation(allocation)

        print(f"highest EFX: {highest_efx}-EFX")

        worst_efx = highest_efx
        break
