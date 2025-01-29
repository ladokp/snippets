import random
import os

# Constants
BOARD_SIZE = 8  # Size of the chessboard
EMPTY = "."  # Empty cell representation
QUEEN = "Q"  # Queen's position representation
OBSTACLE = "#"  # Obstacle representation
NUMBER_IF_OBSTACLES = 20 # Number of obstacles
GOAL = "G"  # Goal position representation
INITIAL_SCORE = 100  # Starting score for the player


def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def create_board():
    """
    Creates and initializes the game board.

    Returns:
        board (list): 2D list representing the board.
        queen_position (tuple): Initial position of the queen.
        goal_position (tuple): Position of the goal.
    """
    # Create an empty board
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    queen_position = (0, 0)  # Queen starts at the top-left corner
    goal_position = (BOARD_SIZE - 1, BOARD_SIZE - 1)  # Goal at bottom-right corner

    # Place random obstacles on the board
    for _ in range(NUMBER_IF_OBSTACLES):
        x, y = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
        if (x, y) != queen_position and (x, y) != goal_position:
            board[x][y] = OBSTACLE

    # Place the queen and the goal
    board[queen_position[0]][queen_position[1]] = QUEEN
    board[goal_position[0]][goal_position[1]] = GOAL

    return board, queen_position, goal_position


def print_board(board, clear=False):
    """
    Prints the current state of the game board with coordinate descriptions.

    Args:
        board (list): 2D list representing the board.
        clear (bool): Whether to clear the screen before printing.
    """
    if clear:
        clear_screen()

    # Print column headers with proper alignment
    print("   " + " ".join(f"{i}" for i in range(BOARD_SIZE)))

    for i, row in enumerate(board):
        # Print row number with alignment
        print(f"{i:2} " + " ".join(row))


def is_valid_path(board, start, end):
    """
    Checks if the path between the start and end positions is valid.

    Args:
        board (list): 2D list representing the board.
        start (tuple): Starting position (row, column).
        end (tuple): Ending position (row, column).

    Returns:
        bool: True if the path is valid, False otherwise.
    """
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Ensure movement is in a straight line or diagonal
    if not (dx == 0 or dy == 0 or abs(dx) == abs(dy)):
        return False

    # Normalize movement direction
    step_x = (dx // abs(dx)) if dx != 0 else 0
    step_y = (dy // abs(dy)) if dy != 0 else 0

    # Check each square along the path for obstacles or out-of-bounds
    x, y = x1, y1
    while (x, y) != (x2, y2):
        x += step_x
        y += step_y
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE) or board[x][y] == OBSTACLE:
            return False

    return True


def move_queen(board, queen_pos, destination):
    """
    Moves the queen to the specified destination if the path is valid.

    Args:
        board (list): 2D list representing the board.
        queen_pos (tuple): Current position of the queen (row, column).
        destination (tuple): Desired destination (row, column).

    Returns:
        tuple: New position of the queen and a boolean indicating if the move was successful.
    """
    x, y = queen_pos
    x_dest, y_dest = destination

    # Check if the path to the destination is valid
    if is_valid_path(board, queen_pos, destination):
        board[x][y] = EMPTY  # Clear the current queen position
        board[x_dest][y_dest] = QUEEN  # Place the queen at the destination
        return destination, True
    else:
        print("Invalid move! Path is blocked or invalid.")
        return queen_pos, False


def play_game():
    """
    Main function to play the Queen's Game. Includes game setup, gameplay loop,
    scoring, and the option to start a new game.
    """
    clear_screen()  # Clear previous outputs before starting the game

    while True:  # Loop to allow starting a new game
        # Initialize game board, queen position, and goal
        board, queen_pos, goal_pos = create_board()
        score = INITIAL_SCORE

        print("Welcome to the Queen's Game!")
        print("Reach the goal with the highest score possible!")
        print_board(board)

        first_move = True  # Flag to skip clearing the screen on the first display

        while True:  # Game loop
            print(f"Queen's position: {queen_pos}")
            print(f"Score: {score}")
            try:
                # Get destination coordinates from the player
                x_dest = int(input("Enter destination row (0-7): "))
                y_dest = int(input("Enter destination column (0-7): "))
            except ValueError:
                print("Invalid input! Coordinates must be integers between 0 and 7.")
                continue

            # Check if destination is within bounds
            if not (0 <= x_dest < BOARD_SIZE and 0 <= y_dest < BOARD_SIZE):
                print("Invalid coordinates! Out of bounds.")
                continue

            # Move the queen to the desired destination
            destination = (x_dest, y_dest)
            original_position = queen_pos  # Store the original position
            queen_pos, moved = move_queen(board, queen_pos, destination)

            if moved:
                # Calculate distance traveled and deduct score
                distance = max(abs(x_dest - original_position[0]), abs(y_dest - original_position[1]))
                score -= distance
                print_board(board, clear=not first_move)
                first_move = False

            # Check for game over conditions
            if score <= 0:
                print("Game over! You ran out of points.")
                break

            if queen_pos == goal_pos:
                print(f"Congratulations! You've reached the goal with a score of {score}.")
                break

        # Ask the player if they want to start a new game
        play_again = input("Do you want to start a new game? (yes/no): ").strip().lower()
        if play_again != "yes":
            print("Thank you for playing the Queen's Game! Goodbye!")
            break


if __name__ == "__main__":
    play_game()
