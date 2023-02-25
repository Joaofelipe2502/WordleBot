# 0 is gray
# 1 is yellow
# 2 is green
import cProfile
import math
import pstats
import random
import time
from statistics import mean


class Colors:
    GRAY = "\033[40m"
    YELLOW = "\033[43m"
    GREEN = "\033[42m"
    END = "\033[0m"


class Guess:
    def __init__(self, guess, avg_remaining_words):
        self.guess = guess
        self.avg_remaining_words = avg_remaining_words


class Pattern:
    def __init__(self, pattern, calculated_average_remaining):
        self.pattern = pattern
        self.calculated_average_remaining = calculated_average_remaining


color_dict = {
    'g': 2,
    'green': 2,
    'yellow': 1,
    'y': 1,
    'gray': 0,
    '-': 0,

    2: 'g',
    1: 'y',
    0: '-'
}

def color(c):
    if c == 0:
        return Colors.GRAY
    if c == 1:
        return Colors.YELLOW
    if c == 2:
        return Colors.GREEN
    return Colors.END


with open('wordleList.txt') as word_file:
    word_list = set(word_file.read().split())


with open('answer_list.txt') as word_file:
    answer_list = set(word_file.read().split())


with open('test.txt') as word_file:
    short_list = set(word_file.read().split())


def main():
    print("\n\nWELCOME TO WORDLE")

    is_manual = False
    answer = ""
    valid_words = word_list
    if input("Are you using me in a real game (manually input pattern output)[y], or would you like to play against me (choose your own / random word)[n] [y/n]\n") == "y":
        is_manual = True
    else:
        if input("Would you like to randomize the answer? [y/n]\n") == "y":
            answer = random.choice(list(answer_list))
        else:
            answer = input("Input the answer: ")
            if not check_valid_wordle(answer):
                raise ValueError

    print("To start ", end="")
    guess, pattern = game(answer, is_manual)
    guesses_remaining = 5

    while True:
        valid_words = get_valid_words(guess, pattern, valid_words)
        print(f"\nYou have {guesses_remaining} guesses remaining")
        print("\nWhat next?")
        print("Input 'v' to see valid answers")
        print("Input 'b' to see the best answers")
        print("Input 'c', or anything else to continue the game")
        inp = input("> ")[0]

        if inp == "v":
            print(valid_words)
            print(f"That's {len(valid_words)} remaining possible guesses")
            continue

        if inp == "b":
            best_guesses = find_best_guess(valid_words, word_list)
            print("See how many guesses?")
            requested_number = int(input("> "))
            for i in range(requested_number):
                try:
                    print(f"{best_guesses[i].guess} on average leaves {best_guesses[i].avg_remaining_words}")
                except ValueError:
                    print("No more valid guesses")
                    break
            continue

        print("\n")
        guess, pattern = game(answer, is_manual)
        guesses_remaining -= 1


def game(answer, is_manual):
    guess = ""
    while not check_valid_wordle(guess):
        print("Input a guess, 5 letters, no special characters.")
        guess = input("Guess:    ").lower()

    if is_manual is True:
        pattern_inp = input(f"Input pattern output (g = green, y = yellow, \"-\" = gray), ie \"gy--g\"\n{guess.upper()}\n").lower()[:5]
        pattern = [color_dict[i] for i in pattern_inp]
    else:
        pattern = get_pattern(guess, answer)
        print("feedback: ", end="")
    for i in range(5):
        c = pattern[i]
        print(f"{color(c)}{guess[i].upper()}{color(5)}", end="")
    print("")
    return guess, pattern


def get_pattern(guess, answer):
    pattern = [0, 0, 0, 0, 0]
    for idx, letter in enumerate(guess):

        if letter == answer[idx]:
            pattern[idx] = 2

        if letter not in answer or pattern[idx] == 2:
            continue

        while letter in answer:
            index = answer.index(letter)
            if answer[index] == guess[index]:
                pattern[index] = 2
            else:
                pattern[idx] = 1
            answer = answer.replace(letter, "-", 1)

    return pattern


def get_valid_words(guess, pattern, dictionary):
    valid_words = []
    for word in dictionary:
        word_pattern = get_pattern(guess, word)
        if word_pattern == pattern:
            valid_words.append(word)
    return valid_words


def average_remaining_words(guess, dictionary):
    start_time = time.time_ns()
    pool = []
    pattern_pool = []
    for answer in dictionary:
        pattern = get_pattern(guess, answer)
        try:
            index = [x.pattern for x in pattern_pool].index(pattern)
            pool.append(pattern_pool[index].calculated_average_remaining)
        except ValueError:
            avg_words = len(get_valid_words(guess, pattern, dictionary))
            pool.append(avg_words)
            pattern_pool.append(Pattern(pattern, avg_words))

    end_time = time.time_ns()
    return mean(pool)


def find_best_guess(valid_words, dictionary):
    guess_list = []
    i = 0
    for guess in dictionary:
        guess_list.append(Guess(guess, average_remaining_words(guess, valid_words)))
        i += 1
        print(f"{i} - {round((i/14855)*100, 3)}%")
    guess_list.sort(key=lambda x: x.avg_remaining_words)
    return guess_list


def check_valid_wordle(wordle):
    if wordle.isalpha() and len(wordle) == 5:
        return True
    return False

if __name__ == '__main__':
    """
    FOR TESTING WHAT FUNCTION TAKES SO LONG
    with cProfile.Profile() as pr:
        best_guess = find_best_guess(answer_list, word_list)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()"""

    main()