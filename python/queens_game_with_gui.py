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
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_game_parameters():
    clear_screen()
    print("Welcome to the Queen's Game!")
    use_defaults = input("Do you want to play with default parameters? (yes/no) [yes]: ").strip().lower() or "yes"

    if use_defaults == "no":
        board_size = int(input(f"Enter board size (default {DEFAULT_BOARD_SIZE}): ") or DEFAULT_BOARD_SIZE)
        number_of_obstacles = int(input(f"Enter number of obstacles (default {DEFAULT_NUMBER_OF_OBSTACLES}): ") or DEFAULT_NUMBER_OF_OBSTACLES)
        initial_score = int(input(f"Enter initial score (default {DEFAULT_INITIAL_SCORE}): ") or DEFAULT_INITIAL_SCORE)
    else:
        board_size = DEFAULT_BOARD_SIZE
        number_of_obstacles = DEFAULT_NUMBER_OF_OBSTACLES
        initial_score = DEFAULT_INITIAL_SCORE

    return board_size, number_of_obstacles, initial_score


def create_board(board_size, number_of_obstacles):
    board = [[EMPTY for _ in range(board_size)] for _ in range(board_size)]
    queen_position = (0, 0)
    goal_position = (board_size - 1, board_size - 1)

    for _ in range(number_of_obstacles):
        x, y = random.randint(0, board_size - 1), random.randint(0, board_size - 1)
        if (x, y) != queen_position and (x, y) != goal_position:
            board[x][y] = OBSTACLE

    board[queen_position[0]][queen_position[1]] = QUEEN
    board[goal_position[0]][goal_position[1]] = GOAL

    return board, queen_position, goal_position


def is_valid_path(board, start, end):
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
        if not (0 <= x < len(board) and 0 <= y < len(board[0])) or board[x][y] == OBSTACLE:
            return False

    return True


def move_queen(board, queen_pos, destination):
    x, y = queen_pos
    x_dest, y_dest = destination

    if is_valid_path(board, queen_pos, destination):
        board[x][y] = EMPTY
        board[x_dest][y_dest] = QUEEN
        return destination, True
    else:
        return queen_pos, False


class QueensGame:
    def __init__(self, board_size, number_of_obstacles, initial_score):
        self.board_size = board_size
        self.number_of_obstacles = number_of_obstacles
        self.initial_score = initial_score

        self.board, self.queen_pos, self.goal_pos = create_board(self.board_size, self.number_of_obstacles)
        self.score = self.initial_score
        self.selected = None
        self.game_over = False

        self.root = tk.Tk()
        self.root.title("Queen's Game")
        self.canvas_size = max(self.board_size, self.board_size) * CELL_SIZE
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size + 50)
        self.canvas.pack()
        self.restart_button = tk.Button(self.root, text="Restart Game", command=self.restart_game)
        self.restart_button.pack()
        self.draw_board()
        self.root.mainloop()

    def restart_game(self):
        self.board, self.queen_pos, self.goal_pos = create_board(self.board_size, self.number_of_obstacles)
        self.score = self.initial_score
        self.selected = None
        self.game_over = False

        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                x1, y1 = j * CELL_SIZE, i * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE

                color = "white"
                if self.board[i][j] == OBSTACLE:
                    color = "black"
                elif (i, j) == self.queen_pos:
                    color = "blue"
                elif self.board[i][j] == GOAL:
                    color = "green"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

                if (i, j) == self.queen_pos:
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="Q", fill="white", font=("Arial", 14, "bold"))

                if self.selected == (i, j) and not self.game_over:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=3)

    def on_click(self, event):
        if self.game_over:
            return

        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE

        if self.selected:
            new_pos = (row, col)
            original_pos = self.queen_pos
            self.queen_pos, moved = move_queen(self.board, self.queen_pos, new_pos)

            if moved:
                distance = max(abs(new_pos[0] - original_pos[0]), abs(new_pos[1] - original_pos[1]))
                self.score -= distance
                if self.score <= 0:
                    self.end_game("Game over! You ran out of points.")
                    return
                if self.queen_pos == self.goal_pos:
                    self.end_game(f"Congratulations! You've reached the goal with a score of {self.score}.")
                    return
            self.selected = None
        else:
            if (row, col) == self.queen_pos:
                self.selected = (row, col)

        self.draw_board()

    def end_game(self, message):
        self.game_over = True
        self.queen_pos = self.goal_pos
        self.draw_board()
        self.canvas.create_rectangle(0, len(self.board) * CELL_SIZE, len(self.board[0]) * CELL_SIZE, len(self.board) * CELL_SIZE + 50, fill="white")
        self.canvas.create_text(
            len(self.board[0]) * CELL_SIZE // 2,
            len(self.board) * CELL_SIZE + 25,
            text=message,
            fill="red",
            font=("Arial", 10)
        )
        self.canvas.unbind("<Button-1>")


def play_game():
    board_size, number_of_obstacles, initial_score = get_game_parameters()
    QueensGame(board_size, number_of_obstacles, initial_score)


if __name__ == "__main__":
    play_game()
