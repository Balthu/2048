"""
This module implements a simple 2048 game using Tkinter for the GUI.

Dependencies:
    - random.randint: Used to generate random numbers for initializing the game board and adding new tiles.
    - random.choice: Used to choose between adding a "2" or "4" when adding a new tile.
    - tkinter.messagebox: Used to display message boxes for game over and new game prompts.
    - copy.deepcopy: Used to create a deep copy of the game board to check for changes.
    - tkinter: Used for creating the graphical user interface.
    - json: Used for handling leaderboard data storage and retrieval.
    - pygame: Used for playing sound effects during the game.
    - pathlib.Path: Used for defining the path to the leaderboard file.

Variables:
    - LEADERBOARD (Path): Path object representing the location of the leaderboard file.

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
    gameboard = [[0 for _ in range(4)] for _ in range(4)]
    # Generate random positions for two initial values
    random_position = [randint(0, 3) for _ in range(4)]
    # Ensure the two random positions are not the same
    while random_position[0:2] == random_position[2:4]:
        random_position[2:4] = randint(0, 3), randint(0, 3)
    # Place two random values (either 2 or 4) at the generated positions
    gameboard[random_position[0]][random_position[1]] = choice((2, 4))
    gameboard[random_position[2]][random_position[3]] = choice((2, 4))
    return gameboard


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
        for j in range(2, -1, -1):
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
    for i in range(2, -1, -1):
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
    update_points(points_label, points)
    update_top_score(label_highscore, points)
    if check_endgame(gameboard):
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
    global victory_count

    if any(2048 in element for element in tab) and victory_count == 0:
        victory_count = 1
        winner_window = tk.Toplevel(root, bg="#EEDFC8")
        winner_window.geometry("400x100")
        winner_window.title("2048 - You win !")
        winner_window.resizable(False, False)
        winner_label = tk.Label(
            winner_window,
            text="You've reached 2048 ! \n Congratulations!",
            font=("Arial", 20, "bold"),
            bg="#EEDFC8",
            fg="#766F65",
        )
        winner_label.pack(padx=5, pady=15)
        try:
            pygame.mixer.music.load("fanfare.mp3")
            pygame.mixer.music.play()
        except pygame.error:
            pass

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
    global gameboard, points, victory_count
    try:
        pygame.mixer.music.load("notif.mp3")
        pygame.mixer.music.play()
    except pygame.error:
        pass
    answer = messagebox.askyesno("Game over", "Do you want to start a new game?")
    if answer:
        gameboard = initialisation()
        points = 0
        victory_count = 0
        update_gameboard_labels(labels)
        update_points(labels_point, 0)


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
                font=font_format[gameboard[i][j]],
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
    points_label.config(text=f"SCORE \n {score}")


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
        label_highscore.config(text=f"BEST \n {max(scores)}")
        with open(LEADERBOARD, "w", encoding="utf-8") as f:
            json.dump(scores, f)
    else:
        label_highscore.config(text=f"BEST {points}")


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
    "#EDC850",
    "#EDC542",
    "#EDC12D",
    "#EF666D",
    "#EE4E5A",
    "#E14338",
    "#73B3D6",
    "#5CA0DF",
    "#007BBE",
]

color_cells = {0: colorset_cells[0]}

for i in range(1, 18):
    color_cells[2**i] = colorset_cells[i]

colorset_font = ["#CDC1B5", "#766F65", "white"]
color_font = {0: colorset_font[0]}
for i in range(1, 18):
    if i < 3:
        color_font[2**i] = colorset_font[1]
    else:
        color_font[2**i] = colorset_font[2]

fontset = [("Arial", 50), ("Arial", 38), ("Arial", 27)]
font_format = {0: fontset[0]}
for i in range(1, 18):
    if i < 10:
        font_format[2**i] = fontset[0]
    elif i < 14:
        font_format[2**i] = fontset[1]
    else:
        font_format[2**i] = fontset[2]

# Initialize the game board, points and victory count
gameboard = initialisation()
points = 0
victory_count = 0

# Retrieve the top score
highscore = top_score()
