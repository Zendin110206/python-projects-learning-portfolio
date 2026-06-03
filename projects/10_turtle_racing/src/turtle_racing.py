import random as rd
import turtle

WIDTH = 700
HEIGHT = 500
MIN_RACERS = 2
MAX_RACERS = 8
START_X = -300
FINISH_X = 300
MOVE_MIN = 1
MOVE_MAX = 20

COLORS = ["red", "green", "blue", "orange", "purple", "pink", "yellow", "black"]


def get_racer_count():
    while True:
        racer_count = input(f"Enter the number of racers ({MIN_RACERS} - {MAX_RACERS}): ")

        if not racer_count.isdigit():
            print("Please enter a number.")
            continue

        racer_count = int(racer_count)

        if MIN_RACERS <= racer_count <= MAX_RACERS:
            return racer_count

        print(f"Racer count must be between {MIN_RACERS} and {MAX_RACERS}.")


def calculate_y_positions(racer_count):
    spacing = HEIGHT // (racer_count + 1)
    y_positions = []

    for i in range(1, racer_count + 1):
        y_position = -HEIGHT // 2 + (i * spacing)
        y_positions.append(y_position)

    return y_positions


def setup_screen():
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title("Turtle Racing")

    return screen


def create_racers(racer_count):
    racers = []
    y_positions = calculate_y_positions(racer_count)

    for i in range(racer_count):
        racer = turtle.Turtle(shape="turtle")
        racer.color(COLORS[i])
        racer.penup()
        racer.goto(START_X, y_positions[i])

        racers.append(racer)

    return racers


def race(racers):
    winner_color = None

    while winner_color is None:
        for racer in racers:
            distance = rd.randrange(MOVE_MIN, MOVE_MAX)
            racer.forward(distance)

            if racer.xcor() >= FINISH_X:
                winner_color = racer.pencolor()
                break

    return winner_color


def main():
    racer_count = get_racer_count()
    screen = setup_screen()
    racers = create_racers(racer_count)

    winner_color = race(racers)
    print(f"The winner is {winner_color}!")

    screen.exitonclick()


if __name__ == "__main__":
    main()
