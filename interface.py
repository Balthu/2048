"""
2048 Game GUI Module

This module sets up the graphical user interface (GUI) for the 2048 game using the Tkinter library.

Dependencies:
    - tkinter: The standard GUI library for Python.
    - engine: The game engine module containing game logic.

Variables:
    - root: The main Tkinter window.
    - color_cells: Dictionary mapping cell values to background colors.
    - color_font: Dictionary mapping cell values to font colors.

Functions:
    - newgame(labels, label_points): Starts a new game.
    - reset_leaderboard(label_highscore): Resets the high score to 0.
    - position(position_user: str, tab: list, score: int, labels, points_label, label_highscore):
        Updates the game board and score based on the user's move.
"""

import tkinter as tk  # Importing the tkinter library for GUI
import engine  # Importing the game engine module
from engine import (
    color_cells,
    color_font,
    root,
)  # Importing specific variables from the engine module

root.configure(bg="#CDC1B5")  # Configuring the root window background color
root.title("2048")  # Setting the title of the window
root.resizable(False, False)  # Making the window non-resizable

# Creating frames for game information and the game board
info_frame = tk.Frame(root, bg="#CDC1B5")  # Frame for game information
game_frame = tk.Frame(root, borderwidth=5, bg="#766F65")  # Frame for the game board
info_frame.pack()  # Packing the information frame
game_frame.pack()  # Packing the game frame

# Creating a menu bar
menubar = tk.Menu(root)  # Menu bar
root.config(menu=menubar)  # Configuring the root window with the menu
menu_option = tk.Menu(menubar, tearoff=False)  # Options dropdown menu
menubar.add_cascade(
    label="Options", menu=menu_option
)  # Adding the options dropdown to the menu bar
# Adding options to the dropdown menu
menu_option.add_command(
    label="New game", command=lambda: engine.newgame(labels, label_points)
)
menu_option.add_command(
    label="Erase highscore", command=lambda: engine.reset_leaderboard(label_highscore)
)
menu_option.add_separator()  # Adding a separator between options
menu_option.add_command(label="Quit game", command=root.quit)

# Configuring columns for the game board
for i in range(4):
    game_frame.columnconfigure(i, minsize=120)

label_texts = engine.gameboard  # Getting the initial game board
# Creating labels for each cell in the game board
labels = [
    [
        tk.Label(
            game_frame,
            text=label_texts[i][j],
            font=("Arial", 50),
            bg=color_cells[label_texts[i][j]],
            fg=color_font[label_texts[i][j]],
            borderwidth=2,
            relief=tk.SOLID,
        )
        for j in range(4)
    ]
    for i in range(4)
]
# Placing labels in the grid
for i in range(4):
    for j in range(4):
        labels[i][j].grid(row=i, column=j, padx=1, pady=1, sticky=tk.NSEW)

# Label for displaying points
label_points = tk.Label(
    info_frame,
    font=("Franklin Gothic Book", 20),
    text=f"Points : {engine.points}",
    bg="#766F65",
    fg="white",
)
label_points.pack(pady=5)

# Label for displaying highscore
label_highscore = tk.Label(
    info_frame,
    font=("Franklin Gothic Book", 20),
    text=f"BEST : {engine.highscore}",
    bg="#766F65",
    fg="white",
)
label_highscore.pack(pady=5)

# Binding keyboard keys to movement functions
root.bind(
    "<Left>",
    lambda event: engine.position(
        "LEFT", engine.gameboard, engine.points, labels, label_points, label_highscore
    ),
)
root.bind(
    "<Right>",
    lambda event: engine.position(
        "RIGHT", engine.gameboard, engine.points, labels, label_points, label_highscore
    ),
)
root.bind(
    "<Down>",
    lambda event: engine.position(
        "DOWN", engine.gameboard, engine.points, labels, label_points, label_highscore
    ),
)
root.bind(
    "<Up>",
    lambda event: engine.position(
        "UP", engine.gameboard, engine.points, labels, label_points, label_highscore
    ),
)

if __name__ == "__main__":
    root.mainloop()  # Running the main event loop
