import networkx as nx

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
        unenvied_agent = None
        for agent in agents:
            if graph.in_degree(agent) == 0:
                # prefering agents with empty bundles to get 1/2-EFX allocation
                if allocation.for_agent(agent).size() == 0:
                    unenvied_agent = agent
                    break
                elif unenvied_agent is None:
                    unenvied_agent = agent
        
        if unenvied_agent is None:
            cycle = nx.find_cycle(graph)
            allocation = eliminate_cycle(graph, cycle, allocation)

        allocation.allocate(agent, item)

        update_graph(graph, agents, allocation, agent)

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


def update_graph(graph: nx.DiGraph, agents: Agents, allocation: Allocation, agent_with_new_item: Agent) -> None:
    """
    Updates the envy `graph` after a new item was allocated to `agent_with_new_item`.
    """

    for agent in agents:
        valuation_of_allocated_bundle = agent.get_valuation(allocation.for_agent(agent))
        valuation_of_new_bundle = agent.get_valuation(allocation.for_agent(agent_with_new_item))

        if valuation_of_new_bundle > valuation_of_allocated_bundle:
            graph.add_edge(agent, agent_with_new_item)