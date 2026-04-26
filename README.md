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

  - 我先把仓库整理成文档要求的基础结构，目的是让后面的读取、解析、测试、服务化都有固定位置。
    - 文件逻辑：
      app/services 放业务逻辑
      app/schemas 放结构定义
      scripts 放 CLI 脚本
      data 放示例输入
      tests 放测试

- `Task 1.2`：已完成 JD 文本读取、校验和清洗

  - 这一部分在 jd_reader.py；
  - 核心函数是：read_jd_text() 和 clean_jd_text()
  - 它负责 4 件事：
    1.只允许 .txt
    2.检查文件是否存在
    3.检查内容是否为空
    4.清理多余空行和空格
  - **具体逻辑**
    read_jd_text() 的处理顺序是：
    1.把传入路径转成 Path
    2.判断文件是否存在
    3.判断是不是文件而不是目录
    4.判断后缀是不是 .txt
    5.用 utf-8-sig 读取
    6.调 clean_jd_text() 清洗
    7.清洗后为空就报错
    8.返回清洗后的字符串

- `Task 1.3`：已完成规则版技能提取

  - 这一部分在 jd_parser.py；

  - 核心函数是：find_matched_keywords()、extract_role()、extract_skill_report()

  - 1.我先把技能池固定成分类结构：engineering、llm、agent、rag、production

    另外单独补了：BONUS_KEYWORDS
    这样做的原因是文档最终输出需要区分：
    •核心技能
    •加分项
    •各分类技能

  - 2.规则匹配逻辑
    find_matched_keywords() 做的是最简单但稳定的一版：
    •把全文转小写
    •把每个关键词也转小写
    •用 keyword.lower() in text.lower() 判断是否命中
    •输出时仍保留关键词原始写法

  - 3.角色提取
    我补了一个简单角色提取函数 extract_role()：
    •先在文本里找已知岗位名
    •找不到就退回第一行
    这么做是为了让输出结构里能有 role，也方便直接进入 Task 1.4。

  - 4.汇总结构
    extract_skill_report() 会分别提取：
    •engineering_skills
    •llm_skills
    •agent_skills
    •rag_skills
    •production_skills
    •bonus_skills
    然后把核心分类技能合并成：required_skills

- `Task 1.4`：已完成结构化 JSON 输出

- `Task 1.5`：已补齐单元测试

