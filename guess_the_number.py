import random


def play_game():
    secret_number = random.randint(1, 100)
    guess_count = 0

    print("Guess the Number")
    print("I am thinking of a number between 1 and 100.")

    while True:
        guess_text = input("Enter your guess: ")

        if not guess_text.isdigit():
            print("Please enter a whole number.")
            continue

        guess = int(guess_text)
        guess_count += 1

        if guess < secret_number:
            print("Too low. Try again.")
        elif guess > secret_number:
            print("Too high. Try again.")
        else:
            print(f"You got it in {guess_count} guesses!")
            break


if __name__ == "__main__":
    play_game()
