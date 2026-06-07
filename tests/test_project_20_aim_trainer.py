import importlib.util
import os
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock, patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "projects" / "20_aim_trainer" / "src" / "aim_trainer.py"


def load_aim_trainer() -> ModuleType:
    spec = importlib.util.spec_from_file_location("aim_trainer_under_test", SCRIPT)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def test_module_import_does_not_initialize_pygame_or_open_window() -> None:
    with (
        patch("pygame.init") as pygame_init,
        patch("pygame.display.set_mode") as set_mode,
    ):
        aim_trainer = load_aim_trainer()

    pygame_init.assert_not_called()
    set_mode.assert_not_called()
    assert aim_trainer.LABEL_FONT is None


def test_core_constants_match_project_spec() -> None:
    aim_trainer = load_aim_trainer()

    assert aim_trainer.WIDTH == 800
    assert aim_trainer.HEIGHT == 600
    assert aim_trainer.WINDOW_TITLE == "Aim Trainer"
    assert aim_trainer.FPS == 60
    assert aim_trainer.TARGET_INCREMENT == 400
    assert aim_trainer.TARGET_PADDING == 30
    assert aim_trainer.TOP_BAR_HEIGHT == 50
    assert aim_trainer.LIVES == 3


def test_format_time_uses_minutes_seconds_and_tenths() -> None:
    aim_trainer = load_aim_trainer()

    assert aim_trainer.format_time(0) == "00:00.0"
    assert aim_trainer.format_time(5.4) == "00:05.4"
    assert aim_trainer.format_time(65.2) == "01:05.2"


def test_calculate_speed_and_accuracy_handle_zero_values() -> None:
    aim_trainer = load_aim_trainer()

    assert aim_trainer.calculate_speed(5, 10) == 0.5
    assert aim_trainer.calculate_speed(0, 10) == 0
    assert aim_trainer.calculate_speed(5, 0) == 0
    assert aim_trainer.calculate_accuracy(5, 10) == 50
    assert aim_trainer.calculate_accuracy(0, 0) == 0


def test_get_center_x_centers_surface_width() -> None:
    aim_trainer = load_aim_trainer()
    surface = Mock()
    surface.get_width.return_value = 200

    assert aim_trainer.get_center_x(surface) == 300


def test_target_starts_small_grows_then_shrinks() -> None:
    aim_trainer = load_aim_trainer()
    target = aim_trainer.Target(100, 120)

    assert target.x == 100
    assert target.y == 120
    assert target.size == 0
    assert target.grow is True

    target.update()
    assert target.size == target.GROWTH_RATE

    target.size = target.MAX_SIZE - target.GROWTH_RATE
    target.update()

    assert target.grow is False
    assert target.size == target.MAX_SIZE - (target.GROWTH_RATE * 2)


def test_target_collision_uses_current_radius() -> None:
    aim_trainer = load_aim_trainer()
    target = aim_trainer.Target(100, 100)
    target.size = 20

    assert target.collide(100, 100) is True
    assert target.collide(120, 100) is True
    assert target.collide(121, 100) is False


def test_create_random_target_stays_inside_playable_area() -> None:
    aim_trainer = load_aim_trainer()

    with patch.object(aim_trainer.random, "randint", side_effect=[30, 80]) as randint:
        target = aim_trainer.create_random_target()

    assert target.x == 30
    assert target.y == 80
    randint.assert_any_call(
        aim_trainer.TARGET_PADDING,
        aim_trainer.WIDTH - aim_trainer.TARGET_PADDING,
    )
    randint.assert_any_call(
        aim_trainer.TOP_BAR_HEIGHT + aim_trainer.TARGET_PADDING,
        aim_trainer.HEIGHT - aim_trainer.TARGET_PADDING,
    )


def test_draw_top_bar_renders_expected_labels() -> None:
    aim_trainer = load_aim_trainer()
    font = Mock()
    window = Mock()
    font.render.side_effect = [
        "time-label",
        "speed-label",
        "hits-label",
        "lives-label",
    ]

    with (
        patch.object(aim_trainer, "LABEL_FONT", font),
        patch.object(aim_trainer.pygame.draw, "rect") as draw_rect,
    ):
        aim_trainer.draw_top_bar(window, elapsed_time=10, targets_pressed=5, misses=1)

    draw_rect.assert_called_once_with(
        window,
        aim_trainer.TOP_BAR_COLOR,
        (0, 0, aim_trainer.WIDTH, aim_trainer.TOP_BAR_HEIGHT),
    )
    assert [call.args[0] for call in font.render.call_args_list] == [
        "Time: 00:10.0",
        "Speed: 0.5 t/s",
        "Hits: 5",
        "Lives: 2",
    ]
    window.blit.assert_any_call("time-label", (5, 5))
    window.blit.assert_any_call("speed-label", (200, 5))
    window.blit.assert_any_call("hits-label", (450, 5))
    window.blit.assert_any_call("lives-label", (650, 5))
