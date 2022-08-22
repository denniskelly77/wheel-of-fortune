# Wound up not using all of these imports
from config import word_list_loc
from config import turntextloc
from config import wheel_text_loc
from config import max_rounds
from config import vowel_cost
from config import roundstatusloc
from config import final_prize
from config import finalRoundTextLoc

import random

players = {0: {"round total": 0, "game total": 0, "name": ""},
           1: {"round total": 0, "game total": 0, "name": ""},
           2: {"round total": 0, "game total": 0, "name": ""},
           }

round_num = 0
word_list = []
turn_text = ""
wheel_list = []
round_word = ""
blank_word = []
vowels = {"a", "e", "i", "o", "u"}
round_status = ""
final_round_text = ""

# Define function to unmask letters in blank_word
def update_blank_word(letter):
    global blank_word
    blank_word = ''.join([round_word[i] if round_word[i] == letter else blank_word[i] for i in range(len(round_word))])

def read_dictionary_file():
    global word_list
    # Read dictionary file in from dictionary file location
    # Store each word in a list.
    with open(word_list_loc, 'r') as f:
        word_list = f.read().lower().split('\n')


def read_turn_txt_file():
    global turn_text
    # read in turn intial turn status "message" from file


def read_final_round_txt_file():
    global final_round_text
    # read in turn intial turn status "message" from file


def read_round_status_txt_file():
    global round_status
    # read the round status  the Config roundstatusloc file location


def read_wheel_txt_file():
    global wheel_list
    # read the Wheel name from input using the Config wheelloc file location
    def safe_int(x):
        try:
            return int(x)
        except ValueError:
            return x
    
    with open(wheel_text_loc, 'r') as f:
        wheel_text = f.read().split('\n')
    
    wheel_list = list(map(safe_int, wheel_text))


def get_player_info():
    global players
    for player in players.keys():
        players[player]['name'] = input(f"What's your name, player {player}? ")

def display_round_amounts():
    print("\nRound Amounts for Each Player")
    for player in players.keys():
        print(f"{players[player]['name']} has earned {players[player]['round total']} this round")
    
    input("\nPress enter ")

def display_game_amounts():
    print("\nTotal Game Amounts for Each Player")
    for player in players.keys():
        print(f"{players[player]['name']} has ${players[player]['game total']} in the bank")
    
    input('\nPress enter ')


def game_setup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turn_text
    global word_list

    read_dictionary_file()
    read_turn_txt_file()
    read_wheel_txt_file()
    get_player_info()
    read_round_status_txt_file()
    read_final_round_txt_file()


def get_word():
    global word_list
    global round_word
    global blank_word
    # choose random word from dictionary
    # make a list of the word with underscores instead of letters.
    word = random.choice(word_list)
    word_list.remove(word)
    round_underscore_word = ''.join(['_' if c.isalpha() else c for c in word])
    return word, round_underscore_word


def wof_round_setup():
    global players
    global round_word
    global blank_word

    # Set round total for each player = 0
    for player in players.keys():
        players[player]['round total'] = 0

    # Return the starting player number (random)
    init_player = random.choice(range(3))

    # Use getWord function to retrieve the word and the underscore word (blankWord)
    round_word, blank_word = get_word()

    return init_player

def final_round_setup():
    global players
    global round_word
    global blank_word

    # Get the word for the final round
    round_word, blank_word = get_word()

    # Find and return the index of the winning player
    return sorted(players, key=lambda s: players[s]['game total'])[-1]

def guess_letter(letter, player_num):
    global players
    global blank_word
    # parameters:  take in a letter guess and player number
    # Change position of found letter in blankWord to the letter instead of underscore
    # return good_guess= true if it was a correct guess
    # return count of letters in word.
    # ensure letter is a consonant.
    letter = letter.lower()
    if letter in vowels:
        print(f"{letter.upper()}'s not a consonant! Lose a turn")
        good_guess = False
        count = 0
    elif letter in blank_word:
        print(f"{letter.upper()} has already been guessed! Lose a turn")
        good_guess = False
        count = 0
    else:
        update_blank_word(letter)
        good_guess = letter in round_word if not blank_word == round_word else False
        count = round_word.count(letter)
    
    return good_guess, count


def spin_wheel(player_num):
    global wheel_list
    global players
    global vowels

    # Get random value for wheellist
    # Check for bankrupcy, and take action.
    # Check for loose turn
    # Get amount from wheel if not loose turn or bankruptcy
    # Ask user for letter guess
    # Use guessletter function to see if guess is in word, and return count
    # Change player round total if they guess right.
    event = random.choice(wheel_list)
    print(f"Result of spin is {event}")
    if event == 'BANKRUPT':
        print(f"Sorry {players[player_num]['name']}, you've gone bankrupt and your turn is over")
        players[player_num]['round total'] = 0
        still_in_turn = False
    elif event == "Lose a Turn":
        print(f"Sorry {players[player_num]['name']}, your turn is over")
        still_in_turn = False
    else:
        print(f"Amount at stake: ${event}")
        guess = input('Guess a consonant: ')
        still_in_turn, multiplier = guess_letter(guess, player_num)
        players[player_num]['round total'] += event*multiplier
        if multiplier == 0: print("Letter not in word, better luck next time")


    return still_in_turn


