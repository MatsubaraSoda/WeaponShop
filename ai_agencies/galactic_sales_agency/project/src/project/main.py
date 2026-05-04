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


def _load_knowledge_file(filename: str, hint: str) -> str:
    """读取 GSA 闭环知识文件。"""
    data_path = Path(__file__).resolve().parents[2] / "knowledge" / filename
    if not data_path.exists():
        raise FileNotFoundError(
            f"Knowledge file not found: {data_path}. {hint}"
        )
    return data_path.read_text(encoding="utf-8").strip()


def load_cas_report() -> str:
    """CAS 武器客观输入。"""
    return _load_knowledge_file(
        "report.cas.md",
        "Please provide project/knowledge/report.cas.md.",
    )


def load_nla_report() -> str:
    """NLA 宇宙语境输入。"""
    return _load_knowledge_file(
        "report.nla.md",
        "Please provide project/knowledge/report.nla.md.",
    )


def load_gsa_bible() -> str:
    """GSA 内部最高规范输入。"""
    return _load_knowledge_file(
        "GSA_Weapons_Bible.md",
        "Please provide project/knowledge/GSA_Weapons_Bible.md.",
    )


def _build_inputs() -> dict[str, str]:
    """统一构造 crew 输入，匹配 tasks.yaml 占位符。"""
    return {
        "cas_report": load_cas_report(),
        "nla_report": load_nla_report(),
        "gsa_bible": load_gsa_bible(),
        "current_year": str(datetime.now().year),
    }


def run():
    """Run the crew."""
    _ensure_output_dir()
    inputs = _build_inputs()

    try:
        Project().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """Train the crew for a given number of iterations."""
    _ensure_output_dir()
    inputs = _build_inputs()
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
    inputs = _build_inputs()

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

    base_inputs = _build_inputs()
    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "cas_report": (
            trigger_payload.get("cas_report")
            or trigger_payload.get("weapon_data")
            or base_inputs["cas_report"]
        ),
        "nla_report": trigger_payload.get("nla_report") or base_inputs["nla_report"],
        "gsa_bible": trigger_payload.get("gsa_bible") or base_inputs["gsa_bible"],
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
