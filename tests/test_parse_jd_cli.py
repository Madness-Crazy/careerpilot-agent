import json
import subprocess
import sys


def test_parse_jd_cli_generates_json_file(tmp_path) -> None:
    jd_file = tmp_path / "sample_jd.txt"
    jd_file.write_text(
        "AI Agent Engineer\n要求熟悉 Python、FastAPI、RAG、Function Calling、LangGraph。\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "scripts/parse_jd.py", str(jd_file)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd="D:\\pycharm\\PythonProject\\careerpilot-agent",
        check=False,
    )

    output_file = jd_file.with_suffix(".json")

    assert result.returncode == 0
    assert output_file.exists()

    parsed_output = json.loads(output_file.read_text(encoding="utf-8"))
    assert parsed_output["role"] == "AI Agent Engineer"
    assert parsed_output["engineering_skills"] == ["Python", "FastAPI"]
    assert parsed_output["agent_skills"] == ["Function Calling", "LangGraph"]
    assert parsed_output["rag_skills"] == ["RAG"]