def buy_vowel(player_num):
    global players
    global blank_word
    global vowels

    # Take in a player number
    # Ensure player has 250 for buying a vowelcost
    # Use guessLetter function to see if the letter is in the file
    # Ensure letter is a vowel
    # If letter is in the file let good_guess = True
    if players[player_num]['round total'] < vowel_cost:
        print("Not enough money to buy a vowel")
        good_guess = False
    else:
        players[player_num]['round total'] -= vowel_cost
        purchase = input("Which vowel would you like to buy? ")
        if purchase not in vowels:
            print("Not a vowel, lose a turn")
            good_guess = False
        elif purchase in blank_word:
            print("Vowel already in word, lose a turn")
            good_guess = False
        else:
            update_blank_word(purchase)
            good_guess = purchase in round_word if not round_word == blank_word else False
            if purchase not in round_word: print('Vowel not in word, turn over')

    return good_guess


def guess_word(player_num):
    global players
    global blank_word
    global round_word

    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    # Fill in blankList with all letters, instead of underscores if correct
    # return False ( to indicate the turn will finish)

    guess = input("What word would you like to guess? ").lower()
    if guess == round_word:
        print("You got it!")
        blank_word = ''.join([c for c in round_word])
    else:
        print(f"Wrong guess {players[player_num]['name']}, turn's over. Too bad!")

    return False


def wof_turn(player_num):
    global round_word
    global blank_word
    global turn_text
    global players

    # take in a player number.
    # use the string.format method to output your status for the round
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal

    still_in_turn = True
    while still_in_turn:

        # use the string.format method to output your status for the round
        # Get user input S for spin, B for buy a vowel, G for guess the word
        print(f"\nIt's {players[player_num]['name']}'s turn\n")
        print("Select S to spin the wheel")
        print("Select B to buy a vowel")
        print("Select G to guess the word")
        print(f"Amount you've earned this round {players[player_num]['round total']}")
        print(f"On the board: {blank_word}")

        choice = input("What would you like to do? ")

        if(choice.strip().upper() == "S"):
            still_in_turn = spin_wheel(player_num)
        elif(choice.strip().upper() == "B"):
            still_in_turn = buy_vowel(player_num)
        elif(choice.upper() == "G"):
            still_in_turn = guess_word(player_num)
        else:
            print("Not a correct option")

    # Check to see if the word is solved, and return false if it is,
    # Or otherwise break the while loop of the turn.


def wof_round():
    global players
    global round_word
    global blank_word
    global round_status
    current_player = wof_round_setup()

    # Keep doing things in a round until the round is done ( word is solved)
    # While still in the round keep rotating through players
    # Use the wofTurn fuction to dive into each players turn until their turn is done.

    # Print roundstatus with string.format, tell people the state of the round as you are leaving a round.
    print('\nNew Round\n')
    input('Press enter ')
    still_in_round = True
    while still_in_round:
        display_round_amounts()
        wof_turn(current_player)

        if round_word == blank_word:
            still_in_round = False
        else:
            current_player = (current_player + 1) % 3

    print(f"{players[current_player]['name']} has won the round! The word was {round_word}")
    # Update winner's bank amount
    players[current_player]['game total'] += players[current_player]['round total']
    display_game_amounts()


def wof_final_round():
    global round_word
    global blank_word
    global final_round_text
    default_revelations = {'r', 's', 't', 'l', 'n', 'e'}
    win_player = final_round_setup()
    amount = final_prize

    # Find highest gametotal player.  They are playing.
    # Print out instructions for that player and who the player is.
    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    # Gather 3 consonants and 1 vowel and use the guessletter function to see if they are in the word
    # Print out the current blankWord again
    # Remember guessletter should fill in the letters with the positions in blankWord
    # Get user to guess word
    # If they do, add finalprize and gametotal and print out that the player won

    # Perform the default updates to the blank word
    # Print statements to introduce final round
    print("\nFinal Round\n")
    input("Press enter ")
    print(f"\n{players[win_player]['name']} has the highest game total, so they'll be playing in the final round")
    
    # Reveal default letters
    for c in default_revelations:
        update_blank_word(c)
    
    # Ask the user for 3 consonants
    for i in range(3):
        print(f"On the board: {blank_word}")
        guess = input("Please guess a consonant ")
        guess_letter(guess, win_player)
    
    # Ask the user for a vowel
    print(f"On the board: {blank_word}")
    guess = input("Please guess a vowel ")
    if guess in vowels:
        update_blank_word(guess)
    else:
        print("That wasn't a vowel")
    
    # Print blank_word and prompt the user to guess the word
    print(f"\nAlright {players[win_player]['name']}, it's time to guess the word")
    print(f"On the board: {blank_word}")
    guess_word(win_player)

    if blank_word == round_word:
        print(f"Congrats {players[win_player]['name']}, you've won! Your prize is ${amount}!")
    else:
        print(f"The word was {round_word}. Thanks for playing and better luck next time")
        


def main():
    game_setup()

    for i in range(0, max_rounds):
        if i in [0, 1]:
            wof_round()
        else:
            wof_final_round()


if __name__ == "__main__":
    main()


    