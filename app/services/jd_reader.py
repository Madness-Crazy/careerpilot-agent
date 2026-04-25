from pathlib import Path


class JDReaderError(Exception):
    """JD 文件读取或校验失败时抛出。"""


def clean_jd_text(text: str) -> str:
    # 先清理每一行首尾空白，再删除空行，保证输出结果稳定，
    # 不会因为复制来的多余换行或空格影响后续解析。
    lines = [line.strip() for line in text.splitlines()]
    non_empty_lines = [line for line in lines if line]
    return "\n".join(non_empty_lines).strip()


def read_jd_text(file_path: str | Path) -> str:
    # 同时兼容字符串路径和 Path 对象，方便后续在 CLI 和服务层复用。
    path = Path(file_path)

    if not path.exists():
        raise JDReaderError(f"未找到 JD 文件：{path}")

    if not path.is_file():
        raise JDReaderError(f"给定路径不是文件：{path}")

    if path.suffix.lower() != ".txt":
        raise JDReaderError("Phase 1 只支持读取 .txt 格式的 JD 文件。")

    try:
        # utf-8-sig 可以自动处理带 BOM 的 UTF-8 文件，
        # 这在 Windows 编辑器里很常见，避免把 BOM 读进正文。
        raw_text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise JDReaderError(f"文件无法按 UTF-8 编码读取：{path}") from exc

    cleaned_text = clean_jd_text(raw_text)
    if not cleaned_text:
        raise JDReaderError(f"JD 文件清洗后内容为空：{path}")

    return cleaned_text
