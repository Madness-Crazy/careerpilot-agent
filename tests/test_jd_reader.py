import pytest

from app.services.jd_reader import JDReaderError, clean_jd_text, read_jd_text


def test_read_jd_text_returns_cleaned_content(tmp_path) -> None:
    # 正常 JD 应该能读出内容，并清理掉多余空行与首尾空格。
    jd_file = tmp_path / "sample_jd.txt"
    jd_file.write_text("AI Agent Engineer\n\n  Python  \n\nFastAPI\n", encoding="utf-8")

    result = read_jd_text(jd_file)

    assert result == "AI Agent Engineer\nPython\nFastAPI"


def test_read_jd_text_raises_for_missing_file(tmp_path) -> None:
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(JDReaderError, match="未找到 JD 文件"):
        read_jd_text(missing_file)


def test_read_jd_text_raises_for_non_txt_file(tmp_path) -> None:
    # Phase 1 只允许纯文本输入，先把输入面收窄，减少不必要复杂度。
    jd_file = tmp_path / "sample_jd.md"
    jd_file.write_text("AI Agent Engineer", encoding="utf-8")

    with pytest.raises(JDReaderError, match=r"只支持读取 \.txt"):
        read_jd_text(jd_file)


def test_read_jd_text_raises_for_empty_file(tmp_path) -> None:
    jd_file = tmp_path / "empty_jd.txt"
    jd_file.write_text("", encoding="utf-8")

    with pytest.raises(JDReaderError, match="JD 文件清洗后内容为空"):
        read_jd_text(jd_file)


def test_read_jd_text_raises_for_whitespace_only_file(tmp_path) -> None:
    # 只有空白符的文件本质上等于空文件，也应该被拒绝。
    jd_file = tmp_path / "blank_jd.txt"
    jd_file.write_text("\n   \n\t\n", encoding="utf-8")

    with pytest.raises(JDReaderError, match="JD 文件清洗后内容为空"):
        read_jd_text(jd_file)


def test_clean_jd_text_removes_extra_blank_lines() -> None:
    raw_text = "Role\n\n\nRequirement A\n   \nRequirement B\n"

    result = clean_jd_text(raw_text)

    assert result == "Role\nRequirement A\nRequirement B"
