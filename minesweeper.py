"""
Minesweeper game executed by tkinter module
"""

import CONSTANT
import time
from tkinter import *
import random


class button_place:
    def __init__(self, row, col, bomb, button, color, number):
        self.row = row
        self.col = col
        self.bomb = bomb
        self.button = button
        self.color = color
        self.number = number


def find_bombs(row: int, col: int) -> int:

    """
    Find the number of bombs a cell is a neighbor to
    :param row: The row of the cell.
    :param col: The column of the cell.
    :return: The number of bombs a cell is a neighbor to.
    """
    CONSTANT.bombs_count = 0
    for row_place in range(-1, 2):
        for col_place in range(-1, 2):
            if -1 < col + col_place < 9 and -1 < row + row_place < 9:
                if row_place != 0 or col_place != 0:
                    if CONSTANT.lst[row + row_place][col + col_place].bomb:
                        CONSTANT.bombs_count += 1
    return CONSTANT.bombs_count


def change_marker() -> None:

    """
    Change the marker flag according to its' current symbol
    """
    if CONSTANT.marker_flag:
        marker = Button(mark_frame, text="Mark", command=change_marker)
        marker.grid(row=0, column=2)
        CONSTANT.marker_flag = False
    else:
        marker = Button(mark_frame, text="Mark", bg="red",
                        command=change_marker)
        marker.grid(row=0, column=2)
        CONSTANT.marker_flag = True


def check(row: int, col: int) -> None:

    """
    Change the button according to its' current attributes
    :param row: The row of the cell.
    :param col: The column of the cell.
    """
    button_class = CONSTANT.lst[row][col]
    if CONSTANT.marker_flag:
        if button_class.color == "grey" and CONSTANT.count_bombs > 0:
            button_class.button = Button(game_frame, bg="red", padx=7, text="?",
                                         command=lambda: check(row, col))
            button_class.button.grid(row=row, column=col)
            button_class.color = "red2"
            CONSTANT.count_bombs -= 1
            marker_count = Label(mark_frame,
                                 text=f"Marker count: {CONSTANT.count_bombs}")
            marker_count.grid(row=0, column=0)
        elif button_class.color == "red2":
            button_class.button = Button(game_frame, bg="grey", padx=10,
                                         command=lambda: check(row, col))
            button_class.button.grid(row=row, column=col)
            button_class.color = "grey"
            CONSTANT.count_bombs += 1
            marker_count = Label(mark_frame,
                                 text=f"Marker count: {CONSTANT.count_bombs}")
            marker_count.grid(row=0, column=0)
    else:
        if button_class.color == "grey":
            if button_class.bomb:
                button_class.button = Button(game_frame, bg="red",
                                             padx=7, text="*")
                button_class.button.grid(row=row, column=col)
                button_class.color = "red"
                mass = Label(end_frame,
                             text="You found a bomb! Try again!!!", bg="red")
                mass.grid(row=1)
                if CONSTANT.flag:
                    CONSTANT.flag = False
                    for row_place in range(9):
                        for col_place in range(9):
                            check(row_place, col_place)
                            game_frame.update()
            elif button_class.number == 0:
                button_class.button = Label(game_frame,
                                            bg="white", padx=11, pady=3)
                button_class.button.grid(row=row, column=col)
                button_class.color = "white"
                for rows in range(-1, 2):
                    for cols in range(-1, 2):
                        if -1 < col + cols < 9 and -1 < row + rows < 9:
                            if rows != 0 or cols != 0:
                                check(row + rows, col + cols)
            if 1 <= button_class.number <= 8:
                button_class.button = Label(
                    game_frame, bg="white",
                    fg=f"{CONSTANT.color_names[button_class.number]}",
                    padx=9, pady=3, text=f"{button_class.number}")
                button_class.button.grid(row=row, column=col)
                button_class.color = "None"
                for rows in range(-1, 2):
                    for cols in range(-1, 2):
                        if -1 < col + cols < 9 and -1 < row + rows < 9:
                            if rows != 0 or cols != 0:
                                if CONSTANT.lst[row + rows][col + cols].number\
                                        == 0:
                                    check(row + rows, col + cols)


def main() -> None:

    """
    Build the initial board and execute the game
    """
    for row in range(9):
        CONSTANT.lst.append([])
        for col in range(9):
            CONSTANT.lst[row].append([])
            if 1 <= random.randint(1, 101) <= 25 and CONSTANT.count_bombs < 12:
                CONSTANT.count_bombs += 1
                button = Button(game_frame, bg="grey", padx=10,
                                command=lambda row=row, col=col: check(row, col))
                CONSTANT.lst[row][col] = button_place(row, col,
                                                      True, button, "grey", 10)
                CONSTANT.lst[row][col].button.grid(row=row, column=col)
            else:
                button = Button(game_frame, bg="grey", padx=10,
                                command=lambda: check(row, col))
                CONSTANT.lst[row][col] = button_place(row, col, False,
                                                      button, "grey", 10)
                CONSTANT.lst[row][col].button.grid(row=row, column=col)

    mark_count = Label(mark_frame, text=f"Marker count: {CONSTANT.count_bombs}")
    mark_count.grid(row=0, column=0)
    space = Label(mark_frame, text="     ")
    space.grid(row=0, column=1)
    marker_button = Button(mark_frame, text="Mark", command=change_marker)
    marker_button.grid(row=0, column=2)

    for row in range(9):
        for col in range(9):
            if not CONSTANT.lst[row][col].bomb:
                CONSTANT.lst[row][col].number = find_bombs(row, col)

    while CONSTANT.flag:
        final_count = 0
        open_count = 0
        for classes_list in CONSTANT.lst:
            for button_class in classes_list:
                if button_class.color == "grey":
                    open_count += 1

        if open_count == 0:
            for classes_list in CONSTANT.lst:
                for button_class in classes_list:
                    if button_class.bomb and button_class.color == "red2":
                        final_count += 1

        if final_count == 12:
            massage = Label(end_frame, text="Congrats! You won!!!", bg="blue")
            massage.grid()
            CONSTANT.flag = False
        game_frame.update()

    time.sleep(CONSTANT.end_time)
    game_frame.update()


if __name__ == '__main__':
    root = Tk()
    game_frame = LabelFrame(root)
    game_frame.grid(row=0)
    mark_frame = LabelFrame(root)
    mark_frame.grid(row=1)
    end_frame = LabelFrame(root)
    end_frame.grid(row=2)
    main()
