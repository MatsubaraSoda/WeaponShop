import os

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from dotenv import load_dotenv

load_dotenv()


def _thinking_llm_model() -> str:
    """与 Visual Forge 一致：OPENAI 兼容中转需使用 openai/<模型名>，避免 MODEL=gemini-* 被当成原生 Google 提供方。"""
    raw = (os.getenv("MODEL") or os.getenv("OPENAI_MODEL_NAME") or "").strip()
    if not raw:
        raise ValueError("请在 .env 中设置 MODEL 或 OPENAI_MODEL_NAME")
    if raw.startswith("openai/"):
        return raw
    return f"openai/{raw}"


@CrewBase
class Project():
    """GSA crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    def get_thinking_llm(self) -> LLM:
        base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE")
        return LLM(
            model=_thinking_llm_model(),
            base_url=base_url,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    @agent
    def schema_alignment_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['schema_alignment_strategist'],  # type: ignore[index]
            verbose=True,
            llm=self.get_thinking_llm(),
        )

    @task
    def schema_alignment_blueprint_task(self) -> Task:
        return Task(
            config=self.tasks_config['schema_alignment_blueprint_task'],  # type: ignore[index]
        )

    @agent
    def merchandising_copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config['merchandising_copywriter'],  # type: ignore[index]
            verbose=True,
            llm=self.get_thinking_llm(),
        )

    @task
    def merchandising_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['merchandising_generation_task'],  # type: ignore[index]
            context=[self.schema_alignment_blueprint_task()],
        )

    @agent
    def compliance_gate_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['compliance_gate_auditor'],  # type: ignore[index]
            verbose=True,
            llm=self.get_thinking_llm(),
        )

    @task
    def compliance_gate_task(self) -> Task:
        return Task(
            config=self.tasks_config['compliance_gate_task'],  # type: ignore[index]
            context=[self.merchandising_generation_task()],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GSA crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
