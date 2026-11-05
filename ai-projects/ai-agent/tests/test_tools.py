from agent.core import Agent
from agent.tools import calculator, list_files, read_file


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


def test_unknown_tool_and_bad_args_are_reported():
    agent = Agent()
    assert agent._call_tool("nope", {}).startswith("Error")
    assert agent._call_tool("calculator", {"wrong": "x"}).startswith("Error")
