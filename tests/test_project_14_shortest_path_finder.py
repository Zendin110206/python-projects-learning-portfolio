import importlib.util
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "projects" / "14_shortest_path_finder" / "src" / "shortest_path_finder.py"

EXPECTED_PATH = [
    (0, 1),
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (6, 1),
    (7, 1),
    (7, 2),
    (7, 3),
    (7, 4),
    (7, 5),
    (7, 6),
    (7, 7),
    (8, 7),
]


class FakeScreen:
    def __init__(self) -> None:
        self.clear_count = 0
        self.refresh_count = 0
        self.getch_count = 0
        self.added_strings = []

    def clear(self) -> None:
        self.clear_count += 1

    def refresh(self) -> None:
        self.refresh_count += 1

    def addstr(self, *args) -> None:
        self.added_strings.append(args)

    def getch(self) -> None:
        self.getch_count += 1


def load_shortest_path_finder() -> ModuleType:
    spec = importlib.util.spec_from_file_location("shortest_path_finder_under_test", SCRIPT)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def test_module_import_does_not_start_curses_wrapper() -> None:
    with patch("curses.wrapper") as wrapper:
        load_shortest_path_finder()

    wrapper.assert_not_called()


def test_find_position_returns_start_and_end_coordinates() -> None:
    shortest_path_finder = load_shortest_path_finder()

    assert shortest_path_finder.find_position(shortest_path_finder.MAZE, "O") == (0, 1)
    assert shortest_path_finder.find_position(shortest_path_finder.MAZE, "X") == (8, 7)
    assert shortest_path_finder.find_position(shortest_path_finder.MAZE, "?") is None


def test_find_neighbors_keeps_positions_inside_grid() -> None:
    shortest_path_finder = load_shortest_path_finder()

    assert shortest_path_finder.find_neighbors(shortest_path_finder.MAZE, 0, 1) == [
        (1, 1),
        (0, 0),
        (0, 2),
    ]
    assert shortest_path_finder.find_neighbors(shortest_path_finder.MAZE, 1, 1) == [
        (0, 1),
        (2, 1),
        (1, 0),
        (1, 2),
    ]


def test_find_shortest_path_returns_expected_default_path() -> None:
    shortest_path_finder = load_shortest_path_finder()

    path = shortest_path_finder.find_shortest_path(shortest_path_finder.MAZE, delay=0)

    assert path == EXPECTED_PATH


def test_find_shortest_path_does_not_cross_walls() -> None:
    shortest_path_finder = load_shortest_path_finder()

    path = shortest_path_finder.find_shortest_path(shortest_path_finder.MAZE, delay=0)

    assert path is not None
    assert all(
        shortest_path_finder.MAZE[row][col] != shortest_path_finder.WALL
        for row, col in path
    )


def test_find_shortest_path_returns_none_when_no_path_exists() -> None:
    shortest_path_finder = load_shortest_path_finder()
    blocked_maze = [["O", "#", "X"]]

    path = shortest_path_finder.find_shortest_path(blocked_maze, delay=0)

    assert path is None


def test_draw_maze_marks_path_without_replacing_start_or_end() -> None:
    shortest_path_finder = load_shortest_path_finder()
    screen = FakeScreen()

    shortest_path_finder.draw_maze(
        screen,
        shortest_path_finder.MAZE,
        path=[(0, 1), (1, 1), (8, 7)],
    )

    assert screen.clear_count == 1
    assert screen.refresh_count == 1
    assert (0, 2, "O") in screen.added_strings
    assert (1, 2, "*") in screen.added_strings
    assert (8, 14, "X") in screen.added_strings


def test_find_shortest_path_can_animate_with_screen() -> None:
    shortest_path_finder = load_shortest_path_finder()
    screen = FakeScreen()

    with patch.object(shortest_path_finder.time, "sleep") as sleep:
        path = shortest_path_finder.find_shortest_path(
            shortest_path_finder.MAZE,
            screen,
            delay=0,
        )

    assert path == EXPECTED_PATH
    assert screen.clear_count > 0
    assert sleep.call_count == screen.clear_count


def test_main_shows_success_message_and_waits_for_key() -> None:
    shortest_path_finder = load_shortest_path_finder()
    screen = FakeScreen()

    with patch.object(shortest_path_finder, "find_shortest_path", return_value=EXPECTED_PATH):
        shortest_path_finder.main(screen)

    assert (10, 0, "Path found. Press any key to exit.") in screen.added_strings
    assert screen.getch_count == 1


def test_main_shows_no_path_message_and_waits_for_key() -> None:
    shortest_path_finder = load_shortest_path_finder()
    screen = FakeScreen()

    with patch.object(shortest_path_finder, "find_shortest_path", return_value=None):
        shortest_path_finder.main(screen)

    assert (10, 0, "No path found. Press any key to exit.") in screen.added_strings
    assert screen.getch_count == 1
