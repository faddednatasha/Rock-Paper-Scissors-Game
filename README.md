# 🐍 Python Word Scramble Game
---
A simple, interactive word scrambling game implemented in Python. Test your vocabulary and deductive skills by unscrambling a randomly selected word from a predefined list.

## ✨ Features

Random Word Selection: A secret word is chosen at random from a diverse list.

Efficient Scrambling: Uses Python's built-in random.sample function to ensure the word is thoroughly mixed.

Attempt Tracking: Keeps count of how many guesses it takes to solve the puzzle.

Simple Command Line Interface: Easy to run and play in any terminal environment.

## ⚙️ How to Run

Prerequisites

You only need Python 3 installed on your system.

1. Save the Code

Save the provided code into a file named word_scramble.py.

2. Run from Terminal

Open your terminal or command prompt, navigate to the directory where you saved the file, and execute the following command:

game.py



## 🕹️ Game Logic

Start: The game selects a secret word from its internal dictionary.

Scramble: The scramble_word function shuffles the letters of the secret word.

Prompt: The user is presented with the scrambled word and prompted for a guess.

Guessing: The user enters their guess. The game tracks the number of attempts.

Win Condition: If the guess matches the secret word (case-insensitive), the game congratulates the player and reports the total attempts.

Fail Condition: If the guess is incorrect, the player is prompted to try again.

## 🛠️ Customization

To make the game more challenging or tailored, you can easily modify the word list within the word_scramble_game function:

    words = ["python", "programming", "challenge", "computer", "developer"]
    # Change this list to your preferred words!
