"""Simple worm (snake) game implemented with curses.

Use arrow keys to move the worm. Eat food (π) to grow. Avoid hitting the
borders or yourself. Press 'q' to quit.
"""

import curses
import random


def main(stdscr):
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(True)
    win.nodelay(True)
    win.timeout(100)
    win.border()

    snk_y = sh // 2
    snk_x = sw // 4
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2],
    ]

    food = [sh // 2, sw // 2]
    win.addch(food[0], food[1], curses.ACS_PI)

    key = curses.KEY_RIGHT

    while True:
        try:
            next_key = win.getch()
        except curses.error:
            next_key = -1
        if next_key != -1:
            if next_key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, ord('q')]:
                key = next_key
        if key == ord('q'):
            break

        new_head = [snake[0][0], snake[0][1]]
        if key == curses.KEY_UP:
            new_head[0] -= 1
        elif key == curses.KEY_DOWN:
            new_head[0] += 1
        elif key == curses.KEY_LEFT:
            new_head[1] -= 1
        elif key == curses.KEY_RIGHT:
            new_head[1] += 1

        if (
            new_head[0] in [0, sh - 1]
            or new_head[1] in [0, sw - 1]
            or new_head in snake
        ):
            break

        snake.insert(0, new_head)
        if new_head == food:
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh - 2),
                    random.randint(1, sw - 2),
                ]
                if nf not in snake:
                    food = nf
            win.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')

        win.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

    win.nodelay(False)
    msg = "Game Over!"
    win.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
    win.refresh()
    win.getch()


if __name__ == "__main__":
    curses.wrapper(main)
