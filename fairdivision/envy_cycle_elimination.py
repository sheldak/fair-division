import networkx as nx

from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.items import Items


def envy_cycle_elimination(agents: Agents, allocation: Allocation, items: Items) -> Allocation:
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
            allocation = eliminate_cycle(cycle, allocation)

        allocation.allocate(agent, item)

        update_graph(graph, agents, allocation, agent)

    return allocation


def initialize_graph(agents: Agents, allocation: Allocation) -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.add_nodes_from(agents)
    
    for agent_1 in agents:
        for agent_2 in agents:
            if agent_1 != agent_2:
                valuation_of_1 = agent_1.get_valuation(allocation.for_agent(agent_1))
                valuation_of_2 = agent_1.get_valuation(allocation.for_agent(agent_2))

                if valuation_of_2 > valuation_of_1:
                    graph.add_edge(agent_1, agent_2)

    return graph


def eliminate_cycle(cycle: list[tuple[Agent, Agent]], allocation: Allocation) -> Allocation:
    first_bundle = allocation.for_agent(cycle[0][0])

    for envious, envied in cycle[:-1]:
        allocation.allocate_bundle(envious, allocation.for_agent(envied))

    allocation.allocate_bundle(cycle[-1][0], first_bundle)

    return allocation


def update_graph(graph: nx.DiGraph, agents: Agents, allocation: Allocation, agent_with_new_item: Agent) -> None:
    for agent in agents:
        valuation_of_agent = agent.get_valuation(allocation.for_agent(agent))
        valuation_of_new_bundle = agent.get_valuation(allocation.for_agent(agent_with_new_item))

        if valuation_of_new_bundle > valuation_of_agent:
            graph.add_edge(agent, agent_with_new_item)