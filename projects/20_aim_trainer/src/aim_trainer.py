import math
import random
import time

import pygame

WIDTH = 800
HEIGHT = 600
WINDOW_TITLE = "Aim Trainer"
FPS = 60

TARGET_INCREMENT = 400
TARGET_PADDING = 30
TARGET_EVENT = pygame.USEREVENT

BG_COLOR = (0, 25, 40)
TOP_BAR_COLOR = "grey"
TEXT_COLOR = "black"
END_TEXT_COLOR = "white"

TOP_BAR_HEIGHT = 50
LIVES = 3

FONT_NAME = "comicsans"
FONT_SIZE = 24

LABEL_FONT = None


def format_time(seconds):
    minutes = int(seconds // 60)
    seconds_left = seconds % 60

    return f"{minutes:02d}:{seconds_left:04.1f}"


def calculate_speed(targets_pressed, elapsed_time):
    if elapsed_time <= 0:
        return 0

    return targets_pressed / elapsed_time


def calculate_accuracy(targets_pressed, clicks):
    if clicks <= 0:
        return 0

    return targets_pressed / clicks * 100


def get_center_x(surface):
    return WIDTH / 2 - surface.get_width() / 2


class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, window):
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(window, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(window, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    def collide(self, mouse_x, mouse_y):
        distance = math.sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2)

        return distance <= self.size


def create_random_target():
    x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
    y = random.randint(TOP_BAR_HEIGHT + TARGET_PADDING, HEIGHT - TARGET_PADDING)

    return Target(x, y)


def draw_top_bar(window, elapsed_time, targets_pressed, misses):
    remaining_lives = LIVES - misses
    speed = calculate_speed(targets_pressed, elapsed_time)

    pygame.draw.rect(window, TOP_BAR_COLOR, (0, 0, WIDTH, TOP_BAR_HEIGHT))

    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}",
        True,
        TEXT_COLOR,
    )
    speed_label = LABEL_FONT.render(
        f"Speed: {speed:.1f} t/s",
        True,
        TEXT_COLOR,
    )
    hits_label = LABEL_FONT.render(
        f"Hits: {targets_pressed}",
        True,
        TEXT_COLOR,
    )
    lives_label = LABEL_FONT.render(
        f"Lives: {remaining_lives}",
        True,
        TEXT_COLOR,
    )

    window.blit(time_label, (5, 5))
    window.blit(speed_label, (200, 5))
    window.blit(hits_label, (450, 5))
    window.blit(lives_label, (650, 5))


def draw_game(window, targets, elapsed_time, targets_pressed, misses):
    window.fill(BG_COLOR)

    for target in targets:
        target.draw(window)

    draw_top_bar(window, elapsed_time, targets_pressed, misses)


def draw_end_screen(window, elapsed_time, targets_pressed, clicks):
    speed = calculate_speed(targets_pressed, elapsed_time)
    accuracy = calculate_accuracy(targets_pressed, clicks)

    window.fill(BG_COLOR)

    title_label = LABEL_FONT.render("Game Over", True, END_TEXT_COLOR)
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}",
        True,
        END_TEXT_COLOR,
    )
    speed_label = LABEL_FONT.render(
        f"Speed: {speed:.1f} t/s",
        True,
        END_TEXT_COLOR,
    )
    hits_label = LABEL_FONT.render(
        f"Hits: {targets_pressed}",
        True,
        END_TEXT_COLOR,
    )
    accuracy_label = LABEL_FONT.render(
        f"Accuracy: {accuracy:.1f}%",
        True,
        END_TEXT_COLOR,
    )
    exit_label = LABEL_FONT.render(
        "Press any key or close the window to exit.",
        True,
        END_TEXT_COLOR,
    )

    window.blit(title_label, (get_center_x(title_label), 120))
    window.blit(time_label, (get_center_x(time_label), 180))
    window.blit(speed_label, (get_center_x(speed_label), 220))
    window.blit(hits_label, (get_center_x(hits_label), 260))
    window.blit(accuracy_label, (get_center_x(accuracy_label), 300))
    window.blit(exit_label, (get_center_x(exit_label), 380))

    pygame.display.update()

    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

            if event.type == pygame.KEYDOWN:
                waiting = False


def main():
    global LABEL_FONT

    pygame.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    LABEL_FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
    clock = pygame.time.Clock()

    targets = []
    targets_pressed = 0
    clicks = 0
    misses = 0

    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    running = True

    while running:
        clock.tick(FPS)
        click = False
        mouse_position = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == TARGET_EVENT:
                targets.append(create_random_target())

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets[:]:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1
                continue

            if click and target.collide(*mouse_position):
                targets.remove(target)
                targets_pressed += 1
                break

        if misses >= LIVES:
            draw_end_screen(window, elapsed_time, targets_pressed, clicks)
            running = False

        draw_game(window, targets, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
