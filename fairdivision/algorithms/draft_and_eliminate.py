from math import sqrt

from fairdivision.algorithms.envy_cycle_elimination import envy_cycle_elimination
from fairdivision.algorithms.round_robin import round_robin
from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.item import Item
from fairdivision.utils.items import Items


PHI = (1 + sqrt(5)) / 2


# Implementation of Algorithm 3 from "Multiple birds with one stone: Beating 1/2 for EFX and GMMS via envy cycle
# elimination" by Amanatidis et al.
def draft_and_eliminate(agents: Agents, items: Items) -> Allocation:
    """
    Returns an allocation for the given `agents` and `items`.

    The algorithm starts with determining an ordering of agents in which they will choose their first items. "Quite
    happy" agents are the ones who are particularly satisfied after receiving their first item. They choose it before
    the other agents. Next, everyone except the "quite happy" agents receives a second item, but in the reversed
    ordering. Finally, Envy Cycle Elimination is called to redistribute the remaining items.
    """
     
    n = agents.size()
    ordering, quite_happy_n = preprocessing(agents, items)

    allocation = Allocation(agents)
    allocation, items_left = round_robin(agents, items, allocation, ordering, n)

    reversed_ordering = list(reversed(ordering))
    allocation, items_left = round_robin(agents, items_left, allocation, reversed_ordering, n - quite_happy_n)

    return envy_cycle_elimination(agents, items_left, allocation)


# Implementation of Algorithm 4 from "Multiple birds with one stone: Beating 1/2 for EFX and GMMS via envy cycle
# elimination" by Amanatidis et al.
def preprocessing(agents: Agents, items: Items) -> tuple[list[int], int]:
    """
    Creates ordering of `agents` for distribution of the first one to two items per agent, and decides how many agents
    will be "quite happy" with only one item.

    Each agent chooses a favorite item in lexicographical order. An agent is made "quite happy" if she values an
    already chosen (assigned) item (but not to an already existing "quite happy" agent) more than her favorite item
    among the unassigned ones with a factor equal to at least the golden ratio (about 1.618). Then, she has the item
    assigned, and the previous owner will have another chance of choosing an item. Each agent can choose at most one
    item.
    """

    m = items.size()

    agents_left = agents.copy()
    items_left = items.copy()

    ordering = []
    quite_happy_agents = Agents([])

    # agents who have associated items, but are not quite happy
    processed = Agents([])
    items_owners: dict[Item, Agent] = {}

    # items assigned to `processed`` agents
    assigned = Items([])

    # time of receiving the final item for each agent
    timestamps: dict[Agent, int] = {}

    while agents_left.size() > 0 and items_left.size() > 0:
        timestamp = m - items_left.size() + 1
        
        agent = agents_left.get_agents()[0]
        favorite_unassigned = agent.get_favorite_item(items_left)
        
        if is_extremely_envious(agent, favorite_unassigned, assigned):
            favorite_assigned = agent.get_favorite_item(assigned)

            previous_owner = items_owners[favorite_assigned]
            processed.remove_agent(previous_owner)
            assigned.remove_item(favorite_assigned)

            agents_left.add_agent(previous_owner)

            del items_owners[favorite_assigned]
            quite_happy_agents.add_agent(agent)

            ordering.append(agent.get_index())
        else:
            processed.add_agent(agent)
            assigned.add_item(favorite_unassigned)

            items_owners[favorite_unassigned] = agent
            items_left.remove_item(favorite_unassigned)

        agents_left.remove_agent(agent)
        timestamps[agent] = timestamp
    
    for agent in sorted(processed, key=lambda agent: timestamps[agent]):
        ordering.append(agent.get_index())

    return ordering, quite_happy_agents.size()


def is_extremely_envious(agent: Agent, favorite_unassigned: Item, assigned: Items) -> bool:
    """
    Checks if `agent` values any already assigned item more than `favorite_unassigned` with a factor of at least 1.618.
    """
    
    if assigned.size() > 0:
        favorite_unassigned_valuation = agent.get_valuation(favorite_unassigned)

        favorite_assigned = agent.get_favorite_item(assigned)
        favorite_assigned_valuation = agent.get_valuation(favorite_assigned)

        return favorite_assigned_valuation > PHI * favorite_unassigned_valuation
    else:
        return False
