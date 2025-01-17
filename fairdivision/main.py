import random

from fairdivision.algorithms.all_allocations import all_allocations
from fairdivision.algorithms.draft_and_eliminate import draft_and_eliminate
from fairdivision.algorithms.envy_cycle_elimination import envy_cycle_elimination
from fairdivision.algorithms.fast_envy_cycle_elimination import fast_envy_cycle_elimination
from fairdivision.algorithms.ordered_picking import ordered_picking
from fairdivision.algorithms.round_robin import round_robin
from fairdivision.algorithms.xp_ece import xp_ece

from fairdivision.utils.allocation import Allocation
from fairdivision.utils.checkers import *
from fairdivision.utils.generators import *
from fairdivision.utils.helpers import print_allocation, print_valuations
from fairdivision.utils.importers import import_from_file


seed = 6923741
seed = random.randint(1, 100_000)
random.seed(seed)
print(f"seed: {seed}\n")

agents, items, restrictions = import_from_file(f"instances/ordered_picking_05_ef1.txt")

# n = 2
# m = 5

# agents = generate_agents(n)
# items = generate_items(m)

# generator = AdditiveGenerator()
# generator = OrderedGenerator()

# generate_valuations(agents, items, generator)

print_valuations(agents, items)

# (allocation, items_left) = round_robin(agents, items)
# allocation = fast_envy_cycle_elimination(agents, items)
# allocation = envy_cycle_elimination(agents, items)
# allocation = draft_and_eliminate(agents, items)
allocation = xp_ece(agents, items)

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
    print(f"fraction of EF1-satisfied agents: {ef1_satisfied_fraction(agents, allocation)}")
print()
