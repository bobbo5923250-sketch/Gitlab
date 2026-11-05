from agent.core import Agent, parse_text_tool_call
from agent.tools import analyze_csv, calculator, list_files, read_file


def test_calculator_basic_math():
    assert calculator("2 + 3 * 4") == "14"
    assert calculator("(10 - 4) / 3") == "2.0"
    assert calculator("2 ** 10") == "1024"


def test_calculator_rejects_code():
    assert calculator("__import__('os').system('dir')").startswith("Error")


def test_read_file_inside_workspace():
    assert "sales.csv" in list_files()
    assert "revenue_thb" in read_file("sales.csv")


def test_read_file_blocks_path_traversal():
    assert read_file("../agent/tools.py").startswith("Error")


def test_analyze_csv_groups_and_sorts():
    result = analyze_csv("sales.csv", "month", "revenue_thb")
    assert result.splitlines()[0] == "2025-03: 663,000.00"  # 480,000 + 183,000
    assert analyze_csv("sales.csv", "nope", "revenue_thb").startswith("Error")


def test_parse_text_tool_call():
    assert parse_text_tool_call('{"name": "calculator", "parameters": {"expression": "1+1"}}') == (
        "calculator",
        {"expression": "1+1"},
    )
    assert parse_text_tool_call("The answer is 42.") is None
    assert parse_text_tool_call('{"not": "a call"}') is None


def test_unknown_tool_and_bad_args_are_reported():
    agent = Agent()
    assert agent._call_tool("nope", {}).startswith("Error")
    assert agent._call_tool("calculator", {"wrong": "x"}).startswith("Error")
