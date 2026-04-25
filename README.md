# CareerPilot Agent

面向 `AI Agent Engineer` 求职场景的学习规划项目。当前已完成 `Phase 1`：JD 解析 CLI。

## Phase 1 已实现内容

- 读取 `.txt` 格式 JD 文件
- 对输入文本做清洗，删除多余空行和首尾空格
- 对异常输入给出中文错误提示
- 基于规则匹配提取岗位技能
- 输出结构化 JSON 到终端
- 自动生成同目录下的 JSON 结果文件
- 提供中英文测试用例

## 目录结构

```text
careerpilot-agent/
  app/
    schemas/
      jd.py
    services/
      jd_reader.py
      jd_parser.py
  data/
    sample_jd.txt
    sample_jd_cn.txt
  scripts/
    parse_jd.py
  tests/
    test_jd_reader.py
    test_jd_parser.py
    test_parse_jd_cli.py
  README.md
  requirements.txt
```

## 安装依赖

```bash
python -m pip install -r requirements.txt
```

## 运行 CLI

英文示例：

```bash
python scripts/parse_jd.py data/sample_jd.txt
```

中文示例：

```bash
python scripts/parse_jd.py data/sample_jd_cn.txt
```

运行后会有两个结果：

1. 终端打印结构化 JSON
2. 在原 JD 文件旁边生成一个同名 `.json` 文件

例如：

```text
data/sample_jd.txt
data/sample_jd.json
```

## 输出字段说明

- `role`：岗位名称
- `required_skills`：岗位核心技能汇总
- `bonus_skills`：岗位加分项
- `engineering_skills`：工程类技能
- `llm_skills`：LLM 类技能
- `agent_skills`：Agent 类技能
- `rag_skills`：RAG 类技能
- `production_skills`：生产化类技能

## 运行测试

```bash
pytest tests
```

当前测试覆盖：

- 正常读取 JD 文件
- 文件不存在
- 非 `.txt` 文件
- 空文件和空白文件
- 中文 JD 识别
- 英文 JD 识别
- CLI 生成 JSON 结果文件

## 当前限制

- Phase 1 只支持 `.txt`
- 技能提取基于关键词规则，不做语义理解
- 同义词和更复杂的上下文判断将在后续阶段继续增强

## 与文档要求的对应关系

- `Task 1.1`：已创建项目基础目录结构
- `Task 1.2`：已完成 JD 文本读取、校验和清洗
- `Task 1.3`：已完成规则版技能提取
- `Task 1.4`：已完成结构化 JSON 输出
- `Task 1.5`：已补齐单元测试

## 当前未在仓库内完成的事项

以下事项属于外部环境动作，当前仓库代码无法直接代替：

- 创建 GitHub 仓库
- 提交 Git commit 记录
- 创建和激活虚拟环境

如果需要，我可以下一步继续补 `Phase 2` 的 FastAPI 服务化。
