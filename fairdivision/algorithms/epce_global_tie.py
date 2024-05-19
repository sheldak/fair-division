import math
import networkx as nx # type: ignore
from typing import Optional

from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.helpers import print_valuations, next_instance_to_file
from fairdivision.utils.items import Items


def epce_global_tie(agents: Agents, items: Items) -> Allocation:
    """
    Returns an allocation for the given `agents` and `items`.

    While there are still unallocated items, it gives the favorite one to an agent that will certainly preserve EFX
    property of the allocation. Additionally, it uses an envy graph to redistribute bundles if no such agent is
    present. In case that there are simultaneously no envy cycles and no agents preserving EFX property, algorithm
    starts from scratch but with a different priority order for breaking ties.

    The algorithm may try all possible permutations of priority order for breaking ties, but there is no guarantee that
    any of them will lead to an EFX allocation. In such a case an exception will be raised.
    """

    tie_break_index = 0
    max_tie_break_index = math.factorial(agents.size())

    while tie_break_index < max_tie_break_index:
        tie_break_order = get_tie_break_order(agents, tie_break_index)

        items_left = items.copy()
        allocation = Allocation(agents)

        while items_left.size() > 0:
            efx_preserving_agent = get_efx_preserving_agent(agents, items_left, tie_break_order, allocation)

            got_stuck = False
            
            while efx_preserving_agent is None:
                envy_graph = create_envy_graph(agents, allocation)

                try:
                    cycle = nx.find_cycle(envy_graph)

                    reallocate_bundles(cycle, allocation)
                    efx_preserving_agent = get_efx_preserving_agent(agents, items_left, tie_break_order, allocation)
                except nx.NetworkXNoCycle:
                    got_stuck = True
                    break

            if got_stuck:
                break

            favorite_item = efx_preserving_agent.get_favorite_item(items_left)
            allocation.allocate(efx_preserving_agent, favorite_item)
            items_left.remove_item(favorite_item)
        else:
            if tie_break_index >= 8:
                print(tie_break_index)
                print_valuations(agents, items)
                print()

                next_instance_to_file(agents, items, tie_break_index, "results/non_rec/results_5/")
            return allocation
        
        tie_break_index += 1
    else:
        print(tie_break_index)
        print_valuations(agents, items)
        print()

        next_instance_to_file(agents, items, tie_break_index, "results/non_rec/results_5/")
        raise Exception("No EFX allocation found")


def get_tie_break_order(agents: Agents, tie_break_index: int) -> list[Agent]:
    """
    Returns a unique permutaion of `agents` for every `tie_break_index`.

    When n is the number of agent, `tie_break_index` can be between 0 and n!, so each value `tie_break_index` matches
    exactly one permutation of agents.

    The permutations are created by iterating through agents and giving them one spot each in the `tie_break_order`
    list. Exact spots are determined by `tie_break_index`. The first agent lexicographically has n available spots. The
    interval [0, n!-1] is divided into n equal parts and depending on `tie_break_index`, one of n spots is chosen for
    the agent. Now, the number of available permutations is only (n-1)!. The second agent has n-1 available spots and
    has one assigned similarly to the previous agent. The algorithm continues until the last agent gets the last
    available spot.
    """
    
    n = agents.size()

    tie_break_order = [None for _ in agents]

    permutations_per_spot = math.factorial(n)

    if tie_break_index >= permutations_per_spot:
        raise Exception("`tie_break_index` is too large")
    
    for i in range(n, 0, -1):
        permutations_per_spot //= i

        spots_to_skip = tie_break_index // permutations_per_spot

        current_position = 0

        while tie_break_order[current_position] is not None or spots_to_skip > 0:
            if tie_break_order[current_position] is None:
                spots_to_skip -= 1
            
            current_position += 1

        tie_break_order[current_position] = agents.get_agents()[n - i]

        tie_break_index %= permutations_per_spot

    return tie_break_order


def get_efx_preserving_agent(agents: Agents, items_left: Items, tie_break_order: list[Agent], allocation: Allocation) -> Optional[Agent]:
    """
    Returns an agent that can get any item and preserve EFX property of `allocation` if such an agent exists.

    If many agents will preserve EFX property, the agent earliest in `tie_break_order` has priority.
    """

    for agent in tie_break_order:
        if allocation.for_agent(agent).size() == 0:
            return agent

    efx_preserving_agents = agents.copy()
    
    for agent_i in agents:
        for agent_j in agents:
            if agent_i != agent_j:
                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                # making sure that after allocating an item to agent j, agent i will be still EFX-satisfied
                valuation_of_j = agent_i.get_valuation(allocation.for_agent(agent_j))
                
                best_unallocated_valuation = agent_i.get_valuation(agent_i.get_favorite_item(items_left))

                items_of_j = allocation.for_agent(agent_j).get_items().copy()
                
                lowest_valuation = agent_i.get_valuation(items_of_j.get_items()[0])
                for item in items_of_j:
                    item_valuation =  agent_i.get_valuation(item)
                    if item_valuation < lowest_valuation:
                        lowest_valuation = item_valuation

                efx_ensuring_valuation_of_j = max(valuation_of_j + best_unallocated_valuation - lowest_valuation, valuation_of_j)

                # removing agent j if she may not preserve EFX property of the allocation after getting an item
                if efx_ensuring_valuation_of_j > valuation_of_i and agent_j in efx_preserving_agents:
                    efx_preserving_agents.remove_agent(agent_j)

    if efx_preserving_agents.size() == 0:
        return None
    else:
        for agent in tie_break_order:
            if agent in efx_preserving_agents:
                return agent


def create_envy_graph(agents: Agents, allocation: Allocation) -> nx.DiGraph:
    """
    Creates envy graph from the given `allocation`.

    Each node in the graph is an agent. An edge `(i, j)` represents that the agent `i` envies the bundle of agent `j`.
    Only the agents with non-empty bundles can be envied so only envy towards them is checked.
    """

    graph = nx.DiGraph()
    graph.add_nodes_from(agents)

    possibly_envied_agents = agents.copy()
    for agent in agents:
        if allocation.for_agent(agent).size() == 0:
            possibly_envied_agents.remove_agent(agent)
    
    for agent_i in agents:
        for agent_j in possibly_envied_agents:
            if agent_i.envies(agent_j, allocation):
                graph.add_edge(agent_i, agent_j)

    return graph


def reallocate_bundles(cycle: list[tuple[Agent, Agent]], allocation: Allocation) -> None:
    """
    Reallocates bundles according to `cycle` from envy graph.
    """

    first_bundle = allocation.for_agent(cycle[0][0])

    for envious, envied in cycle[:-1]:
        allocation.allocate_bundle(envious, allocation.for_agent(envied))

    allocation.allocate_bundle(cycle[-1][0], first_bundle)
