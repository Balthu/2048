"""
This module implements a simple 2048 game using Tkinter for the GUI.

Functions:
    - initialisation() -> list: Creates a 4x4 array initialized with zeros and places two random values in the array.
    - move_up(tab: list) -> list: Moves values upwards in the array.
    - merge_up(tab: list, score: int) -> [list, int]: Merges identical values upwards in the array
    and updates the score.
    - move_down(tab: list) -> list: Moves values downwards in the array.
    - merge_down(tab: list, score: int) -> [list, int]: Merges identical values downwards in the array
    and updates the score.
    - move_right(tab: list) -> list: Moves values to the right in the array.
    - merge_right(tab: list, score: int) -> [list, int]: Merges identical values to the right in the array
    and updates the score.
    - move_left(tab: list) -> list: Moves values to the left in the array.
    - merge_left(tab: list, score: int) -> [list, int]: Merges identical values to the left in the array
    and updates the score.
    - position(position_user: str, tab: list, score: int, labels, points_label, label_highscore) :
    Executes the chosen move by the user and updates the game state.
    - add_two(tab: list) -> list: Adds a random "2" or "4" in an empty cell of the array.
    - check_endgame(tab: list) -> bool: Checks if the game is over.
    - newgame(labels, labels_point): Starts a new game if the user chooses to continue.
    - update_gameboard_labels(labels): Updates the GUI with the current game state.
    - update_points(points_label, score): Updates the points label with the current score.
    - update_top_score(label_highscore, points: int): Updates the top score label with the current score.
    - top_score() -> int: Retrieves the top score from the leaderboard file.
    - reset_leaderboard(label_highscore): Resets the leaderboard file.
    - easy_mode(): Displays a surprise message.
"""

from random import randint, choice
from tkinter import messagebox
import copy
import tkinter as tk
import json
import pygame
from pathlib import Path

# Initialize pygame
pygame.init()

# Define the path to the leaderboard file
LEADERBOARD = Path("leaderboard.json")


def initialisation() -> list:
    """
    Creates a new game board and initializes it with two random values.

    Returns:
        list: A 4x4 array representing the game board.
    """
    # Create a 4x4 array initialized with zeros
    gameboard_array = [[0 for _ in range(4)] for _ in range(4)]
    # Generate random positions for two initial values
    random_value = [randint(0, 3) for _ in range(4)]
    # Ensure the two random positions are not the same
    while (random_value[0], random_value[1]) == (random_value[2], random_value[3]):
        random_value[2] = randint(0, 3)
        random_value[3] = randint(0, 3)
    # Place two random values (either 2 or 4) at the generated positions
    gameboard_array[random_value[0]][random_value[1]] = choice((2, 4))
    gameboard_array[random_value[2]][random_value[3]] = choice((2, 4))
    return gameboard_array


def move_right(tab: list) -> list:
    """
    Moves values to the right in the array.

    Args:
        tab (list): The game board.

    Returns:
        list: The updated game board after moving values to the right.
    """
    for row in tab:
        while 0 in row:
            row.remove(0)
        for i in range(4 - len(row)):
            row.insert(0, 0)

    return tab


def merge_right(tab: list, score: int) -> [list, int]:
    """
    Merges identical values to the right in the array and updates the score.

    Args:
        tab (list): The game board.
        score (int): The current score.

    Returns:
        [list, int]: The updated game board and the updated score.
    """
    for i in range(4):
        for j in range(3):
            if tab[i][j + 1] == tab[i][j]:
                tab[i][j] = 0
                tab[i][j + 1] *= 2
                score = score + tab[i][j + 1]
    return tab, score


def move_left(tab: list) -> list:
    """
    Moves values to the left in the array.

    Args:
        tab (list): The game board.

    Returns:
        list: The updated game board after moving values to the left.
    """
    for row in tab:
        while 0 in row:
            row.remove(0)
        for i in range(4 - len(row)):
            row.append(0)

    return tab


