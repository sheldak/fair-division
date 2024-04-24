import random

from fairdivision.algorithms.all_allocations import all_allocations
from fairdivision.algorithms.envy_cycle_elimination import envy_cycle_elimination
from fairdivision.algorithms.ordered_picking import ordered_picking
from fairdivision.algorithms.round_robin import round_robin

from fairdivision.utils.allocation import Allocation
from fairdivision.utils.checkers import *
from fairdivision.utils.generators import *
from fairdivision.utils.helpers import print_allocation, print_valuations
from fairdivision.utils.importers import import_from_file


# seed = 31350826
seed = random.randint(1, 100_000)
random.seed(seed)
print(f"seed: {seed}\n")

n = 100
m = 2000

agents, items, restrictions = import_from_file(f"instances/ordered_picking_0333_ef1.txt")

# agents = generate_agents(n)
# items = generate_items(m)

# generator = AdditiveGenerator(min=0, max=10000)
# generator = OrderedGenerator(min=0, max=10000)

# generate_valuations(agents, items, generator)

print_valuations(agents, items)

allocation = Allocation(agents)
# ordering = [i for i in range(1, n+1)]

# (allocation, items_left) = round_robin(agents, allocation, items, ordering, "inf")
allocation = envy_cycle_elimination(agents, allocation, items)
# allocation = ordered_picking(agents, items)

print_allocation(allocation)

print(f"EF: {is_ef(agents, allocation)}\n")

efx = is_efx(agents, allocation)
print(f"EFX: {efx}")
if not efx == True:
    print(f"highest EFX: {highest_efx_approximation(agents, allocation)}-EFX")
print()

ef1 = is_ef1(agents, allocation)
print(f"EF1: {ef1}")
if not ef1 == True:
    print(f"highest EF1: {highest_ef1_approximation(agents, allocation)}-EF1")
print()

# mms = is_mms(agents, items, allocation)
# print(f"MMS: {mms}")
# if not mms == True:
#     print(f"highest MMS: {highest_mms_approximation(agents, items, allocation)}-MMS")
# print()


