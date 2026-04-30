import os

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from dotenv import load_dotenv

# 导入画图工具
from project.tools.image_generation_tool import FlowImageGeneratorTool

load_dotenv()


def _thinking_llm_model() -> str:
    """从环境读取模型名；中转 OpenAI 兼容时一般用 openai/<裸模型名> 路由。"""
    raw = (os.getenv("MODEL") or os.getenv("OPENAI_MODEL_NAME") or "").strip()
    if not raw:
        raise ValueError("请在 .env 中设置 MODEL 或 OPENAI_MODEL_NAME")
    if raw.startswith("openai/"):
        return raw
    return f"openai/{raw}"

@CrewBase
class Project():
    """Visual Forge Studio crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    def get_thinking_llm(self) -> LLM:
        # 使用 OpenAI 兼容协议对接中转；地址与密钥来自 .env
        # 支持：OPENAI_BASE_URL 或 OPENAI_API_BASE、OPENAI_API_KEY、MODEL 或 OPENAI_MODEL_NAME
        base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE")
        return LLM(
            model=_thinking_llm_model(),
            base_url=base_url,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    @agent
    def image_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['image_generator'],  # type: ignore[index]
            verbose=True,
            # --- 核心改动 2：装备思考大脑 ---
            llm=self.get_thinking_llm(),
            # --- 核心改动 3：装备画图工具双手 ---
            tools=[FlowImageGeneratorTool()] 
        )

    @task
    def test_image_generation(self) -> Task:
        return Task(
            config=self.tasks_config['test_image_generation'],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Project crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )