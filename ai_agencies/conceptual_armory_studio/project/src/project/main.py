#!/usr/bin/env python
import sys
import warnings
from pathlib import Path

from datetime import datetime

from project.crew import Project

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def load_world_lore() -> str:
    # 基于当前项目目录定位，不依赖宿主机上的 ai_agencies 路径
    lore_path = Path(__file__).resolve().parents[2] / "knowledge" / "report.md"
    if not lore_path.exists():
        raise FileNotFoundError(
            f"World lore file not found: {lore_path}. "
            "Please provide project/knowledge/report.md."
        )
    return lore_path.read_text(encoding="utf-8").strip()

def run():
    """
    Run the crew.
    """
    inputs = {
        'world_lore': load_world_lore(),
        'current_year': str(datetime.now().year)
    }

    try:
        Project().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "world_lore": load_world_lore(),
        'current_year': str(datetime.now().year)
    }
    try:
        Project().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

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
    inputs = {
        "world_lore": load_world_lore(),
        "current_year": str(datetime.now().year)
    }

    try:
        Project().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

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

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "world_lore": trigger_payload.get("world_lore", load_world_lore()),
        "current_year": str(datetime.now().year)
    }

    try:
        result = Project().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
