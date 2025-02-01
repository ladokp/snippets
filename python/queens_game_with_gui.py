"""
Queen's Game: A puzzle game where the player moves a queen piece across the board to reach 
the goal while avoiding obstacles. The game features customizable board settings and a GUI.
"""

import random
import os
import tkinter as tk

# Default Constants
DEFAULT_BOARD_SIZE = 8  # Size of the chessboard
DEFAULT_NUMBER_OF_OBSTACLES = 20  # Number of obstacles
DEFAULT_INITIAL_SCORE = 100  # Starting score for the player

EMPTY = "."  # Empty cell representation
QUEEN = "Q"  # Queen's position representation
OBSTACLE = "#"  # Obstacle representation
GOAL = "G"  # Goal position representation

CELL_SIZE = 50  # Size of each cell in pixels


def clear_screen():
    """Clears the terminal screen based on the operating system."""
    os.system("cls" if os.name == "nt" else "clear")


def get_game_parameters():
    """Prompts the user to choose default or custom game parameters.

    Returns:
        tuple: Board size, number of obstacles, and initial score.
    """
    clear_screen()
    print("Welcome to the Queen's Game!")
    use_defaults = (
        input("Do you want to play with default parameters? (yes/no) [yes]: ")
        .strip()
        .lower()
        or "yes"
    )

    if use_defaults == "no":
        board_size = int(
            input(f"Enter board size (default {DEFAULT_BOARD_SIZE}): ")
            or DEFAULT_BOARD_SIZE
        )
        number_of_obstacles = int(
            input(
                f"Enter number of obstacles (default {DEFAULT_NUMBER_OF_OBSTACLES}): "
            )
            or DEFAULT_NUMBER_OF_OBSTACLES
        )
        initial_score = int(
            input(f"Enter initial score (default {DEFAULT_INITIAL_SCORE}): ")
            or DEFAULT_INITIAL_SCORE
        )
    else:
        board_size = DEFAULT_BOARD_SIZE
        number_of_obstacles = DEFAULT_NUMBER_OF_OBSTACLES
        initial_score = DEFAULT_INITIAL_SCORE

    return board_size, number_of_obstacles, initial_score


def create_board(board_size, number_of_obstacles):
    """Creates the game board with the queen, goal, and obstacles.

    Args:
        board_size (int): Size of the chessboard.
        number_of_obstacles (int): Number of obstacles to place.

    Returns:
        dict: The board, queen's initial position, goal position, and score.
    """
    board = [[EMPTY for _ in range(board_size)] for _ in range(board_size)]
    queen_position = (0, 0)
    goal_position = (board_size - 1, board_size - 1)
    score = DEFAULT_INITIAL_SCORE

    for _ in range(number_of_obstacles):
        x, y = random.randint(0, board_size - 1), random.randint(0, board_size - 1)
        if (x, y) != queen_position and (x, y) != goal_position:
            board[x][y] = OBSTACLE

    board[queen_position[0]][queen_position[1]] = QUEEN
    board[goal_position[0]][goal_position[1]] = GOAL

    return {
        "board": board,
        "queen_position": queen_position,
        "goal_position": goal_position,
        "score": score,
    }


class QueensGame:
    """Class to handle the Queen's Game logic and GUI."""

    def __init__(self, board_size, number_of_obstacles, initial_score):
        self.settings = {
            "board_size": board_size,
            "number_of_obstacles": number_of_obstacles,
            "initial_score": initial_score,
        }
        self.state = create_board(
            self.settings["board_size"], self.settings["number_of_obstacles"]
        )

        self.root = tk.Tk()
        self.root.title("Queen's Game")
        self.canvas_size = (
            max(self.settings["board_size"], self.settings["board_size"]) * CELL_SIZE
        )
        self.canvas = tk.Canvas(
            self.root, width=self.canvas_size, height=self.canvas_size + 50
        )
        self.canvas.pack()
        self.restart_button = tk.Button(
            self.root, text="Restart Game", command=self.restart_game
        )
        self.restart_button.pack()
        self.draw_board()
        self.root.mainloop()

    def restart_game(self):
        """Restarts the game with the same parameters."""
        self.state = create_board(
            self.settings["board_size"], self.settings["number_of_obstacles"]
        )
        self.draw_board()

    def draw_board(self):
        """Draws the board and updates the queen, goal, and obstacles."""
        self.canvas.delete("all")
        for i, row in enumerate(self.state["board"]):
            for j, cell in enumerate(row):
                x1, y1 = j * CELL_SIZE, i * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE

                color = "white"
                if cell == OBSTACLE:
                    color = "black"
                elif (i, j) == self.state["queen_position"]:
                    color = "blue"
                elif cell == GOAL:
                    color = "green"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

                if (i, j) == self.state["queen_position"]:
                    self.canvas.create_text(
                        (x1 + x2) // 2,
                        (y1 + y2) // 2,
                        text="Q",
                        fill="white",
                        font=("Arial", 14, "bold"),
                    )

    def on_click(self, event):
        """Handles click events to select and move the queen."""
        if self.state.get("game_over"):
            return

        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE

        new_pos = (row, col)
        if (row, col) == self.state["queen_position"]:
            self.state["selected"] = (row, col)
        else:
            if self.state.get("selected"):
                self.state["queen_position"] = new_pos
                self.state["score"] -= 1

                if self.state["score"] <= 0:
                    self.end_game("Game over! You ran out of points.")
                elif new_pos == self.state["goal_position"]:
                    self.end_game(
                        "Congratulations!"
                        f"You reached the goal with a score of {self.state['score']}."
                    )
        self.draw_board()

    def end_game(self, message):
        """Ends the game and displays the final message."""
        self.state["game_over"] = True
        self.draw_board()
        self.canvas.create_text(
            self.canvas_size // 2,
            self.canvas_size + 25,
            text=message,
            fill="red",
            font=("Arial", 10),
        )
        self.canvas.unbind("<Button-1>")


def play_game():
    """Initializes the game with user-defined or default parameters."""
    board_size, number_of_obstacles, initial_score = get_game_parameters()
    QueensGame(board_size, number_of_obstacles, initial_score)


if __name__ == "__main__":
    play_game()
