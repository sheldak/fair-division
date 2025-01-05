import networkx as nx # type: ignore
import random
from typing import Optional

from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.items import Items


def xp_ece(agents: Agents, items: Items, max_attempts: int = 1000) -> Allocation:
    """
    Returns an allocation for the given `agents` and `items`.

    While there are still unallocated items, it gives the favorite one to an agent that will certainly preserve the EFX
    property of the allocation. If more agents are preserving EFX, one is chosen according to a random priority order.
    Additionally, the algorithm uses an envy graph to redistribute bundles if no EFX-preserving agent is present. In
    case there are simultaneously no envy cycles and no agents preserving EFX property, the algorithm starts from
    scratch. A new tie-breaking order is randomly generated for every attempt to give an item, so each rerun of the
    algorithm may differ.
    """

    for _ in range(max_attempts):
        items_left = items.copy()
        allocation = Allocation(agents)

        while items_left.size() > 0:
            tie_break_order = get_random_tie_break_order(agents)

            efx_preserving_agent = get_efx_preserving_agent(agents, items_left, tie_break_order, allocation)

            while efx_preserving_agent is None:
                envy_graph = create_envy_graph(agents, allocation)

                try:
                    cycle = nx.find_cycle(envy_graph)

                    reallocate_bundles(cycle, allocation)
                    efx_preserving_agent = get_efx_preserving_agent(agents, items_left, tie_break_order, allocation)
                except nx.NetworkXNoCycle:
                    break

            if efx_preserving_agent is None:
                break
            else:
                favorite_item = efx_preserving_agent.get_favorite_item(items_left)
                allocation.allocate(efx_preserving_agent, favorite_item)
                items_left.remove_item(favorite_item)
        else:
            return allocation

    raise Exception("No EFX allocation found")


def get_random_tie_break_order(agents: Agents) -> list[Agent]:
    """
    Returns a random permutaion of `agents`.
    """

    tie_break_order = agents.get_agents().copy()
    random.shuffle(tie_break_order)

    return tie_break_order


def get_efx_preserving_agent(
        agents: Agents, 
        items_left: Items, 
        tie_break_order: list[Agent], 
        allocation: Allocation) -> Optional[Agent]:
    """
    Returns an agent who, after receiving any item, maintains the EFX property of `allocation`. If no such agent
    exists, it returns None.

    If multiple agents preserve the EFX property, the agent earliest in `tie_break_order` has priority.
    """

    for agent_j in tie_break_order:
        if allocation.for_agent(agent_j).size() == 0:
            return agent_j
        else:
            for agent_i in agents:
                if agent_i != agent_j:
                    valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                    # making sure that after allocating an item to agent j, agent i will be still EFX-satisfied
                    valuation_of_j = agent_i.get_valuation(allocation.for_agent(agent_j))

                    best_unallocated_valuation = agent_i.get_valuation(agent_i.get_favorite_item(items_left))

                    items_of_j = allocation.for_agent(agent_j).get_items().copy()

                    lowest_valuation_of_j = agent_i.get_valuation(items_of_j.get_items()[0])
                    for item in items_of_j:
                        item_valuation =  agent_i.get_valuation(item)
                        if item_valuation < lowest_valuation_of_j:
                            lowest_valuation_of_j = item_valuation

                    efx_ensuring_valuation_of_j = max(
                        valuation_of_j + best_unallocated_valuation - lowest_valuation_of_j, 
                        valuation_of_j
                    )

                    # skipping agent j if she may not preserve EFX property of the allocation after getting an item
                    if efx_ensuring_valuation_of_j > valuation_of_i:
                        break
            else:
                return agent_j
            
    return None


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
