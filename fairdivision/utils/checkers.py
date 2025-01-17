from typing import Literal

from fairdivision.algorithms.all_allocations import all_allocations

from fairdivision.utils.agent import Agent
from fairdivision.utils.agents import Agents
from fairdivision.utils.allocation import Allocation
from fairdivision.utils.helpers import get_maximin_shares
from fairdivision.utils.items import Items


def is_ef(agents: Agents, allocation: Allocation) -> Literal[True] | tuple[Literal[False], tuple[Agent, Agent]]:
    """
    Checks if the given `allocation` to `agents` is envy-free.

    Returns `True` if it is EF or tuple `(False, (evious_agent, envied_agent))` otherwise.
    """

    possibly_envied_agents = agents.copy()
    for agent in agents:
        if allocation.for_agent(agent).size() == 0:
            possibly_envied_agents.remove_agent(agent)
     
    for agent_i in agents:
        for agent_j in possibly_envied_agents:
            if agent_i != agent_j:
                if agent_i.envies(agent_j, allocation):
                    return (False, (agent_i, agent_j))
                
    return True

def is_efx0(agents: Agents, allocation: Allocation) -> Literal[True] | tuple[Literal[False], tuple[Agent, Agent]]:
    """
    Checks if the given `allocation` to `agents` is envy-free up to any good.

    Returns `True` if it is EFX0 or tuple `(False, (evious_agent, envied_agent))` otherwise.
    """

    possibly_envied_agents = agents.copy()
    for agent in agents:
        if allocation.for_agent(agent).size() == 0:
            possibly_envied_agents.remove_agent(agent)

    for agent_i in agents:
        for agent_j in possibly_envied_agents:
            if agent_i != agent_j:
                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                for item_to_remove in allocation.for_agent(agent_j):
                    items_subset = allocation.for_agent(agent_j).copy()
                    items_subset.remove_item(item_to_remove)

                    valuation_of_j = agent_i.get_valuation(items_subset)

                    if valuation_of_j > valuation_of_i:
                        return (False, (agent_i, agent_j))
                
    return True


def highest_efx0_approximation(agents: Agents, allocation: Allocation) -> float:
    """
    Checks what is the highest `a` such that `allocation` is a-EFX0.  

    The result is rounded to 3 decimal places. If `allocation` is EFX0, returns `1`.
    """

    alpha = 1.0

    possibly_envied_agents = agents.copy()
    for agent in agents:
        if allocation.for_agent(agent).size() == 0:
            possibly_envied_agents.remove_agent(agent)

    for agent_i in agents:
        for agent_j in possibly_envied_agents:
            if agent_i != agent_j:
                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                for item_to_remove in allocation.for_agent(agent_j):
                    items_subset = allocation.for_agent(agent_j).copy()
                    items_subset.remove_item(item_to_remove)

                    valuation_of_j = agent_i.get_valuation(items_subset)

                    if valuation_of_j > valuation_of_i:
                        # assumes non-negative valuations
                        alpha = min(alpha, valuation_of_i / valuation_of_j)
                
    return round(alpha, 3)


def efx0_satisfied_fraction(agents: Agents, allocation: Allocation) -> float:
    """
    Returns a fraction of `agents` that are not envious up to any good.

    Returns 1 if `allocation` is EFX0. 
    """

    possibly_envied_agents = agents.copy()
    for agent in agents:
        if allocation.for_agent(agent).size() == 0:
            possibly_envied_agents.remove_agent(agent)

    efx_satisfied_agents_number = 0

    for agent_i in agents:
        is_efx_satisfied = True
        for agent_j in possibly_envied_agents:
            if not is_efx_satisfied:
                break

            if agent_i != agent_j:
                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                for item_to_remove in allocation.for_agent(agent_j):
                    items_subset = allocation.for_agent(agent_j).copy()
                    items_subset.remove_item(item_to_remove)

                    valuation_of_j = agent_i.get_valuation(items_subset)

                    if valuation_of_j > valuation_of_i:
                        is_efx_satisfied = False
                        break
        
        if is_efx_satisfied:
            efx_satisfied_agents_number += 1

    return round(efx_satisfied_agents_number / agents.size(), 3)



