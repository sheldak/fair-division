import networkx as nx # type: ignore
from typing import Optional

from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.items import Items


def envy_cycle_elimination(agents: Agents, allocation: Allocation, items: Items) -> Allocation:
    """
    Returns a full allocation for the given `agents`, `items` and partial `allocation`.

    While there are still unallocated items, it gives the favorite one to the unenvied agent, breaking ties in favor of
    empty bundles. Additionally, it uses an envy graph to redistribute bundles if no unenvied agent is present.
    """

    items_left = items.copy()
    graph = create_envy_graph(agents, allocation)

    while items_left.size() > 0:
        unenvied_agent = get_unenvied_agent(graph, agents, allocation)

        while unenvied_agent is None:
            cycle = nx.find_cycle(graph)
            graph = eliminate_cycle(agents, cycle, allocation)

            unenvied_agent = get_unenvied_agent(graph, agents, allocation)

        favorite_item = unenvied_agent.get_favorite_item(items_left)
        allocation.allocate(unenvied_agent, favorite_item)
        items_left.remove_item(favorite_item)

        update_graph(graph, agents, allocation, unenvied_agent)

    return allocation


def create_envy_graph(agents: Agents, allocation: Allocation) -> nx.DiGraph:
    """
    Creates envy graph from the given `allocation`.

    Each node in the graph is an agent. An edge `(i, j)` represents that the agent `i` envies the bundle of agent `j`.
    Only the agents with non-empty bundles can be envied so we only check envy towards them.
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


def eliminate_cycle(agents: Agents, cycle: list[tuple[Agent, Agent]], allocation: Allocation) -> nx.DiGraph:
    """
    Eliminates an envy cycle in the envy graph by redistributing bundles of the agents in `cycle`.

    Bundles are reallocated and then a new envy graph is created from scratch.
    """

    first_bundle = allocation.for_agent(cycle[0][0])

    for envious, envied in cycle[:-1]:
        allocation.allocate_bundle(envious, allocation.for_agent(envied))

    allocation.allocate_bundle(cycle[-1][0], first_bundle)

    return create_envy_graph(agents, allocation)


def update_graph(graph: nx.DiGraph, agents: Agents, allocation: Allocation, endowed_agent: Agent) -> None:
    """
    Updates the envy `graph` after a new item was allocated to `endowed_agent`.
    """

    # deleting envy towards the agents that endowed agent no longer envies
    for previously_envied in graph[endowed_agent].copy():
        if not endowed_agent.envies(previously_envied, allocation):
            graph.remove_edge(endowed_agent, previously_envied)

    # adding envy towards the endowed agent
    for agent in agents:
        if agent.envies(endowed_agent, allocation):
            graph.add_edge(agent, endowed_agent)
