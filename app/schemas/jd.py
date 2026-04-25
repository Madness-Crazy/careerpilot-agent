from pydantic import BaseModel, Field


class JDParseResult(BaseModel):
    # role 允许为空，是因为有些 JD 文本本身不包含明确岗位名，
    # 这种情况下后续可以再由规则或 LLM 补充识别。
    role: str | None = Field(default=None, description="岗位名称")
    required_skills: list[str] = Field(default_factory=list, description="岗位核心技能")
    bonus_skills: list[str] = Field(default_factory=list, description="岗位加分项技能")
    engineering_skills: list[str] = Field(default_factory=list, description="工程类技能")
    llm_skills: list[str] = Field(default_factory=list, description="LLM 类技能")
    agent_skills: list[str] = Field(default_factory=list, description="Agent 类技能")
    rag_skills: list[str] = Field(default_factory=list, description="RAG 类技能")
    production_skills: list[str] = Field(default_factory=list, description="生产化类技能")
