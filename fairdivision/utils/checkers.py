from typing import Literal

from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.bundle import Bundle


def is_ef(agents: Agents, allocation: Allocation) -> Literal[True] | tuple[Literal[False], tuple[Agent, Agent]]:
    for agent_i in agents:
        for agent_j in agents:
            if agent_i != agent_j:
                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))
                valuation_of_j = agent_i.get_valuation(allocation.for_agent(agent_j))

                if valuation_of_j > valuation_of_i:
                    return (False, (agent_i, agent_j))
                
    return True


def is_efx(agents: Agents, allocation: Allocation) -> Literal[True] | tuple[Literal[False], tuple[Agent, Agent]]:
    for agent_i in agents:
        for agent_j in agents:
            if agent_i != agent_j:
                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                for item_to_remove in allocation.for_agent(agent_j):
                    items_subset = allocation.for_agent(agent_j).copy()
                    items_subset.delete_item(item_to_remove)

                    valuation_of_j = agent_i.get_valuation(items_subset)

                    if valuation_of_j > valuation_of_i:
                        return (False, (agent_i, agent_j))
                
    return True


def highest_efx_approximation(agents: Agents, allocation: Allocation) -> float:
    alpha = 1

    for agent_i in agents:
        for agent_j in agents:
            if agent_i != agent_j:
                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                for item_to_remove in allocation.for_agent(agent_j):
                    items_subset = allocation.for_agent(agent_j).copy()
                    items_subset.delete_item(item_to_remove)

                    valuation_of_j = agent_i.get_valuation(items_subset)

                    if valuation_of_j > valuation_of_i:
                        # assumes non-negative valuations
                        alpha = min(alpha, valuation_of_i / valuation_of_j)
                
    return round(alpha, 3)


def is_ef1(agents: Agents, allocation: Allocation) -> Literal[True] | tuple[Literal[False], tuple[Agent, Agent]]:
    for agent_i in agents:
        for agent_j in agents:
            if agent_i != agent_j:
                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                for item_to_remove in allocation.for_agent(agent_j):
                    items_subset = allocation.for_agent(agent_j).copy()
                    items_subset.delete_item(item_to_remove)

                    valuation_of_j = agent_i.get_valuation(items_subset)

                    if valuation_of_i >= valuation_of_j:
                        break
                else:
                    return (False, (agent_i, agent_j)) 
                
    return True


def highest_ef1_approximation(agents: Agents, allocation: Allocation) -> float:
    alpha = 1

    for agent_i in agents:
        for agent_j in agents:
            if agent_i != agent_j:
                agent_i_alpha = 0

                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                for item_to_remove in allocation.for_agent(agent_j):
                    items_subset = allocation.for_agent(agent_j).copy()
                    items_subset.delete_item(item_to_remove)

                    valuation_of_j = agent_i.get_valuation(items_subset)

                    if valuation_of_i >= valuation_of_j:
                        break
                    else:
                        agent_i_alpha = max(agent_i_alpha, valuation_of_i / valuation_of_j)
                else:
                    # assumes non-negative valuations
                    alpha = min(alpha, agent_i_alpha)
                
    return round(alpha, 3)