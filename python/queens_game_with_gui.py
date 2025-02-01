"""
Queen's Game Module

This module implements a puzzle game where the player moves a queen across the board
to reach the goal while avoiding obstacles. The game includes customizable board settings
and a graphical interface.
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

PROTECTED_CELLS = {
    (0, 0),
    (0, 1),
    (1, 0),
    (1, 1),
    (7, 7),
}  # Cells that should never contain obstacles


def clear_screen():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def get_game_parameters():
    """Prompts the player to choose default or custom game parameters."""
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
    """Creates the game board with obstacles, queen, and goal positions."""
    board = [[EMPTY for _ in range(board_size)] for _ in range(board_size)]
    queen_position = (0, 0)
    goal_position = (board_size - 1, board_size - 1)

    obstacles_added = 0
    while obstacles_added < number_of_obstacles:
        x, y = random.randint(0, board_size - 1), random.randint(0, board_size - 1)
        if (x, y) not in PROTECTED_CELLS and board[x][y] == EMPTY:
            board[x][y] = OBSTACLE
            obstacles_added += 1

    board[queen_position[0]][queen_position[1]] = QUEEN
    board[goal_position[0]][goal_position[1]] = GOAL

    return board, queen_position, goal_position


def is_valid_path(board, start, end):
    """Checks if the queen's movement from start to end is valid."""
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    if not (dx == 0 or dy == 0 or abs(dx) == abs(dy)):
        return False

    step_x = (dx // abs(dx)) if dx != 0 else 0
    step_y = (dy // abs(dy)) if dy != 0 else 0

    x, y = x1, y1
    while (x, y) != (x2, y2):
        x += step_x
        y += step_y
        if (
            not (0 <= x < len(board) and 0 <= y < len(board[0]))
            or board[x][y] == OBSTACLE
        ):
            return False

    return True


def move_queen(board, queen_pos, destination):
    """Moves the queen to a new position if the path is valid."""
    x, y = queen_pos
    x_dest, y_dest = destination

    if is_valid_path(board, queen_pos, destination):
        board[x][y] = EMPTY
        board[x_dest][y_dest] = QUEEN
        return destination, True

    return queen_pos, False


class QueensGame:
    """Handles the game logic and GUI for the Queen's Game."""

    def __init__(self, board, queen_pos, goal_pos, score):
        self.board = board
        self.queen_pos = queen_pos
        self.goal_pos = goal_pos
        self.score = score
        self.selected = None
        self.game_over = False

        self.root = tk.Tk()
        self.root.title("Queen's Game")

        canvas_size = max(len(board), len(board[0])) * CELL_SIZE
        self.canvas = tk.Canvas(self.root, width=canvas_size, height=canvas_size + 50)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.restart_button = tk.Button(
            self.root, text="Restart Game", command=self.restart_game
        )
        self.restart_button.pack()

        self.draw_board()
        self.root.mainloop()

    def draw_board(self):
        """Draws the game board with current state of the queen and obstacles."""
        self.canvas.delete("all")
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                x1, y1 = j * CELL_SIZE, i * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE

                color = "white"
                if cell == OBSTACLE:
                    color = "black"
                elif (i, j) == self.queen_pos:
                    color = "blue"
                elif cell == GOAL:
                    color = "green"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

                if (i, j) == self.queen_pos:
                    self.canvas.create_text(
                        (x1 + x2) // 2,
                        (y1 + y2) // 2,
                        text="Q",
                        fill="white",
                        font=("Arial", 14, "bold"),
                    )

                if self.selected == (i, j) and not self.game_over:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=3)

    def on_click(self, event):
        """Handles mouse click events to select and move the queen."""
        if self.game_over:
            return

        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE

        if self.selected:
            new_pos = (row, col)
            original_pos = self.queen_pos
            self.queen_pos, moved = move_queen(self.board, self.queen_pos, new_pos)

            if moved:
                distance = max(
                    abs(new_pos[0] - original_pos[0]), abs(new_pos[1] - original_pos[1])
                )
                self.score -= distance
                if self.score <= 0:
                    self.end_game("Game over! You ran out of points.")
                    return
                if self.queen_pos == self.goal_pos:
                    self.end_game(
                        f"Congratulations! You've reached the goal with a score of {self.score}."
                    )
                    return
            self.selected = None
        elif (row, col) == self.queen_pos:
            self.selected = (row, col)

        self.draw_board()

    def end_game(self, message):
        """Handles game over conditions and displays the final message."""
        self.game_over = True
        self.queen_pos = self.goal_pos
        self.draw_board()
        self.canvas.create_rectangle(
            0,
            len(self.board) * CELL_SIZE,
            len(self.board[0]) * CELL_SIZE,
            len(self.board) * CELL_SIZE + 50,
            fill="white",
        )
        self.canvas.create_text(
            len(self.board[0]) * CELL_SIZE // 2,
            len(self.board) * CELL_SIZE + 25,
            text=message,
            fill="red",
            font=("Arial", 10),
        )
        self.canvas.unbind("<Button-1>")

    def restart_game(self):
        """Restarts the game with the same or new parameters."""
        board_size, number_of_obstacles, initial_score = get_game_parameters()
        self.board, self.queen_pos, self.goal_pos = create_board(
            board_size, number_of_obstacles
        )
        self.score = initial_score
        self.selected = None
        self.game_over = False
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()


def play_game():
    """Starts the Queen's Game."""
    board_size, number_of_obstacles, initial_score = get_game_parameters()
    board, queen_pos, goal_pos = create_board(board_size, number_of_obstacles)
    QueensGame(board, queen_pos, goal_pos, initial_score)


if __name__ == "__main__":
    play_game()