def is_efx(agents: Agents, allocation: Allocation) -> Literal[True] | tuple[Literal[False], tuple[Agent, Agent]]:
    """
    Checks if the given `allocation` to `agents` is envy-free up to any positively valued good.

    Returns `True` if it is EFX or tuple `(False, (evious_agent, envied_agent))` otherwise.
    """

    possibly_envied_agents = agents.copy()
    for agent in agents:
        if allocation.for_agent(agent).size() == 0:
            possibly_envied_agents.remove_agent(agent)

    for agent_i in agents:
        for agent_j in possibly_envied_agents:
            if agent_i != agent_j:
                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                for item_to_remove in allocation.for_agent(agent_j):
                    if agent_i.get_valuation(item_to_remove) > 0:
                        items_subset = allocation.for_agent(agent_j).copy()
                        items_subset.remove_item(item_to_remove)

                        valuation_of_j = agent_i.get_valuation(items_subset)

                        if valuation_of_j > valuation_of_i:
                            return (False, (agent_i, agent_j))
                
    return True


def highest_efx_approximation(agents: Agents, allocation: Allocation) -> float:
    """
    Checks what is the highest `a` such that `allocation` is a-EFX.  

    The result is rounded to 3 decimal places. If `allocation` is EFX, returns `1`.
    """

    alpha = 1.0

    possibly_envied_agents = agents.copy()
    for agent in agents:
        if allocation.for_agent(agent).size() == 0:
            possibly_envied_agents.remove_agent(agent)

    for agent_i in agents:
        for agent_j in possibly_envied_agents:
            if agent_i != agent_j:
                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                for item_to_remove in allocation.for_agent(agent_j):
                    if agent_i.get_valuation(item_to_remove) > 0:
                        items_subset = allocation.for_agent(agent_j).copy()
                        items_subset.remove_item(item_to_remove)

                        valuation_of_j = agent_i.get_valuation(items_subset)

                        if valuation_of_j > valuation_of_i:
                            # assumes non-negative valuations
                            alpha = min(alpha, valuation_of_i / valuation_of_j)
                
    return round(alpha, 3)


def efx_satisfied_fraction(agents: Agents, allocation: Allocation) -> float:
    """
    Returns a fraction of `agents` that are not envious up to any positively valued good.

    Returns 1 if `allocation` is EFX. 
    """

    possibly_envied_agents = agents.copy()
    for agent in agents:
        if allocation.for_agent(agent).size() == 0:
            possibly_envied_agents.remove_agent(agent)

    efx_satisfied_agents_number = 0

    for agent_i in agents:
        is_efx_satisfied = True
        for agent_j in possibly_envied_agents:
            if not is_efx_satisfied:
                break

            if agent_i != agent_j:
                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                for item_to_remove in allocation.for_agent(agent_j):
                    if agent_i.get_valuation(item_to_remove) > 0:
                        items_subset = allocation.for_agent(agent_j).copy()
                        items_subset.remove_item(item_to_remove)

                        valuation_of_j = agent_i.get_valuation(items_subset)

                        if valuation_of_j > valuation_of_i:
                            is_efx_satisfied = False
                            break
        
        if is_efx_satisfied:
            efx_satisfied_agents_number += 1

    return round(efx_satisfied_agents_number / agents.size(), 3)


def is_ef2(agents: Agents, allocation: Allocation) -> Literal[True] | tuple[Literal[False], tuple[Agent, Agent]]:
    """
    Checks if the given `allocation` to `agents` is envy-free up to two goods.

    Returns `True` if it is EF2 or tuple `(False, (evious_agent, envied_agent))` otherwise.
    """

    possibly_envied_agents = agents.copy()
    for agent in agents:
        if allocation.for_agent(agent).size() == 0:
            possibly_envied_agents.remove_agent(agent)

    for agent_i in agents:
        for agent_j in possibly_envied_agents:
            if agent_i != agent_j:
                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                items_to_check = min(2, allocation.for_agent(agent_j).size())

                for item_to_remove in allocation.for_agent(agent_j):
                    items_subset = allocation.for_agent(agent_j).copy()
                    items_subset.remove_item(item_to_remove)

                    valuation_of_j = agent_i.get_valuation(items_subset)

                    if valuation_of_i >= valuation_of_j:
                        items_to_check -= 1
                        if items_to_check == 0:
                            break
                else:
                    return (False, (agent_i, agent_j)) 
                
    return True


