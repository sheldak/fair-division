from __future__ import annotations
from typing import Iterator

from fairdivision.utils.agent import Agent


class Agents:
    """
    A class representating a collection of agents.

    Contains agents in two structures:
      - a dictionary that has agent's index as a key, and the corresponding agent as value
      - a list of agents sorted in an ascending order of their indices
    """

    def __init__(self, agents_list: list[Agent]):
        self.agents: dict[int, Agent] = {}
        self.sorted_agents: list[Agent] = []
        self.__initialize_agents(agents_list)

    def __iter__(self) -> Iterator[Agent]:
        return self.get_agents().__iter__()
    
    def __repr__(self):
        return f"Agents({self.get_agents()})"
    
    def __str__(self):
        return repr(self)
    
    def __contains__(self, agent):
        return agent.get_index() in self.agents
    
    def copy(self) -> Agents:
        return Agents(self.get_agents().copy())

    def __initialize_agents(self, agents_list: list[Agent]) -> None:
        for agent in agents_list:
            self.agents[agent.get_index()] = agent

        self.sorted_agents = sorted(agents_list, key=lambda agent: agent.get_index())

    def add_agent(self, agent: Agent) -> None:
        self.agents[agent.get_index()] = agent
        self.sorted_agents = sorted(self.sorted_agents + [agent], key=lambda agent: agent.get_index())

    def get_agent(self, index: int) -> Agent:
        if index in self.agents:
            return self.agents[index]
        else:
            raise Exception(f"{self.agents} does not contain agent with index {index}")
        
    def remove_agent(self, index_or_agent: int | Agent) -> None:
        if isinstance(index_or_agent, int):
            self.agents.pop(index_or_agent)
            self.sorted_agents = list(filter(lambda agent: agent.get_index() != index_or_agent, self.sorted_agents))
        elif isinstance(index_or_agent, Agent):
            self.agents.pop(index_or_agent.get_index())
            self.sorted_agents.remove(index_or_agent)
        else:
            raise Exception(f"To delete an agent from agents, index or Agent object was expected, got {index_or_agent}")

    def get_agents(self) -> list[Agent]:
        return self.sorted_agents

    def get_indices(self) -> list[int]:
        return list(map(lambda item: item.get_index(), self.sorted_agents))
    
    def size(self) -> int:
        return len(self.agents)
