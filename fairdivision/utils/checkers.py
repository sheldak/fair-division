from typing import Literal

from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation


def is_ef(agents: Agents, allocation: Allocation) -> Literal[True] | tuple[Literal[False], tuple[Agent, Agent]]:
    """
    Checks if the given `allocation` to `agents` is envy-free.

    Returns `True` if it is EF or tuple `(False, (evious_agent, envied_agent))` otherwise.
    """
     
    for agent_i in agents:
        for agent_j in agents:
            if agent_i != agent_j:
                if agent_i.envies(agent_j, allocation):
                    return (False, (agent_i, agent_j))
                
    return True


def is_efx(agents: Agents, allocation: Allocation) -> Literal[True] | tuple[Literal[False], tuple[Agent, Agent]]:
    """
    Checks if the given `allocation` to `agents` is envy-free up to any good.

    Returns `True` if it is EFX or tuple `(False, (evious_agent, envied_agent))` otherwise.
    """

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
    """
    Checks what is the highest `a` such that `allocation` is a-EFX.  

    The result is rounded to 3 decimal places. If `allocation` is EFX, returns `1`.
    """

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
    """
    Checks if the given `allocation` to `agents` is envy-free up to one good.

    Returns `True` if it is EF1 or tuple `(False, (evious_agent, envied_agent))` otherwise.
    """

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
    """
    Checks what is the highest `a` such that `allocation` is a-EF1.  

    The result is rounded to 3 decimal places. If `allocation` is EF1, returns `1`.
    """

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
