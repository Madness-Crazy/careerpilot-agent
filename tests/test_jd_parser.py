from app.services.jd_parser import extract_role, extract_skill_report, find_matched_keywords


def test_find_matched_keywords_is_case_insensitive() -> None:
    jd_text = "We need Python, fastapi, docker and langgraph."

    matched = find_matched_keywords(jd_text, ["Python", "FastAPI", "Docker", "LangGraph"])

    assert matched == ["Python", "FastAPI", "Docker", "LangGraph"]


def test_extract_role_prefers_known_role_keyword() -> None:
    jd_text = "招聘 AI Agent Engineer，要求熟悉 Python、RAG 和 Function Calling。"

    role = extract_role(jd_text)

    assert role == "AI Agent Engineer"


def test_extract_role_falls_back_to_first_line() -> None:
    jd_text = "智能求职助手开发岗位\n负责 Python 服务开发与 RAG 能力建设。"

    role = extract_role(jd_text)

    assert role == "智能求职助手开发岗位"


def test_extract_skill_report_returns_structured_categories_for_english_jd() -> None:
    jd_text = """
    AI Agent Engineer
    Responsibilities:
    - Build Python and FastAPI services.
    - Design RAG pipelines with Chroma and Embedding workflow.
    - Use OpenAI with JSON Schema outputs.
    - Build Function Calling and LangGraph agent workflows.
    - Track Logging, Cost, Latency and Eval metrics.
    - Bonus: MCP
    """

    report = extract_skill_report(jd_text)

    assert report.role == "AI Agent Engineer"
    assert report.engineering_skills == ["Python", "FastAPI"]
    assert report.llm_skills == ["OpenAI", "JSON Schema"]
    assert report.agent_skills == ["Function Calling", "Workflow", "LangGraph"]
    assert report.rag_skills == ["RAG", "Embedding", "Chroma"]
    assert report.production_skills == ["Eval", "Logging", "Cost", "Latency"]
    assert report.bonus_skills == ["MCP"]
    assert "MCP" not in report.required_skills


def test_extract_skill_report_supports_chinese_jd() -> None:
    jd_text = """
    招聘 AI Agent 工程师
    要求熟悉 Python、FastAPI、RAG、Function Calling、LangGraph。
    有多模态和本地模型部署经验优先。
    """

    report = extract_skill_report(jd_text)

    assert report.role == "AI Agent 工程师"
    assert report.engineering_skills == ["Python", "FastAPI"]
    assert report.agent_skills == ["Function Calling", "LangGraph"]
    assert report.rag_skills == ["RAG"]
    assert report.bonus_skills == ["多模态", "本地模型部署"]


def test_extract_skill_report_returns_empty_lists_when_no_skills_are_matched() -> None:
    jd_text = "负责团队协作与业务沟通，推进项目落地。"

    report = extract_skill_report(jd_text)

    assert report.required_skills == []
    assert report.engineering_skills == []
    assert report.llm_skills == []
    assert report.agent_skills == []
    assert report.rag_skills == []
    assert report.production_skills == []
    assert report.bonus_skills == []
