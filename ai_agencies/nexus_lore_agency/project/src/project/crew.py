from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

_TASKS_YAML_PATH = Path(__file__).resolve().parent / "config" / "tasks.yaml"
_tasks_yaml_cache: dict[str, Any] | None = None


def _get_tasks_yaml_root() -> dict[str, Any]:
    """从磁盘读取 tasks.yaml；勿使用可能被 CrewAI 运行时改写过的 self.tasks_config。"""
    global _tasks_yaml_cache
    if _tasks_yaml_cache is None:
        with _TASKS_YAML_PATH.open(encoding="utf-8") as f:
            loaded = yaml.safe_load(f)
        if not isinstance(loaded, dict):
            raise TypeError("tasks.yaml must parse to a mapping")
        _tasks_yaml_cache = loaded
    return _tasks_yaml_cache


def _clone_pipeline_task_config(task_key: str) -> dict[str, Any]:
    """
    克隆任务配置供流水线动态改写 description。
    使用 JSON 往返复制纯数据，避免 copy.deepcopy 触碰 CrewAI/Pydantic 注入的不可 pickle 对象。
    """
    cfg = json.loads(json.dumps(_get_tasks_yaml_root()[task_key]))
    cfg.pop("agent", None)
    return cfg


def _split_extract_into_theme_seeds(raw: str, expected: int) -> list[str]:
    """将主题提取任务的输出拆成 expected 份种子，供 universe_architect 逐次扩写。"""
    text = raw.strip()
    if expected <= 0:
        return []
    if not text:
        return [""] * expected

    numbered = re.split(r"\n(?=\d+\.\s)", text)
    numbered = [p.strip() for p in numbered if p.strip()]
    if len(numbered) >= expected:
        return numbered[:expected]

    hashed = re.split(r"\n(?=#{2,3}\s)", text)
    hashed = [p.strip() for p in hashed if p.strip()]
    if len(hashed) >= expected:
        return hashed[:expected]

    hrs = re.split(r"\n(?:-{3,}|\*{3,})\s*\n", text)
    hrs = [p.strip() for p in hrs if p.strip()]
    if len(hrs) >= expected:
        return hrs[:expected]

    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    if len(paras) >= expected:
        size = max(1, len(paras) // expected)
        out: list[str] = []
        for i in range(expected):
            start = i * size
            end = (i + 1) * size if i < expected - 1 else len(paras)
            out.append("\n\n".join(paras[start:end]))
        return out

    chunk = max(1, len(text) // expected)
    return [text[i : i + chunk] for i in range(0, len(text), chunk)][:expected]


@CrewBase
class Project:
    """Nexus Lore Agency crew：提取主题 → 逐宇宙扩写 → 汇编 report.md。"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def ip_scavenger(self) -> Agent:
        return Agent(
            config=self.agents_config["ip_scavenger"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def universe_architect(self) -> Agent:
        return Agent(
            config=self.agents_config["universe_architect"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def lore_compiler(self) -> Agent:
        return Agent(
            config=self.agents_config["lore_compiler"],  # type: ignore[index]
            verbose=True,
        )

    @task
    def extract_themes_task(self) -> Task:
        return Task(
            config=self.tasks_config["extract_themes_task"],  # type: ignore[index]
        )

    @task
    def create_universe_task(self) -> Task:
        return Task(
            config=self.tasks_config["create_universe_task"],  # type: ignore[index]
        )

    @task
    def compile_chronicle_task(self) -> Task:
        return Task(
            config=self.tasks_config["compile_chronicle_task"],  # type: ignore[index]
        )

    def kickoff_nla_pipeline(self, inputs: dict[str, Any] | None = None) -> Any:
        """
        NLA 正式流水线（与 tasks.yaml 注释一致）：
        1) extract_themes_task
        2) create_universe_task × number（每次注入一份主题种子）
        3) compile_chronicle_task（汇编为 report.md）

        inputs 须包含「number」（宇宙数量）；可与「target_count」同义传入，二者会在下游合并。
        """
        inputs = dict(inputs or {})
        number = inputs.get("number", inputs.get("target_count", 5))
        try:
            number = int(number)
        except (TypeError, ValueError):
            number = 5
        inputs["number"] = number
        inputs.setdefault("target_count", number)

        c_extract = Crew(
            agents=[self.ip_scavenger()],
            tasks=[self.extract_themes_task()],
            process=Process.sequential,
            verbose=True,
        )
        extract_out = c_extract.kickoff(inputs=inputs)
        extract_raw = (
            extract_out.raw if getattr(extract_out, "raw", None) is not None else str(extract_out)
        )

        seeds = _split_extract_into_theme_seeds(extract_raw, number)
        drafts: list[str] = []

        for i, seed in enumerate(seeds):
            merged_create = _clone_pipeline_task_config("create_universe_task")
            merged_create["description"] = (
                merged_create.get("description", "")
                + f"\n\n### 本轮注入的主题种子（第 {i + 1} / {number} 份）\n{seed}"
            )
            t_create = Task(
                config=merged_create,
                agent=self.universe_architect(),
            )
            c_create = Crew(
                agents=[self.universe_architect()],
                tasks=[t_create],
                process=Process.sequential,
                verbose=True,
            )
            loop_inputs = {
                **inputs,
                "theme_index": i + 1,
                "single_theme_seed": seed,
            }
            out_u = c_create.kickoff(inputs=loop_inputs)
            drafts.append(out_u.raw if getattr(out_u, "raw", None) is not None else str(out_u))

        merged_compile = _clone_pipeline_task_config("compile_chronicle_task")
        merged_compile["description"] = (
            merged_compile.get("description", "")
            + "\n\n### 待汇编的各宇宙稿件（按提取顺序）\n"
            + "\n\n---\n\n".join(drafts)
        )
        t_compile = Task(
            config=merged_compile,
            agent=self.lore_compiler(),
        )
        c_compile = Crew(
            agents=[self.lore_compiler()],
            tasks=[t_compile],
            process=Process.sequential,
            verbose=True,
        )
        return c_compile.kickoff(inputs=inputs)

    @crew
    def crew(self) -> Crew:
        """
        顺序执行 extract → create → compile 各一次（create 自动承接 extract 的上下文）。
        若需「每主题单独一轮扩写」，请使用 main.run() 调用的 kickoff_nla_pipeline。
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
