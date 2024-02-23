import random

from utils.allocation import Allocation
from utils.checkers import *
from utils.generator import *
from utils.helpers import print_allocation, print_valuations
from round_robin import round_robin
from utils.importer import import_from_file


a, i = import_from_file("instances/simple.txt")
print_valuations(a, i, 10)

# seed = 41569
seed = random.randint(1, 100_000)
random.seed(seed)
print(f"seed: {seed}\n")

n = 3
m = 5

agents = generate_agents(n)
items = generate_items(m)

generator = ValuationsGenerator()

generate_valuations(agents, items, generator)

print_valuations(agents, items, 100)

allocation = Allocation(agents)
ordering = [i for i in range(1, n+1)]

(allocation, items) = round_robin(agents, allocation, items, ordering, "inf")

print_allocation(allocation)

print(f"EF: {is_ef(agents, allocation)}")
print(f"EFX: {is_efx(agents, allocation)}")
print(f"EF1: {is_ef1(agents, allocation)}")