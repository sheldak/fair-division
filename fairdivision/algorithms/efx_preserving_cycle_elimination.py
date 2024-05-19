import math
import networkx as nx # type: ignore
from typing import Optional

from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.helpers import print_valuations, next_instance_to_file
from fairdivision.utils.items import Items


def efx_preserving_cycle_elimination(agents: Agents, items: Items) -> Allocation:
    """
    Returns an allocation for the given `agents` and `items`.

    While there are still unallocated items, it gives the favorite one to an agent that will certainly preserve EFX
    property of the allocation. Additionally, it uses an envy graph to redistribute bundles if no such agent is
    present. In case that there are simultaneously no envy cycles and no agents preserving EFX property, algorithm
    starts from scratch but with a different priority order for breaking ties.

    The algorithm may try all possible permutations of priority order for breaking ties, but there is no guarantee that
    any of them will lead to an EFX allocation. In such a case an exception will be raised.
    """

    stuck_counter = 0
    tie_break_indices = initialize_tie_break_indices(items)

    while tie_break_indices is not None:
        current_tie_break_position = 0

        items_left = items.copy()
        allocation = Allocation(agents)

        while items_left.size() > 0:
            tie_break_order = get_tie_break_order(agents, tie_break_indices[current_tie_break_position])

            efx_preserving_agent, tie_present = get_efx_preserving_agent(agents, items_left, tie_break_order, allocation)

            got_stuck = False

            while efx_preserving_agent is None:
                envy_graph = create_envy_graph(agents, allocation)

                try:
                    cycle = nx.find_cycle(envy_graph)

                    reallocate_bundles(cycle, allocation)
                    efx_preserving_agent, tie_present = get_efx_preserving_agent(agents, items_left, tie_break_order, allocation)
                except nx.NetworkXNoCycle:
                    got_stuck = True
                    break

            if got_stuck:
                tie_break_indices = next_tie_break_indices(agents, tie_break_indices)
                stuck_counter += 1
                break

            favorite_item = efx_preserving_agent.get_favorite_item(items_left)
            allocation.allocate(efx_preserving_agent, favorite_item)
            items_left.remove_item(favorite_item)

            if tie_present:
                current_tie_break_position += 1
        else:
            n = agents.size()
            # if (n == 2 and stuck_counter >= 3) or (n == 3 and stuck_counter >= 4) or (n == 4 and stuck_counter >= 6) or (n == 5 and stuck_counter >= 24):
            #     print(stuck_counter)
            #     print_valuations(agents, items)
            #     print()

                # next_instance_to_file(agents, items, stuck_counter, directory)

            return allocation
    else:
        print(stuck_counter)
        print_valuations(agents, items)
        print()

        # next_instance_to_file(agents, items, stuck_counter, directory)
        raise Exception("No EFX allocation found")


def initialize_tie_break_indices(items: Items) -> list[int]:
    return [0 for _ in range(items.size())]


def next_tie_break_indices(agents: Agents, tie_break_indices: list[int]) -> Optional[list[int]]:
    if agents.size() == 1:
        return None

    m = len(tie_break_indices)

    max_tie_break_index = math.factorial(agents.size())

    if m == 1:
        if tie_break_indices[0] + 1 < max_tie_break_index:
            return [tie_break_indices[0] + 1]
        else:
            return None

    next_tie_break_indices = tie_break_indices.copy()

    same_indices_size = 1
    for i in range(m-2, -1, -1):
        if tie_break_indices[i] == tie_break_indices[i+1]:
            same_indices_size += 1
        else:
            break

    previous_highest = all(map(lambda index: index == max_tie_break_index - 1, tie_break_indices[:(m - same_indices_size)]))
    same_indices_second_highest = all(map(lambda index: index == max_tie_break_index - 2, tie_break_indices[(m - same_indices_size):]))
    
    # the last tie break indices
    if same_indices_size == 1 and previous_highest and same_indices_second_highest:
        return None
    
    all_same_and_highest = same_indices_size == m and tie_break_indices[0] == max_tie_break_index - 1

    # the end of the list with the same indices will shrink by one 
    if all_same_and_highest or (not same_indices_size == m and previous_highest and same_indices_second_highest):
        return [0 for _ in range(m - same_indices_size + 1)] + [1 for _ in range(same_indices_size - 1)]
    # the end of the list with the same indices will continue to have the same size
    else:
        # all same indices but not last indices
        if same_indices_size == m:
            return [tie_break_indices[0] + 1 for _ in range(m)]
        else:
            same_indices_value = tie_break_indices[-1]

            # The end of the list with the same indices has the highest number, so previous index is not the highest.
            # Thus, the end of the list can contain all 0s, and the previous index increases by 1
            if same_indices_value == max_tie_break_index - 1:
                next_tie_break_indices[(m - same_indices_size):] = [0 for _ in range(same_indices_size)]
                next_tie_break_indices[m - same_indices_size - 1] += 1

                return next_tie_break_indices
            # The end of the list with the same indices has the second highest number, and the previous index has the highest.
            # Thus, the end of the list will become all 1s, and the previous indices behave as an incremented number with base being 
            # `max_tie_break_index`.
            elif same_indices_value == max_tie_break_index - 2 and tie_break_indices[m - same_indices_size - 1] == max_tie_break_index - 1:
                next_tie_break_indices[(m - same_indices_size):] = [1 for _ in range(same_indices_size)]
                
                for i in range(m - same_indices_size - 1, -1, -1):
                    if tie_break_indices[i] + 1 == max_tie_break_index:
                        next_tie_break_indices[i] = 0
                    else:
                        next_tie_break_indices[i] += 1
                        return next_tie_break_indices
            # The other case when the end of the list can safely increase by 1, or 2 in case of previous index being larger exactly by 1.
            else:
                if same_indices_value + 1 == tie_break_indices[m - same_indices_size - 1]:
                    new_same_value = same_indices_value + 2
                else:
                    new_same_value = same_indices_value + 1

                next_tie_break_indices[(m - same_indices_size):] = [new_same_value for _ in range(same_indices_size)]
                return next_tie_break_indices


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


def get_efx_preserving_agent(agents: Agents, items_left: Items, tie_break_order: list[Agent], allocation: Allocation) -> tuple[Optional[Agent], bool]:
    """
    Returns an agent that can get any item and preserve EFX property of `allocation` if such an agent exists.

    If many agents will preserve EFX property, the agent earliest in `tie_break_order` has priority.
    """

    efx_preserving_agent = None

    for agent in tie_break_order:
        if allocation.for_agent(agent).size() == 0:
            if efx_preserving_agent is None:
                efx_preserving_agent = agent
            else:
                return efx_preserving_agent, True
            
    if efx_preserving_agent is not None:
        return efx_preserving_agent, False

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
        return None, False
    elif efx_preserving_agents.size() == 1:
        return list(efx_preserving_agents)[0], False
    else:
        for agent in tie_break_order:
            if agent in efx_preserving_agents:
                return agent, True


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