def merge_left(tab: list, score: int) -> [list, int]:
    """
    Merges identical values to the left in the array and updates the score.

    Args:
        tab (list): The game board.
        score (int): The current score.

    Returns:
        [list, int]: The updated game board and the updated score.
    """
    for i in range(4):
        for j in range(1, 4):
            if tab[i][j - 1] == tab[i][j]:
                tab[i][j] = 0
                tab[i][j - 1] *= 2
                score = score + tab[i][j - 1]

    return tab, score


def move_up(tab: list) -> list:
    """
    Moves values upwards in the array.

    Args:
        tab (list): The game board.

    Returns:
        list: The updated game board after moving values upwards.
    """
    for j in range(4):
        column = [tab[i][j] for i in range(4)]
        while 0 in column:
            column.remove(0)
        for i in range(4 - len(column)):
            column.append(0)

        for i in range(4):
            tab[i][j] = column[i]
    return tab


def merge_up(tab: list, score: int) -> [list, int]:
    """
    Merges identical values upwards in the array and updates the score.

    Args:
        tab (list): The game board.
        score (int): The current score.

    Returns:
        [list, int]: The updated game board and the updated score.
    """
    for i in range(1, 4):
        for j in range(4):
            if tab[i - 1][j] == tab[i][j]:
                tab[i][j] = 0
                tab[i - 1][j] *= 2
                score = score + tab[i - 1][j]

    return tab, score


def move_down(tab: list) -> list:
    """
    Moves values downwards in the array.

    Args:
        tab (list): The game board.

    Returns:
        list: The updated game board after moving values downwards.
    """
    for j in range(4):
        column = [tab[i][j] for i in range(4)]
        while 0 in column:
            column.remove(0)
        for i in range(4 - len(column)):
            column.insert(0, 0)

        for i in range(4):
            tab[i][j] = column[i]
    return tab


def merge_down(tab: list, score: int) -> [list, int]:
    """
    Merges identical values downwards in the array and updates the score.

    Args:
        tab (list): The game board.
        score (int): The current score.

    Returns:
        [list, int]: The updated game board and the updated score.
    """
    for i in range(3):
        for j in range(4):
            if tab[i + 1][j] == tab[i][j]:
                tab[i][j] = 0
                tab[i + 1][j] *= 2
                score = score + tab[i + 1][j]

    return tab, score


def position(
        position_user: str, tab: list, score: int, labels, points_label, label_highscore
):
    """
    Executes the chosen move by the user and updates the game state.

    Args:
        position_user (str): The chosen move direction ("UP", "DOWN", "LEFT", or "RIGHT").
        tab (list): The game board.
        score (int): The current score.
        labels: Labels representing the game board in the GUI.
        points_label: Label displaying the current score in the GUI.
        label_highscore: Label displaying the high score in the GUI.
    """
    global points, gameboard
    check_board = copy.deepcopy(tab)

    # Move tiles and merge identical tiles based on the chosen direction
    if position_user == "UP":
        tab = move_up(tab)
        tab, score = merge_up(tab, score)
        tab = move_up(tab)
    elif position_user == "DOWN":
        tab = move_down(tab)
        tab, score = merge_down(tab, score)
        tab = move_down(tab)
    elif position_user == "LEFT":
        tab = move_left(tab)
        tab, score = merge_left(tab, score)
        tab = move_left(tab)
    else:
        tab = move_right(tab)
        tab, score = merge_right(tab, score)
        tab = move_right(tab)

    # If the board changes after the move, add a new tile
    if check_board != tab:
        tab = add_two(tab)
    points = score
    gameboard = tab
    update_gameboard_labels(labels)
    update_points(points_label, score)
    update_top_score(label_highscore, points)
    if check_endgame(tab):
        newgame(labels, points_label)


def add_two(tab: list) -> list:
    """
    Adds a random "2" or "4" in an empty cell of the array.

    Args:
        tab (list): The game board.

    Returns:
        list: The updated game board after adding a random value.
    """
    empty_cells = [(i, j) for i in range(4) for j in range(4) if tab[i][j] == 0]
    if empty_cells:
        row, column = choice(empty_cells)
        tab[row][column] = choice((2, 4))
    try:
        pygame.mixer.music.load("move.mp3")
        pygame.mixer.music.play()
    except pygame.error:
        pass
    return tab


