from typing import Literal

from utils.agent import Agent
from utils.agents import Agents
from utils.allocation import Allocation
from utils.bundle import Bundle


def is_ef(agents: Agents, allocation: Allocation) -> Literal[True] | tuple[Literal[False], tuple[Agent, Agent]]:
    for agent_1 in agents:
        for agent_2 in agents:
            if agent_1 != agent_2:
                valuation_of_1 = valuation_of_bundle(agent_1, allocation.for_agent(agent_1))
                valuation_of_2 = valuation_of_bundle(agent_1, allocation.for_agent(agent_2))

                if valuation_of_2 > valuation_of_1:
                    return (False, (agent_1, agent_2))
                
    return True


def is_efx(agents: Agents, allocation: Allocation) -> Literal[True] | tuple[Literal[False], tuple[Agent, Agent]]:
    for agent_1 in agents:
        for agent_2 in agents:
            if agent_1 != agent_2:
                valuation_of_1 = valuation_of_bundle(agent_1, allocation.for_agent(agent_1))

                for item_to_remove in allocation.for_agent(agent_2):
                    items_subset = allocation.for_agent(agent_2).copy()
                    items_subset.delete_item(item_to_remove)

                    valuation_of_2 = valuation_of_bundle(agent_1, items_subset)

                    if valuation_of_2 > valuation_of_1:
                        return (False, (agent_1, agent_2))
                
    return True


def is_ef1(agents: Agents, allocation: Allocation) -> Literal[True] | tuple[Literal[False], tuple[Agent, Agent]]:
    for agent_1 in agents:
        for agent_2 in agents:
            if agent_1 != agent_2:
                valuation_of_1 = valuation_of_bundle(agent_1, allocation.for_agent(agent_1))

                for item_to_remove in allocation.for_agent(agent_2):
                    items_subset = allocation.for_agent(agent_2).copy()
                    items_subset.delete_item(item_to_remove)

                    valuation_of_2 = valuation_of_bundle(agent_1, items_subset)

                    if valuation_of_1 >= valuation_of_2:
                        break
                else:
                    return (False, (agent_1, agent_2)) 
                
    return True


def valuation_of_bundle(agent: Agent, bundle: Bundle) -> int:
    valuation = 0
    for item in bundle:
        valuation += agent.get_valuation(item)

    return valuation