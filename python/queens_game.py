import random
import os

# Default Constants
DEFAULT_BOARD_SIZE = 8  # Size of the chessboard
DEFAULT_NUMBER_OF_OBSTACLES = 20  # Number of obstacles
DEFAULT_INITIAL_SCORE = 100  # Starting score for the player

EMPTY = "."  # Empty cell representation
QUEEN = "Q"  # Queen's position representation
OBSTACLE = "#"  # Obstacle representation
GOAL = "G"  # Goal position representation


def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_game_parameters():
    """
    Asks the player if they want to use default game parameters or customize them.

    Returns:
        board_size (int): Size of the chessboard.
        number_of_obstacles (int): Number of obstacles.
        initial_score (int): Starting score.
    """
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
    """
    Creates and initializes the game board.

    Args:
        board_size (int): Size of the chessboard.
        number_of_obstacles (int): Number of obstacles to place.

    Returns:
        board (list): 2D list representing the board.
        queen_position (tuple): Initial position of the queen.
        goal_position (tuple): Position of the goal.
    """
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


def print_board(board):
    """
    Prints the current state of the game board with coordinate descriptions.

    Args:
        board (list): 2D list representing the board.
    """
    clear_screen()
    print("   " + " ".join(f"{i}" for i in range(len(board[0]))))
    for i, row in enumerate(board):
        print(f"{i:2} " + " ".join(row))


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
        print("Invalid move! Path is blocked or invalid.")
        return queen_pos, False


def play_game():
    board_size, number_of_obstacles, initial_score = get_game_parameters()

    while True:
        board, queen_pos, goal_pos = create_board(board_size, number_of_obstacles)
        score = initial_score

        print("Reach the goal with the highest score possible!")
        print_board(board)

        while True:
            print(f"Queen's position: {queen_pos}")
            print(f"Score: {score}")
            try:
                x_dest = int(input(f"Enter destination row (0-{board_size - 1}): "))
                y_dest = int(input(f"Enter destination column (0-{board_size - 1}): "))
            except ValueError:
                print("Invalid input! Coordinates must be integers within the board limits.")
                continue

            if not (0 <= x_dest < board_size and 0 <= y_dest < board_size):
                print("Invalid coordinates! Out of bounds.")
                continue

            destination = (x_dest, y_dest)
            original_position = queen_pos
            queen_pos, moved = move_queen(board, queen_pos, destination)

            if moved:
                distance = max(abs(x_dest - original_position[0]), abs(y_dest - original_position[1]))
                score -= distance
                print_board(board)

            if score <= 0:
                print("Game over! You ran out of points.")
                break

            if queen_pos == goal_pos:
                print(f"Congratulations! You've reached the goal with a score of {score}.")
                break

        play_again = input("Do you want to start a new game? (yes/no) [no]: ").strip().lower() or "no"
        if play_again != "yes":
            print("Thank you for playing the Queen's Game! Goodbye!")
            break


if __name__ == "__main__":
    play_game()