def is_ef1(agents: Agents, allocation: Allocation) -> Literal[True] | tuple[Literal[False], tuple[Agent, Agent]]:
    """
    Checks if the given `allocation` to `agents` is envy-free up to one good.

    Returns `True` if it is EF1 or tuple `(False, (evious_agent, envied_agent))` otherwise.
    """

    possibly_envied_agents = agents.copy()
    for agent in agents:
        if allocation.for_agent(agent).size() == 0:
            possibly_envied_agents.remove_agent(agent)

    for agent_i in agents:
        for agent_j in possibly_envied_agents:
            if agent_i != agent_j:
                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                for item_to_remove in allocation.for_agent(agent_j):
                    items_subset = allocation.for_agent(agent_j).copy()
                    items_subset.remove_item(item_to_remove)

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

    alpha = 1.0

    possibly_envied_agents = agents.copy()
    for agent in agents:
        if allocation.for_agent(agent).size() == 0:
            possibly_envied_agents.remove_agent(agent)

    for agent_i in agents:
        for agent_j in possibly_envied_agents:
            if agent_i != agent_j:
                agent_i_alpha = 0.0

                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                for item_to_remove in allocation.for_agent(agent_j):
                    items_subset = allocation.for_agent(agent_j).copy()
                    items_subset.remove_item(item_to_remove)

                    valuation_of_j = agent_i.get_valuation(items_subset)

                    if valuation_of_i >= valuation_of_j:
                        break
                    else:
                        agent_i_alpha = max(agent_i_alpha, valuation_of_i / valuation_of_j)
                else:
                    # assumes non-negative valuations
                    alpha = min(alpha, agent_i_alpha)
                
    return round(alpha, 3)


def ef1_satisfied_fraction(agents: Agents, allocation: Allocation) -> float:
    """
    Returns a fraction of `agents` that are not envious up to one good.

    Returns 1 if `allocation` is EF1. 
    """

    possibly_envied_agents = agents.copy()
    for agent in agents:
        if allocation.for_agent(agent).size() == 0:
            possibly_envied_agents.remove_agent(agent)

    ef1_satisfied_agents_number = 0

    for agent_i in agents:
        is_ef1_satisfied = True
        for agent_j in possibly_envied_agents:
            if not is_ef1_satisfied:
                break

            if agent_i != agent_j:
                valuation_of_i = agent_i.get_valuation(allocation.for_agent(agent_i))

                for item_to_remove in allocation.for_agent(agent_j):
                    items_subset = allocation.for_agent(agent_j).copy()
                    items_subset.remove_item(item_to_remove)

                    valuation_of_j = agent_i.get_valuation(items_subset)

                    if valuation_of_i >= valuation_of_j:
                        break
                else:
                    is_ef1_satisfied = False

        if is_ef1_satisfied:
            ef1_satisfied_agents_number += 1

    return round(ef1_satisfied_agents_number / agents.size(), 3)


def is_mms(agents: Agents, items: Items, allocation: Allocation) -> Literal[True] | tuple[Literal[False], Agent]:
    """
    Checks if the given `allocation` of `items` to `agents` is maximin share fair.

    Returns `True` if it is MMS or tuple `(False, not_satisfied_agent)` otherwise.
    """

    maximin_shares = get_maximin_shares(agents, items)

    for agent, _ in allocation.get_allocation():
        if agent.get_valuation(allocation.for_agent(agent)) < maximin_shares[agent]:
            return (False, agent)
    
    return True


def highest_mms_approximation(agents: Agents, items: Items, allocation: Allocation) -> float:
    """
    Checks what is the highest `a` such that `allocation` is a-MMS.  

    The result is rounded to 3 decimal places. If `allocation` is MMS, returns `1`.
    """

    maximin_shares = get_maximin_shares(agents, items)

    alpha = 1.0

    for agent, _ in allocation.get_allocation():
        valuation = agent.get_valuation(allocation.for_agent(agent))

        if valuation < maximin_shares[agent]:
            # assumes non-negative valuations
            alpha = min(alpha, valuation / maximin_shares[agent])

    return round(alpha, 3)


