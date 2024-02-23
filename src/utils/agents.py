from utils.agent import Agent


class Agents:
    def __init__(self, agents_list: list[Agent]):
        self.agents: dict[int, Agent] = {}
        self.initialize_agents(agents_list)

    def __iter__(self):
        return list(self.get_agents()).__iter__()

    def initialize_agents(self, agents_list: list[Agent]) -> None:
        for agent in agents_list:
            self.agents[agent.get_index()] = agent

    def add_agent(self, index: int, agent: Agent) -> None:
        self.agents[index] = agent

    def get_agent(self, index: int) -> Agent:
        if index in self.agents:
            return self.agents[index]
        else:
            raise Exception(f"{self.agents} does not contain agent with index {index}")
        
    def delete_agent(self, index_or_agent: int | Agent) -> None:
        if isinstance(index_or_agent, int):
            self.agents.pop(index_or_agent)
        elif isinstance(index_or_agent, Agent):
            self.agents.pop(index_or_agent.get_index())
        else:
            raise Exception(f"To delete an agent from agents, index or Agent object was expected, got {index_or_agent}")

    def get_agents(self) -> list[Agent]:
        return list(self.agents.values())
    
    def get_indices(self) -> list[int]:
        return list(self.agents.keys())
    
    def size(self) -> int:
        return len(self.agents)