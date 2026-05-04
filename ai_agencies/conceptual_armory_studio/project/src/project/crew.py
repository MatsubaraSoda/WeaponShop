from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class Project:
    """CAS：双代理简化流水线（创作 -> 契约收敛/汇编）。"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def universe_armory_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["universe_armory_creator"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def armory_contract_editor(self) -> Agent:
        return Agent(
            config=self.agents_config["armory_contract_editor"],  # type: ignore[index]
            verbose=True,
        )

    @task
    def create_multiverse_armory_draft_task(self) -> Task:
        return Task(
            config=self.tasks_config["create_multiverse_armory_draft_task"],  # type: ignore[index]
        )

    @task
    def normalize_and_compile_armory_task(self) -> Task:
        return Task(
            config=self.tasks_config["normalize_and_compile_armory_task"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
