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
    - rules(): Display the rules of the game.
"""

import tkinter as tk  # Importing the tkinter library for GUI
import engine  # Importing the game engine module
from pathlib import Path  # Importing pathlib module for handling file paths
from engine import (
    color_cells,
    color_font,
    font_format,
    root,
)  # Importing specific variables from the engine module

root.configure(bg="#CDC1B5")  # Configuring the root window background color
root.title("2048")  # Setting the title of the window
root.resizable(False, False)  # Making the window non-resizable

# Path to the icon file
ICON_FILE = Path("icon.png")

# Checking if the icon file exists
if ICON_FILE.exists():
    # Loading the icon into a PhotoImage object
    icon = tk.PhotoImage(file="icon.png")
    # Setting the icon for the main window and all its associated windows
    root.iconphoto(True, icon)

# Creating frames for game information and the game board
info_frame = tk.Frame(root, bg="#CDC1B5")  # Frame for game information
game_frame = tk.Frame(root, borderwidth=5, bg="#766F65")  # Frame for the game board
info_frame.pack(fill=tk.X)  # Packing the information frame
game_frame.pack()  # Packing the game frame
info_frame.grid_columnconfigure(0, minsize=200)
info_frame.grid_columnconfigure(1, minsize=320)


def rules():
    """
    Display the rules of the game.

    Creates a new window displaying the rules of the 2048 game.

    Returns:
        None
    """
    rules_window = tk.Toplevel(root, bg="#EEDFC8")
    rules_window.geometry("800x200")
    rules_window.title("2048 - Rules")
    rules_window.resizable(False, False)
    text_rules = tk.Text(
        rules_window, font=("Arial", 16, "bold"), bg="#EEDFC8", fg="#766F65"
    )
    text_rules.insert(
        tk.INSERT,
        "A 4x4 grid is generated with two randomly placed tiles "
        "(with a value of 2 or 4).\n \n"
        "Use your arrow keys to move the tiles.\n \n"
        "Tiles with the same number merge into one when they touch.\n"
        "A new tile appears randomly with each valid move.\n"
        "Try to reach 2048!",
    )
    text_rules.config(state=tk.DISABLED)
    text_rules.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


# Creating a menu bar
menubar = tk.Menu(root)  # Menu bar
root.config(menu=menubar)  # Configuring the root window with the menu
menu_option = tk.Menu(menubar, tearoff=False)  # Options dropdown menu
menubar.add_cascade(
    label="Options", menu=menu_option
)  # Adding the options dropdown to the menu bar
# Adding options to the dropdown menu
menu_option.add_command(
    label="New Game", command=lambda: engine.newgame(labels, label_points)
)
menu_option.add_command(
    label="Reset Highscore", command=lambda: engine.reset_leaderboard(label_highscore)
)
menu_option.add_separator()  # Adding a separator between options
menu_option.add_command(label="Rules", command=rules)

menu_option.add_separator()  # Adding a separator between options
menu_option.add_command(label="Quit game", command=root.quit)

# Label for displaying points
label_points = tk.Label(
    info_frame,
    font=("Franklin Gothic Book", 20),
    text=f"SCORE \n {engine.points}",
    bg="#766F65",
    fg="white",
)
label_points.grid(row=0, padx=10, pady=5, sticky=tk.EW)

# Label for displaying highscore
label_highscore = tk.Label(
    info_frame,
    font=("Franklin Gothic Book", 20),
    text=f"BEST \n {engine.highscore}",
    bg="#766F65",
    fg="white",
)
label_highscore.grid(row=1, padx=10, pady=5, column=0, sticky=tk.EW)

label_gamename = tk.Label(
    info_frame,
    font=("Franklin Gothic Book", 40),
    text="   2048   ",
    bg="#EDC12D",
    fg="white",
)
label_gamename.grid(row=0, column=1, padx=10, pady=5, sticky=tk.E)

# Configuring columns for the game board
for i in range(4):
    game_frame.columnconfigure(i, minsize=130)
    game_frame.rowconfigure(i, minsize=130)

label_texts = engine.gameboard  # Getting the initial game board
# Creating labels for each cell in the game board
labels = [
    [
        tk.Label(
            game_frame,
            text=label_texts[i][j],
            font=font_format[label_texts[i][j]],
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
