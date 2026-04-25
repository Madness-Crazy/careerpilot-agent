import json
import logging
import sys
from pathlib import Path

# 在 Windows 终端里显式切到 UTF-8，避免中文日志和提示在子进程测试里出现解码问题。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# 允许直接用 `python scripts/parse_jd.py ...` 运行脚本时
# 也能导入本地 `app` 包，而不需要先把项目安装成包。
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.jd_parser import extract_skill_report
from app.services.jd_reader import JDReaderError, read_jd_text


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def build_output_path(jd_file_path: str | Path) -> Path:
    # 解析结果默认写到原 JD 文件旁边，方便用户直接看到输入和输出的对应关系。
    return Path(jd_file_path).with_suffix(".json")


def main() -> None:
    if len(sys.argv) != 2:
        print("用法：python scripts/parse_jd.py <jd_file.txt>")
        raise SystemExit(1)

    jd_file_path = sys.argv[1]

    try:
        logger.info("开始读取 JD 文件：%s", jd_file_path)
        jd_text = read_jd_text(jd_file_path)

        logger.info("开始执行规则版技能提取")
        skill_report = extract_skill_report(jd_text)
    except JDReaderError as exc:
        logger.error("JD 文件处理失败：%s", exc)
        print(f"错误：{exc}")
        raise SystemExit(1) from exc

    output_path = build_output_path(jd_file_path)
    json_output = skill_report.model_dump_json(indent=2)

    logger.info("开始写入 JSON 结果文件：%s", output_path)
    output_path.write_text(json_output + "\n", encoding="utf-8")

    logger.info("技能提取完成")
    print(json.dumps(skill_report.model_dump(), ensure_ascii=False, indent=2))
    print(f"\n结果文件已生成：{output_path}")


if __name__ == "__main__":
    main()
