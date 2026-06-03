import curses
import random
import time
from curses import wrapper
from pathlib import Path

project_dir = Path(__file__).parent.parent
TEXT_FILE = project_dir / "text.txt"

GREEN_PAIR = 1
RED_PAIR = 2
WHITE_PAIR = 3

ESCAPE_KEY = 27


def load_prompts():
    lines = TEXT_FILE.read_text(encoding="utf-8").splitlines()
    prompts = []

    for line in lines:
        if line.strip():
            prompts.append(line.strip())

    return prompts


def choose_prompt(prompts):
    target_text = random.choice(prompts)
    return target_text


def calculate_wpm(character_count, elapsed_seconds):
    elapsed_seconds = max(elapsed_seconds, 1)
    wpm = round((character_count / 5) / (elapsed_seconds / 60))
    return wpm


def is_escape_key(key):
    return len(key) == 1 and ord(key) == ESCAPE_KEY


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to the WPM Typing Test!")
    stdscr.addstr(1, 0, "Press any key to begin.")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target_text, current_text, wpm):
    stdscr.clear()
    stdscr.addstr(0, 0, target_text)
    stdscr.addstr(1, 0, f"WPM: {wpm}")
    stdscr.addstr(2, 0, "Press Esc to exit.")

    for index, char in enumerate(current_text):
        correct_char = target_text[index]

        if char == correct_char:
            color = curses.color_pair(GREEN_PAIR)

        else:
            color = curses.color_pair(RED_PAIR)

        stdscr.addstr(0, index, char, color)

    stdscr.refresh()


def handle_key(current_text, key, target_text):
    if key in ("KEY_BACKSPACE", "\b", "\x7f"):
        if len(current_text) > 0:
            current_text.pop()

    elif len(current_text) < len(target_text):
        if len(key) == 1:
            current_text.append(key)


def run_typing_round(stdscr, target_text):
    current_text = []
    start_time = time.time()

    stdscr.nodelay(True)

    while True:
        elapsed_seconds = max(time.time() - start_time, 1)
        wpm = calculate_wpm(len(current_text), elapsed_seconds)
        display_text(stdscr, target_text, current_text, wpm)

        typed_text = "".join(current_text)
        if typed_text == target_text:
            stdscr.nodelay(False)
            stdscr.addstr(4, 0, "You completed the text! Press any key to continue.")
            stdscr.refresh()
            key = stdscr.getkey()

            if is_escape_key(key):
                return True
            break

        try:
            key = stdscr.getkey()
        except curses.error:
            continue

        if is_escape_key(key):
            stdscr.nodelay(False)
            return True

        handle_key(current_text, key, target_text)


def initialize_colors():
    curses.init_pair(GREEN_PAIR, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(RED_PAIR, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(WHITE_PAIR, curses.COLOR_WHITE, curses.COLOR_BLACK)


def main(stdscr):
    initialize_colors()
    start_screen(stdscr)
    prompts = load_prompts()

    while True:
        target_text = choose_prompt(prompts)
        user_wants_to_quit = run_typing_round(stdscr, target_text)

        if user_wants_to_quit:
            break


if __name__ == "__main__":
    wrapper(main)
