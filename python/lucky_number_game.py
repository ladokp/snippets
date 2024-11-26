import random
import time
import sys

def print_with_effect(text: str, delay: float = 0.05) -> None:
    """
    Print text with a typing animation effect.

    Args:
        text (str): The text to display with effect.
        delay (float): Time delay between each character, in seconds.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def lucky_number_game() -> None:
    """
    Start the Lucky Number Master game.

    The player guesses a randomly generated number within a set range,
    receiving hints and tracking their time and attempts.
    """
    print_with_effect("Welcome to the Lucky Number Master!")
    print_with_effect("Let's see if you can guess the lucky number...\n")

    # Game configuration
    lower_bound = 1
    upper_bound = 100
    lucky_number = random.randint(lower_bound, upper_bound)
    attempts = 7
    start_time = time.time()

    print_with_effect(f"I've picked a number between {lower_bound} and {upper_bound}.")
    print_with_effect(f"You have {attempts} attempts to guess it.\n")

    for attempt in range(1, attempts + 1):
        try:
            guess = int(input(f"Attempt {attempt}/{attempts} - Enter your guess: "))
        except ValueError:
            print_with_effect("That's not a valid number. Try again!")
            continue

        if guess == lucky_number:
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            print_with_effect(f"🎉 Congratulations! You guessed the lucky number {lucky_number}!")
            print_with_effect(f"You took {duration} seconds to guess correctly.")
            return
        elif guess < lucky_number:
            print_with_effect("Too low! Try a higher number.")
        else:
            print_with_effect("Too high! Try a lower number.")

    print_with_effect(f"😢 Out of attempts! The lucky number was {lucky_number}. Better luck next time!")

def main() -> None:
    """
    Main function to start the game.
    """
    while True:
        lucky_number_game()
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            print_with_effect("Thanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    main()
