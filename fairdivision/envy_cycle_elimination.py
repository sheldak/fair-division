import networkx as nx
from typing import Optional

from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.items import Items


def envy_cycle_elimination(agents: Agents, allocation: Allocation, items: Items) -> Allocation:
    """
    Returns a full allocation for the given `agents`, `items` and partial `allocation`.

    For each unallocated items gives it to the unenvied agent, breaking ties in favor of empty bundles. Additionally, 
    uses envy graph to redistribute bundles if no unenvied agent is present.
    """
     
    graph = initialize_graph(agents, allocation)

    for item in items:
        unenvied_agent = get_unenvied_agent(graph, agents, allocation)
        
        while unenvied_agent is None:
            cycle = nx.find_cycle(graph)
            allocation = eliminate_cycle(graph, cycle, allocation)

            unenvied_agent = get_unenvied_agent(graph, agents, allocation)
        
        allocation.allocate(unenvied_agent, item)

        update_graph(graph, agents, allocation, unenvied_agent)

    return allocation


def initialize_graph(agents: Agents, allocation: Allocation) -> nx.DiGraph:
    """
    Initializes envy graph from the given `allocation`.

    Each node in the graph is an agent. An edge `(i, j)` represents that the agent `i` envies the bundle of agent `j`.
    """

    graph = nx.DiGraph()
    graph.add_nodes_from(agents)
    
    for agent_i in agents:
        for agent_j in agents:
            if agent_i != agent_j:
                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))
                valuation_of_j = agent_i.get_valuation(allocation.for_agent(agent_j))

                if valuation_of_j > valuation_of_i:
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


def eliminate_cycle(graph: nx.DiGraph, cycle: list[tuple[Agent, Agent]], allocation: Allocation) -> Allocation:
    """
    Eliminates an envy cycle in envy `graph` by redistributing bundles of the agents in `cycle`.
    """

    first_bundle = allocation.for_agent(cycle[0][0])

    for envious, envied in cycle[:-1]:
        allocation.allocate_bundle(envious, allocation.for_agent(envied))

    allocation.allocate_bundle(cycle[-1][0], first_bundle)

    graph.remove_edges_from(cycle)

    return allocation


def update_graph(graph: nx.DiGraph, agents: Agents, allocation: Allocation, endowed_agent: Agent) -> None:
    """
    Updates the envy `graph` after a new item was allocated to `endowed_agent`.
    """

    # deleting neighbours that the endowed agent no longer envies
    for previously_envied in graph[endowed_agent].copy():
        valuation_of_allocated_bundle = endowed_agent.get_valuation(allocation.for_agent(endowed_agent))
        valuation_of_other_bundle = endowed_agent.get_valuation(allocation.for_agent(previously_envied))

        if valuation_of_allocated_bundle >= valuation_of_other_bundle:
            graph.remove_edge(endowed_agent, previously_envied)

    # adding envy towards the endowed agent
    for agent in agents:
        valuation_of_allocated_bundle = agent.get_valuation(allocation.for_agent(agent))
        valuation_of_new_bundle = agent.get_valuation(allocation.for_agent(endowed_agent))

        if valuation_of_new_bundle > valuation_of_allocated_bundle:
            graph.add_edge(agent, endowed_agent)