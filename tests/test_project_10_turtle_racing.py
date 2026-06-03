import importlib.util
import io
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "projects" / "10_turtle_racing" / "src" / "turtle_racing.py"


def load_turtle_racing() -> ModuleType:
    spec = importlib.util.spec_from_file_location("turtle_racing_under_test", SCRIPT)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def call_with_inputs(function, player_inputs: list[str], *args):
    inputs = iter(player_inputs)
    output = io.StringIO()

    def fake_input(prompt: str = "") -> str:
        print(prompt, end="")
        return next(inputs)

    with patch("builtins.input", fake_input), redirect_stdout(output):
        result = function(*args)

    return result, output.getvalue()


def run_with_inputs(function, player_inputs: list[str], *args) -> str:
    _, output = call_with_inputs(function, player_inputs, *args)

    return output


class FakeScreen:
    def __init__(self) -> None:
        self.size = None
        self.window_title = None
        self.exit_requested = False

    def setup(self, width: int, height: int) -> None:
        self.size = (width, height)

    def title(self, window_title: str) -> None:
        self.window_title = window_title

    def exitonclick(self) -> None:
        self.exit_requested = True


class FakeRacer:
    def __init__(self, shape: str = "classic") -> None:
        self.shape = shape
        self.color_name = None
        self.pen_is_up = False
        self.position = (0, 0)
        self.x_position = 0
        self.forward_calls = []

    def color(self, color_name: str) -> None:
        self.color_name = color_name

    def penup(self) -> None:
        self.pen_is_up = True

    def goto(self, x_position: int, y_position: int) -> None:
        self.position = (x_position, y_position)
        self.x_position = x_position

    def forward(self, distance: int) -> None:
        self.forward_calls.append(distance)
        self.x_position += distance

    def xcor(self) -> int:
        return self.x_position

    def pencolor(self) -> str:
        assert self.color_name is not None

        return self.color_name


def test_module_import_does_not_create_turtle_window() -> None:
    with (
        patch("turtle.Screen") as screen,
        patch("turtle.Turtle") as turtle,
    ):
        load_turtle_racing()

    screen.assert_not_called()
    turtle.assert_not_called()


def test_get_racer_count_retries_until_valid_number() -> None:
    turtle_racing = load_turtle_racing()

    racer_count, output = call_with_inputs(
        turtle_racing.get_racer_count,
        ["abc", "1", "9", "4"],
    )

    assert racer_count == 4
    assert "Please enter a number." in output
    assert output.count("Racer count must be between 2 and 8.") == 2


def test_calculate_y_positions_spreads_racers_evenly() -> None:
    turtle_racing = load_turtle_racing()

    assert turtle_racing.calculate_y_positions(4) == [-150, -50, 50, 150]


def test_setup_screen_uses_expected_size_and_title() -> None:
    turtle_racing = load_turtle_racing()
    fake_screen = FakeScreen()

    with patch.object(turtle_racing.turtle, "Screen", return_value=fake_screen):
        screen = turtle_racing.setup_screen()

    assert screen is fake_screen
    assert fake_screen.size == (700, 500)
    assert fake_screen.window_title == "Turtle Racing"


def test_create_racers_uses_colors_and_start_positions() -> None:
    turtle_racing = load_turtle_racing()
    created_racers: list[FakeRacer] = []

    def make_racer(shape: str) -> FakeRacer:
        racer = FakeRacer(shape=shape)
        created_racers.append(racer)
        return racer

    with patch.object(turtle_racing.turtle, "Turtle", side_effect=make_racer):
        racers = turtle_racing.create_racers(3)

    assert racers == created_racers
    assert [racer.shape for racer in racers] == ["turtle", "turtle", "turtle"]
    assert [racer.color_name for racer in racers] == ["red", "green", "blue"]
    assert [racer.position for racer in racers] == [(-300, -125), (-300, 0), (-300, 125)]
    assert all(racer.pen_is_up for racer in racers)


def test_race_returns_first_racer_to_reach_finish() -> None:
    turtle_racing = load_turtle_racing()
    red_racer = FakeRacer()
    blue_racer = FakeRacer()
    red_racer.color("red")
    blue_racer.color("blue")
    red_racer.goto(295, 0)
    blue_racer.goto(100, 0)

    with patch.object(turtle_racing.rd, "randrange", return_value=10):
        winner_color = turtle_racing.race([red_racer, blue_racer])

    assert winner_color == "red"
    assert red_racer.forward_calls == [10]
    assert blue_racer.forward_calls == []


def test_main_prints_winner_and_waits_for_window_close() -> None:
    turtle_racing = load_turtle_racing()
    fake_screen = FakeScreen()

    with (
        patch.object(turtle_racing, "get_racer_count", return_value=4),
        patch.object(turtle_racing, "setup_screen", return_value=fake_screen),
        patch.object(turtle_racing, "create_racers", return_value=["racers"]),
        patch.object(turtle_racing, "race", return_value="purple"),
    ):
        output = run_with_inputs(turtle_racing.main, [])

    assert "The winner is purple!" in output
    assert fake_screen.exit_requested is True
