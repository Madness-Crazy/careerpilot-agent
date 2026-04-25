from __future__ import annotations

from app.schemas.jd import JDParseResult


# 这里先用规则匹配做第一版技能提取，后面接入 LLM 时也可以保留这层，
# 作为兜底逻辑、对照基线或者回退方案。
SKILL_KEYWORDS: dict[str, list[str]] = {
    "engineering": ["Python", "FastAPI", "Docker", "Git", "Linux", "CI/CD"],
    "llm": ["OpenAI", "Claude", "Qwen", "Prompt", "JSON Schema", "Streaming"],
    "agent": ["Function Calling", "Tool Use", "Workflow", "Memory", "LangGraph"],
    "rag": ["RAG", "Embedding", "Vector DB", "Chroma", "FAISS", "Milvus"],
    "production": ["Eval", "A/B Test", "Logging", "Cost", "Latency", "Prompt Injection"],
}

# 奖励项通常不是硬性要求，但在 JD 里出现时值得单独保留。
BONUS_KEYWORDS: list[str] = ["MCP", "多模态", "本地模型部署"]

# 角色提取先做一个足够简单的版本：优先匹配已知岗位名，
# 匹配不到时再退回到正文第一行。
ROLE_KEYWORDS: list[str] = [
    "AI Agent Engineer",
    "Agent Engineer",
    "AI Engineer",
    "LLM Engineer",
    "算法工程师",
    "AI Agent 工程师",
    "大模型应用工程师",
]


def extract_role(text: str) -> str | None:
    lowered_text = text.lower()
    for role in ROLE_KEYWORDS:
        if role.lower() in lowered_text:
            return role

    first_line = text.splitlines()[0].strip() if text.splitlines() else ""
    return first_line or None


def find_matched_keywords(text: str, keywords: list[str]) -> list[str]:
    lowered_text = text.lower()
    matched_keywords: list[str] = []

    # 统一做大小写不敏感匹配，同时保留原始关键词写法，方便最终输出。
    for keyword in keywords:
        if keyword.lower() in lowered_text:
            matched_keywords.append(keyword)

    return matched_keywords


def extract_skill_report(text: str) -> JDParseResult:
    engineering_skills = find_matched_keywords(text, SKILL_KEYWORDS["engineering"])
    llm_skills = find_matched_keywords(text, SKILL_KEYWORDS["llm"])
    agent_skills = find_matched_keywords(text, SKILL_KEYWORDS["agent"])
    rag_skills = find_matched_keywords(text, SKILL_KEYWORDS["rag"])
    production_skills = find_matched_keywords(text, SKILL_KEYWORDS["production"])
    bonus_skills = find_matched_keywords(text, BONUS_KEYWORDS)

    # required_skills 先定义为核心分类技能的并集，不包含 bonus，
    # 这样更接近“岗位硬要求”的概念。
    required_skills = [
        *engineering_skills,
        *llm_skills,
        *agent_skills,
        *rag_skills,
        *production_skills,
    ]

    return JDParseResult(
        role=extract_role(text),
        required_skills=required_skills,
        bonus_skills=bonus_skills,
        engineering_skills=engineering_skills,
        llm_skills=llm_skills,
        agent_skills=agent_skills,
        rag_skills=rag_skills,
        production_skills=production_skills,
    )
