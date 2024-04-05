import random

from fairdivision.envy_cycle_elimination import envy_cycle_elimination
from fairdivision.round_robin import round_robin
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.checkers import *
from fairdivision.utils.generators import *
from fairdivision.utils.helpers import print_allocation, print_valuations
from fairdivision.utils.importers import import_from_file

from fairdivision.all_allocations import all_allocations


# seed = 41569
seed = random.randint(1, 100_000)
random.seed(seed)
print(f"seed: {seed}\n")

n = 2
m = 5

# agents, items, restrictions = import_from_file(f"instances/envy_cycle.txt")

agents = generate_agents(n)
items = generate_items(m)

generator = AdditiveGenerator()

generate_valuations(agents, items, generator)

print_valuations(agents, items, 100)

allocation = Allocation(agents)
ordering = [i for i in range(1, n+1)]

(allocation, items) = round_robin(agents, allocation, items, ordering, "inf")
# allocation = envy_cycle_elimination(agents, allocation, items)

print_allocation(allocation)
print()

print(f"EF: {is_ef(agents, allocation)}")
print(f"EFX: {is_efx(agents, allocation)} ({highest_efx_approximation(agents, allocation)}-EFX)")
print(f"EF1: {is_ef1(agents, allocation)} ({highest_ef1_approximation(agents, allocation)}-EF1)")
