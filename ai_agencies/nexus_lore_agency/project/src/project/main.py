#!/usr/bin/env python
import os
import sys
import warnings

from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from project.crew import Project

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(_PROJECT_ROOT / ".env")


def _multiverse_count_from_env() -> int:
    raw = os.getenv("NUMBER_OF_MULTIVERSES")
    if raw is None or str(raw).strip() == "":
        return 2
    try:
        return int(raw)
    except ValueError:
        return 2


def _default_inputs() -> dict:
    n = _multiverse_count_from_env()
    return {
        "number": n,
        "target_count": n,
        "current_year": str(datetime.now().year),
    }


def run():
    """
    Run the NLA pipeline: extract themes → per-theme universe drafts → compile report.md.
    """
    inputs = _default_inputs()

    try:
        Project().kickoff_nla_pipeline(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}") from e


def train():
    """
    Train the crew for a given number of iterations.
    Uses the decorator-defined sequential crew (single-pass create); not identical to run().
    """
    inputs = _default_inputs()
    try:
        Project().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs,
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}") from e


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Project().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}") from e


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = _default_inputs()

    try:
        Project().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs,
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}") from e


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

    n = trigger_payload.get("number", trigger_payload.get("target_count"))
    if n is None:
        n = _multiverse_count_from_env()
    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "number": n,
        "target_count": n,
        "current_year": str(datetime.now().year),
    }

    try:
        result = Project().kickoff_nla_pipeline(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}") from e
