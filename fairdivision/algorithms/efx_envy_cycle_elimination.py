import networkx as nx # type: ignore
from typing import Optional

from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.items import Items


def efx_envy_cycle_elimination(agents: Agents, items: Items) -> Allocation:
    """
    Returns an allocation for the given `agents` and `items`.

    While there are still unallocated items, it gives the favorite one to the unenvied agent, breaking ties in favor of
    empty bundles. Additionally, it uses an envy graph to redistribute bundles if no unenvied agent is present.

    Envy graph is ensuring preserving EFX property.
    """

    items_left = items.copy()
    allocation = Allocation(agents)

    while items_left.size() > 0:
        graph = create_envy_graph(agents, items_left, allocation)

        unenvied_agent = get_unenvied_agent(graph, agents, allocation)

        while unenvied_agent is None:
            cycle = nx.find_cycle(graph)
            graph = eliminate_cycle(agents, items_left, cycle, allocation)

            unenvied_agent = get_unenvied_agent(graph, agents, allocation)

        favorite_item = unenvied_agent.get_favorite_item(items_left)
        allocation.allocate(unenvied_agent, favorite_item)
        items_left.remove_item(favorite_item)

    return allocation


def create_envy_graph(agents: Agents, items_left: Items, allocation: Allocation) -> nx.DiGraph:
    """
    Creates envy graph ensuring EFX from the given `allocation`.

    Each node in the graph is an agent. An edge `(i, j)` represents that the agent `i` envies the bundle of agent `j`.
    Only the agents with non-empty bundles can be envied so we only check envy towards them.

    Here, agent `i` does not envy agent `j` if after a hypothetical extension of agent `j`'s bundle by any unallocated
    item, agent `i` will still be EFX-satisifed. `allocation` is assumed to be EFX.
    """

    graph = nx.DiGraph()
    graph.add_nodes_from(agents)

    possibly_envied_agents = agents.copy()
    for agent in agents:
        if allocation.for_agent(agent).size() == 0:
            possibly_envied_agents.remove_agent(agent)
    
    for agent_i in agents:
        for agent_j in possibly_envied_agents:
            if agent_i != agent_j:
                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                # making sure that after allocating an item to agent j, agent i will be still EFX-satisfied
                valuation_of_j = agent_i.get_valuation(allocation.for_agent(agent_j))
                
                best_unallocated_valuation = agent_i.get_valuation(agent_i.get_favorite_item(items_left))

                items_of_j = allocation.for_agent(agent_j).get_items().copy()
                
                lowest_valuation = agent_i.get_valuation(agent_i.get_favorite_item(items_of_j))
                for item in items_of_j:
                    item_valuation =  agent_i.get_valuation(item)
                    if item_valuation < lowest_valuation:
                        lowest_valuation = item_valuation

                efx_ensuring_valuation_of_j = max(valuation_of_j + best_unallocated_valuation - lowest_valuation, valuation_of_j)

                # maybe adding edge
                if efx_ensuring_valuation_of_j > valuation_of_i:
                    graph.add_edge(agent_i, agent_j)

    return graph


def get_unenvied_agent(graph: nx.DiGraph, agents: Agents, allocation: Allocation) -> Optional[Agent]:
    """
    Returns unenvied agent if such exists.

    Ties are broken in favor of the agents with empty bundles to ensure 1/2-EFX allocation.
    """

    unenvied_agent = None

    for agent in agents:
        if graph.in_degree(agent) == 0:
            if allocation.for_agent(agent).size() == 0:
                unenvied_agent = agent
                break
            elif unenvied_agent is None:
                unenvied_agent = agent

    return unenvied_agent


def eliminate_cycle(agents: Agents, items_left: Items, cycle: list[tuple[Agent, Agent]], allocation: Allocation) -> nx.DiGraph:
    """
    Eliminates an envy cycle in the envy graph by redistributing bundles of the agents in `cycle`.

    Bundles are reallocated and then a new envy graph is created from scratch.
    """

    first_bundle = allocation.for_agent(cycle[0][0])

    for envious, envied in cycle[:-1]:
        allocation.allocate_bundle(envious, allocation.for_agent(envied))

    allocation.allocate_bundle(cycle[-1][0], first_bundle)

    return create_envy_graph(agents, items_left, allocation)
