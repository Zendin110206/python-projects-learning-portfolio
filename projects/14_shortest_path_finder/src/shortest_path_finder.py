import queue
import time
from curses import wrapper

MAZE = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"],
]

WALL = "#"
START = "O"
END = "X"
PATH_MARKER = "*"
SEARCH_DELAY = 0.2


def find_position(maze, target):
    for row_index, row in enumerate(maze):
        for col_index, value in enumerate(row):
            if value == target:
                return (row_index, col_index)

    return None


def find_neighbors(maze, row, col):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    row_count = len(maze)
    col_count = len(maze[0])

    for r, c in directions:
        new_row = row + r
        new_col = col + c

        if 0 <= new_row < row_count and 0 <= new_col < col_count:
            neighbors.append((new_row, new_col))

    return neighbors


def draw_maze(stdscr, maze, path=None):
    if path is None:
        path = []

    stdscr.clear()

    for row_index, row in enumerate(maze):
        for col_index, value in enumerate(row):
            if (row_index, col_index) in path and value == " ":
                value = PATH_MARKER
            stdscr.addstr(row_index, col_index * 2, value)

    stdscr.refresh()


def find_shortest_path(maze, stdscr=None, delay=SEARCH_DELAY):
    start_position = find_position(maze, START)

    if start_position is None:
        return None

    work_queue = queue.Queue()

    work_queue.put((start_position, [start_position]))
    visited = {start_position}

    while not work_queue.empty():
        current_position, path = work_queue.get()

        if stdscr is not None:
            draw_maze(stdscr, maze, path)
            time.sleep(delay)

        row, col = current_position[0], current_position[1]

        if maze[row][col] == END:
            return path

        neighbors = find_neighbors(maze, row, col)

        for neighbor in neighbors:
            n_row, n_col = neighbor

            if maze[n_row][n_col] == WALL:
                continue

            if neighbor in visited:
                continue

            new_path = path + [neighbor]
            work_queue.put((neighbor, new_path))
            visited.add(neighbor)

    return None


def main(stdscr):
    path = find_shortest_path(MAZE, stdscr)

    msg_row = len(MAZE) + 1

    if path is not None:
        draw_maze(stdscr, MAZE, path)
        stdscr.addstr(msg_row, 0, "Path found. Press any key to exit.")

    else:
        stdscr.addstr(msg_row, 0, "No path found. Press any key to exit.")

    stdscr.getch()


if __name__ == "__main__":
    wrapper(main)
