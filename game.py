import random

def scramble_word(word):
    return "".join(random.sample(word, len(word)))

def word_scramble_game():
    words = ["python", "programming", "challenge", "computer", "developer"]
    secret_word = random.choice(words)
    scrambled = scramble_word(secret_word)

    print(f"Unscramble this word: {scrambled}")
    
    attempts = 0
    while True:
        guess = input("Your guess: ").lower()
        attempts += 1
        if guess == secret_word:
            print(f"Correct! You got it in {attempts} attempts.")
            break
        else:
            print("Incorrect. Try again!")

if __name__ == "__main__":
    word_scramble_game()
