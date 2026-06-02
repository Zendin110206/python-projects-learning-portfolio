import importlib.util
import io
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = ROOT / "projects" / "07_madlibs_generator"
SCRIPT = PROJECT_DIR / "src" / "madlibs_generator.py"
STORY = PROJECT_DIR / "story.txt"


def load_madlibs_generator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("madlibs_generator_under_test", SCRIPT)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def run_with_inputs(function, player_inputs: list[str], *args) -> str:
    inputs = iter(player_inputs)
    output = io.StringIO()

    def fake_input(prompt: str) -> str:
        print(prompt, end="")
        return next(inputs)

    with patch("builtins.input", fake_input), redirect_stdout(output):
        function(*args)

    return output.getvalue()


def test_madlibs_story_template_exists_with_expected_placeholders() -> None:
    story = STORY.read_text(encoding="utf-8")

    assert "Today I went to the <place>." in story
    assert story.count("<adjective>") == 2
    assert story.count("<verb>") == 2


def test_madlibs_finds_unique_placeholders_in_order() -> None:
    madlibs_generator = load_madlibs_generator()
    story = STORY.read_text(encoding="utf-8")

    placeholders = madlibs_generator.find_placeholders(story)

    assert placeholders == ["<place>", "<adjective>", "<noun>", "<verb>"]


def test_madlibs_collects_answers_for_each_placeholder_once() -> None:
    madlibs_generator = load_madlibs_generator()

    output = run_with_inputs(
        madlibs_generator.collect_answers,
        ["library", "bright", "robot", "dance"],
        ["<place>", "<adjective>", "<noun>", "<verb>"],
    )

    assert output.count("Enter a word for") == 4
    assert "Enter a word for <place>: " in output
    assert "Enter a word for <verb>: " in output


def test_madlibs_builds_completed_story() -> None:
    madlibs_generator = load_madlibs_generator()
    story = STORY.read_text(encoding="utf-8")
    answers = {
        "<place>": "library",
        "<adjective>": "bright",
        "<noun>": "robot",
        "<verb>": "dance",
    }

    completed_story = madlibs_generator.build_story(story, answers)

    assert "<place>" not in completed_story
    assert "<adjective>" not in completed_story
    assert "<verb>" not in completed_story
    assert "Today I went to the library." in completed_story
    assert "I saw a bright robot that loved to dance." in completed_story
    assert "Everyone started to dance together, and it became a bright day." in (
        completed_story
    )


def test_madlibs_main_prints_completed_story() -> None:
    madlibs_generator = load_madlibs_generator()

    output = run_with_inputs(
        madlibs_generator.main,
        ["library", "bright", "robot", "dance"],
    )

    assert "Here is your completed story:" in output
    assert "Today I went to the library." in output
    assert "I saw a bright robot that loved to dance." in output
    assert "Everyone started to dance together, and it became a bright day." in output
