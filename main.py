# An upgraded wordle game
# Includes: streak counting, user statistics, theme and difficulty specific levels, timer


# Import modules
import pathlib
import random

from rich.console import Console
from rich.theme import Theme

console = Console(width=40, theme=Theme({"warning": "red on yellow"}))

# choose category


def choose_category():
    categories = {
        "1": "animals",
        "2": "jobs",
        "3": "countries",
        "4": "feelings",
        "5": "food",
        "6": "vehicles",
        "7": "random"
    }

    console.print("Choose a category:")
    for key, value in categories.items():
        console.print(f"{key}. {value.title()}")

    while True:
        cat_choice = input("Enter the number of your category: ").strip()
        if cat_choice in categories:
            return categories[cat_choice]
        else:
            console.print("Invalid choice, try again.")


def load_words(category):
    words_path = pathlib.Path(__file__).parent / "words" / f"{category}.txt"
    words = words_path.read_text(encoding="utf-8").split("\n")
    return words


# Rules:
max_guesses = 5
word_length = 5

# store previous guesses and outcomes
guesses = []
outcomes = []

# function to select words at random from my list


def choose_word(words):
    secret_word = random.choice(words)

    return secret_word


def get_user_guess():
    user_guess = input("Enter your guess: ").lower().strip()

    return user_guess


def validate_guess(user_guess):
    if len(user_guess) != word_length:
        print(
            f"Guess must be {word_length} letters long. '{user_guess}' is {len(user_guess)} characters long.")
        return False
    if not user_guess.isalpha():
        print("Guess must only contain letters.")
        return False

    return True

# function which returns the feedback for each letter


def check_guess(secret_word, user_guess):
    # detects if present and correct position
    # present but incorrect position
    # letter not present in word

    # initialise all letters as absent
    result = ["absent"] * word_length
    secret_word_copy = list(secret_word)

    # needs to be passed through twice to avoid repeated letters issue
    # first pass to identify the position of all correct letters
    for i in range(len(user_guess)):
        if user_guess[i] == secret_word[i]:
            result[i] = "correct"
            # note letter as used
            secret_word_copy[i] = None

    # second pass to identify the position of all present letters
    for i in range(len(user_guess)):
        if result[i] == "correct":
            continue
        if user_guess[i] in secret_word_copy:
            result[i] = "present"
            letter_index = secret_word_copy.index(user_guess[i])
            secret_word_copy[letter_index] = None

    return result

# show results


def show_outcome_grid():
    # print("Outcome:")
    console.print()
    for row in range(max_guesses):
        if row < len(guesses):
            user_guess = guesses[row]
            outcome = outcomes[row]

            # display the guess
            for i in range(word_length):
                if outcome[i] == "correct":
                    console.print(
                        f"[bold white on green]{user_guess[i].upper()}[/]", end=" ")

                elif outcome[i] == "present":
                    console.print(
                        f"[bold white on yellow]{user_guess[i].upper()}[/]", end=" ")

                elif outcome[i] == "absent":
                    console.print(
                        f"[bold white on grey37]{user_guess[i].upper()}[/]", end=" ")

        else:
            console.print("_ "*word_length, end="")

        # new line
        console.print()
    # blank line
    console.print()

# main function


def main():
    # assigning the word user needs to guess
    console.print("Welcome to my Wordle Game!")
    category = choose_category()
    words = load_words(category)
    secret_word = choose_word(words)
    guess_num = 0
    previous_guesses = []

    console.print(f"You chose {category.title()}!\n")
    print(
        f"You have {max_guesses} attempts to guess the {word_length}-letter word.")

    while guess_num < max_guesses:
        guess = get_user_guess()

        if validate_guess(guess) == False:
            continue

        if guess in previous_guesses:
            print("You have already guessed that word. Try again.")
            continue

        # keep track of the words that have already been guessed
        previous_guesses.append(guess)

        outcome = check_guess(secret_word, guess)

        # update the guesses and outcomes lists
        guesses.append(guess)
        outcomes.append(outcome)

        # display the grid
        show_outcome_grid()

        guess_num += 1

        if guess == secret_word:
            print(f"{guess.upper()} is right! You win!")
            print(f"You guessed the word in {guess_num} attempts.")
            break

        print(f"Attempts remaining: {max_guesses-guess_num}")

    else:
        print("Unfortunately you didn't guess the word within the allowed number of tries.")
        print(f"The word was '{secret_word}'.")


main()
