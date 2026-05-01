#!/usr/bin/env python
import json
import sys
import warnings
from datetime import datetime
from pathlib import Path

from project.crew import Project

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def _ensure_output_dir() -> None:
    """与 tasks.yaml 中 output_file: output/report.md 一致，工作目录为 project 根时保证目录存在。"""
    (Path(__file__).resolve().parents[2] / "output").mkdir(parents=True, exist_ok=True)


def load_weapon_data() -> str:
    """CAS 武器客观描述与参数，供 basic_merchandising_task 中的 {weapon_data} 插值。"""
    data_path = Path(__file__).resolve().parents[2] / "knowledge" / "report.md"
    if not data_path.exists():
        raise FileNotFoundError(
            f"Weapon data file not found: {data_path}. "
            "Please provide project/knowledge/report.md."
        )
    return data_path.read_text(encoding="utf-8").strip()


def run():
    """Run the crew."""
    _ensure_output_dir()
    inputs = {
        "weapon_data": load_weapon_data(),
        "current_year": str(datetime.now().year),
    }

    try:
        Project().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """Train the crew for a given number of iterations."""
    _ensure_output_dir()
    inputs = {
        "weapon_data": load_weapon_data(),
        "current_year": str(datetime.now().year),
    }
    try:
        Project().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs,
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """Replay the crew execution from a specific task."""
    try:
        Project().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """Test the crew execution and returns the results."""
    _ensure_output_dir()
    inputs = {
        "weapon_data": load_weapon_data(),
        "current_year": str(datetime.now().year),
    }

    try:
        Project().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs,
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    """Run the crew with trigger payload."""
    if len(sys.argv) < 2:
        raise Exception(
            "No trigger payload provided. Please provide JSON payload as argument."
        )

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "weapon_data": trigger_payload.get("weapon_data") or load_weapon_data(),
        "current_year": str(datetime.now().year),
    }

    try:
        _ensure_output_dir()
        result = Project().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(
            f"An error occurred while running the crew with trigger: {e}"
        )