def is_eefx(agents: Agents, items: Items, allocation: Allocation) -> Literal[True] | tuple[Literal[False], Agent]:
    """
    Checks if the given `allocation` of `items` to `agents` is epistemic envy-free up to any positively valued good.

    Returns `True` if it is EEFX or tuple `(False, not_satisfied_agent)` otherwise.
    """

    # check if EFX certificate can be found for each agent
    for agent in agents:
        other_agents = agents.copy()
        other_agents.remove_agent(agent)
        
        other_items = items.copy()
        for item in allocation.for_agent(agent):
            other_items.remove_item(item)

        self_valuation = agent.get_valuation(allocation.for_agent(agent))

        # iterating over all allocations of the rest of the items
        for possible_efx_certificate in all_allocations(other_agents, other_items):
            is_efx_satisfying = True

            # checking if `agent` is EFX satisfied with `possible_efx_certificate`
            for other_agent in other_agents:
                for item_to_remove in possible_efx_certificate.for_agent(other_agent):
                    if agent.get_valuation(item_to_remove) > 0:
                        items_subset = possible_efx_certificate.for_agent(other_agent).copy()
                        items_subset.remove_item(item_to_remove)

                        other_valuation = agent.get_valuation(items_subset)

                        if other_valuation > self_valuation:
                            is_efx_satisfying = False
                            break
            
                if not is_efx_satisfying:
                    break
        
            if is_efx_satisfying:
                break
        # no break occurred, so no certificate found
        else:
            return (False, agent)
        
    return True


def is_prop(agents: Agents, items: Items, allocation: Allocation) -> Literal[True] | tuple[Literal[False], Agent]:
    """
    Checks if the given `allocation` of `items` to `agents` is proportional.

    Returns `True` if it is PROP or tuple `(False, not_satisfied_agent)` otherwise.
    """

    n = agents.size()

    for agent in agents:
        valuation_of_agent = agent.get_valuation(allocation.for_agent(agent))
        valuation_of_all_items = agent.get_valuation(items)

        if valuation_of_agent < valuation_of_all_items / n:
            return (False, agent)
        
    return True


def highest_prop_approximation(agents: Agents, items: Items, allocation: Allocation) -> float:
    """
    Checks what is the highest `a` such that `allocation` is a-PROP.  

    The result is rounded to 3 decimal places. If `allocation` is PROP, returns `1`.
    """

    n = agents.size()

    alpha = 1.0

    for agent in agents:
        valuation_of_agent = agent.get_valuation(allocation.for_agent(agent))
        valuation_of_all_items = agent.get_valuation(items)

        if valuation_of_agent < valuation_of_all_items / n:
            alpha = min(alpha, valuation_of_agent / (valuation_of_all_items / n))

    return round(alpha, 3)


def prop_satisfied_fraction(agents: Agents, items: Items, allocation: Allocation) -> float:
    """
    Returns a fraction of `agents` that are satisfied according to proportionality.

    Returns 1 if `allocation` is PROP. 
    """

    n = agents.size()

    prop_satisfied_agents_number = 0

    for agent in agents:
        valuation_of_agent = agent.get_valuation(allocation.for_agent(agent))
        valuation_of_all_items = agent.get_valuation(items)

        if valuation_of_agent >= valuation_of_all_items / n:
            prop_satisfied_agents_number += 1

    return round(prop_satisfied_agents_number / agents.size(), 3)


def is_prop1(agents: Agents, items: Items, allocation: Allocation) -> Literal[True] | tuple[Literal[False], Agent]:
    """
    Checks if the given `allocation` of `items` to `agents` is proportional up to one good.

    Returns `True` if it is PROP1 or tuple `(False, not_satisfied_agent)` otherwise.
    """

    n = agents.size()

    for agent in agents:
        other_items = items.copy()

        for item in allocation.for_agent(agent):
            other_items.remove_item(item)

        favorite_from_other = agent.get_favorite_item(other_items)

        extended_bundle = allocation.for_agent(agent)
        extended_bundle.add_item(favorite_from_other)
        
        valuation_of_extended_bundle = agent.get_valuation(extended_bundle)

        valuation_of_all_items = agent.get_valuation(items)

        if valuation_of_extended_bundle < valuation_of_all_items / n:
            return (False, agent)
        
    return True