def check_endgame(tab: list) -> bool:
    """
    Checks if the game is over.

    Args:
        tab (list): The game board.

    Returns:
        bool: True if the game is over, False otherwise.
    """
    if any(0 in element for element in tab):
        return False

    for i in range(4):
        for j in range(3):
            if tab[i][j] == tab[i][j + 1]:
                return False

    for i in range(3):
        for j in range(4):
            if tab[i][j] == tab[i + 1][j]:
                return False

    return True


def newgame(labels, labels_point):
    """
    Starts a new game if the user chooses to continue.

    Args:
        labels: Labels representing the game board in the GUI.
        labels_point: Label displaying the current score in the GUI.
    """
    global gameboard, points
    try:
        pygame.mixer.music.load("notif.mp3")
        pygame.mixer.music.play()
    except pygame.error:
        pass
    answer = messagebox.askyesno("Game over", "Do you want to start a new game? ?")
    if answer:
        gameboard = initialisation()
        points = 0
        update_gameboard_labels(labels)
        update_points(labels_point, 0)
    else:
        root.quit()


def update_gameboard_labels(labels):
    """
    Updates the GUI with the current game state.

    Args:
        labels: Labels representing the game board in the GUI.
    """
    for i in range(4):
        for j in range(4):
            labels[i][j].config(
                text=str(gameboard[i][j]),
                bg=color_cells[gameboard[i][j]],
                fg=color_font[gameboard[i][j]],
            )


def update_points(points_label, score):
    """
    Updates the points label with the current score.

    Args:
        points_label: Label displaying the current score in the GUI.
        score (int): The current score.
    """
    points_label.config(text=f"Points : {score}")


def update_top_score(label_highscore, points: int):
    """
    Updates the top score label with the current score.

    Args:
        label_highscore: Label displaying the high score in the GUI.
        points (int): The current score.
    """
    if LEADERBOARD.exists():
        with open(LEADERBOARD, "r", encoding="utf-8") as f:
            scores = json.load(f)

        scores.append(points)
        scores.sort(reverse=True)
        scores = scores[:2]
        label_highscore.config(text=f"BEST : {max(scores)}")
        with open(LEADERBOARD, "w", encoding="utf-8") as f:
            json.dump(scores, f)
    else:
        label_highscore.config(text=f"BEST : {points}")


def top_score() -> int:
    """
    Retrieves the top score from the leaderboard file.

    Returns:
        int: The top score.
    """
    if LEADERBOARD.exists():
        with open(LEADERBOARD, "r", encoding="utf-8") as f:
            scores = json.load(f)
        if len(scores) == 0:
            scores.append(0)
        return max(scores)
    else:
        return points


def reset_leaderboard(label_highscore):
    """
    Resets the leaderboard file.

    Args:
        label_highscore: Label displaying the high score in the GUI.
    """
    scores = [0]
    if LEADERBOARD.exists():
        with open(LEADERBOARD, "w", encoding="utf-8") as f:
            json.dump(scores, f)

    update_top_score(label_highscore, 0)


# Initialize the Tkinter window
root = tk.Tk()

# Define color schemes for the game board cells and fonts
colorset_cells = [
    "#CDC1B5",
    "#EEE4DA",
    "#EEDFC8",
    "#F2B179",
    "#F59563",
    "#F67C60",
    "#F65E3B",
    "#F65E3B",
    "#EDCC62",
]

for i in range(9):
    if i <= 2:
        colorset_cells.append("#EDC850")
    else:
        colorset_cells.append("#3D3A33")

color_cells = {}

for i in range(18):
    if i != 0:
        color_cells[2 ** i] = colorset_cells[i]
    else:
        # rappel 2 ^ 0 = 1
        color_cells[0] = colorset_cells[i]

colorset_font = ["#CDC1B5", "#766F65", "white"]
color_font = {}
for i in range(18):
    if i == 0:
        color_font[0] = colorset_font[0]
    elif i < 3:
        color_font[2 ** i] = colorset_font[1]
    else:
        color_font[2 ** i] = colorset_font[2]

# Initialize the game board and score
gameboard = initialisation()
points = 0

# Retrieve the top score
highscore = top_score()
