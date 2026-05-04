#!/usr/bin/env python
import sys
import time
import warnings
from pathlib import Path

from datetime import datetime

from dotenv import load_dotenv

from project.crew import Project

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(_PROJECT_ROOT / ".env")


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def load_world_lore() -> str:
    """
    NLA 交付的多元宇宙设定稿（由开发者手动复制到 knowledge/report.md）。
    与 Crew 级 Knowledge 中的 report.md 同源，并在 kickoff inputs 中作为 world_lore 注入任务上下文。
    """
    lore_path = Path(__file__).resolve().parents[2] / "knowledge" / "report.md"
    if not lore_path.exists():
        raise FileNotFoundError(
            f"World lore file not found: {lore_path}. "
            "Please provide project/knowledge/report.md (e.g. copy from NLA output)."
        )
    return lore_path.read_text(encoding="utf-8").strip()

def load_cas_weapons_bible_text() -> str:
    p = Path(__file__).resolve().parents[2] / "knowledge" / "CAS_Weapons_Bible.md"
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8").strip()


def _cas_weapons_bible_input_value() -> str:
    """
    供第二阶段“契约整理”任务使用的 Bible 正文。
    """
    text = load_cas_weapons_bible_text()
    if not text:
        raise FileNotFoundError("未找到 knowledge/CAS_Weapons_Bible.md")
    return text


def _base_kickoff_inputs() -> dict:
    return {
        "world_lore": load_world_lore(),
        "current_year": str(datetime.now().year),
        "cas_weapons_bible": _cas_weapons_bible_input_value(),
    }


def _is_retryable_llm_error(err: Exception) -> bool:
    msg = str(err).lower()
    retry_markers = [
        "failed to connect to openai api",
        "connection error",
        "request timed out",
        "timeout",
    ]
    return any(marker in msg for marker in retry_markers)


def _kickoff_with_retry(inputs: dict, max_attempts: int = 3, base_delay_sec: float = 2.0):
    last_err: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return Project().crew().kickoff(inputs=inputs)
        except Exception as e:
            last_err = e
            if (not _is_retryable_llm_error(e)) or attempt >= max_attempts:
                raise
            sleep_s = base_delay_sec * (2 ** (attempt - 1))
            time.sleep(sleep_s)
    if last_err is not None:
        raise last_err
    raise RuntimeError("Unknown kickoff retry state")


def run():
    """
    Run the crew.
    """
    try:
        _kickoff_with_retry(_base_kickoff_inputs())
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        Project().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=_base_kickoff_inputs(),
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Project().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    try:
        Project().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=_base_kickoff_inputs(),
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = _base_kickoff_inputs()
    inputs["crewai_trigger_payload"] = trigger_payload
    inputs["world_lore"] = trigger_payload.get("world_lore", inputs["world_lore"])

    try:
        result = _kickoff_with_retry(inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
