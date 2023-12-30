from src.card import DeckOfCards, Ship
from src.players import Player
from src.game import Game
from src.table import Table
from src.func import report_drawn_card, end_of_round, tax_card_is_drawn, expedition_card_is_drawn
from src.func import ship_card_is_drawn, is_valid_card_on_table, select_card_from_table, check_ship_amount, admiral_check
from src.func import check_expedition
from src.func import clear_terminal, report_player_status
from src.support_functions import *
import msvcrt
import json
import os
import datetime
import time
import logging
import keyboard
from icecream import ic
from termcolor import colored as tc
 

clear_terminal()
splash_screen()

# Start of Game
print_color("-----------------------STARTING THE GAME----------------------", "blue") 
folder_path = "output"  # Replace this with the actual folder path
files = os.listdir(folder_path)# List all files in the folder
clear_log_files(folder_path, files)

# Set the logging file settings
logging.basicConfig(filename='output\logfile.log', filemode='w', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

while True:
    try:
        number_of_players = 2 #int(input(tc("How many players will be playing this game (2-5)?", attrs=["underline"] )))
        if number_of_players < 2 or number_of_players > 5:
            print("Invalid input. Please enter a number between 2 and 5.")
        else:
            break
            
    except ValueError:
        print(f"Invalid number of players. Please enter value from 2 to 5.")

# number_of_players = 2
# Get the current date in YYYY-MM-DD format
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
logging.info("Prepare the game")

# Creating table
#print("-----------------------CREATING THE TABLE----------------------") 
table = Table()
#print("\t table created - OK")
logging.info("Table created")

#print("-----------------------CREATING DECK OF CARDS----------------------") 
# Start of game, create a deck of cards
doc = DeckOfCards()
doc.create_deck()
logging.info("Deck of cards created, total number of cards %i"%(doc.remaining_cards))
#print("We now have %i cards in the deck:" %(doc.remaining_cards))

# Creating game
#print("-----------------------CREATING GAME----------------------") 
game = Game(doc)

temp_names = ["Rowland", "Divan"]

for index, player in enumerate(range(number_of_players), start=1):
    name_of_player = temp_names[index-1]#input(f"\t Enter the name of player number {index}: ")
   # name_of_player = "player_" + str(index)
    a_player = Player(index, name_of_player)
    a_player.add_money(3)
    game.add_player(a_player)

    # create log file for each player
    file_handler1 = logging.FileHandler(f'output\{current_date}_{a_player.id}_{a_player.name}_logger.log')# Create file handlers for the two log files
    file_handler1.setFormatter(formatter)# Set the formatter for the file handlers
    logger1 = logging.getLogger(f'{current_date}_{a_player.id}_{a_player.name}_logger')# Create loggers with different names
    logger1.setLevel(logging.INFO)# Set the logging level for loggers to INFO
    logger1.addHandler(file_handler1)# Add the file handlers to the loggers
    logger1.info('This is the logger file for player %i, %s'%(a_player.id, a_player.name))# Test the loggers
    logger1.info(f'mo=money, vp=victory points, de=defences, di=discount, pe=permanant, te=temporary, , ca = cards, message')
    logger1.info(f'mo\tvp\tde\tdi\tpe\tte\tca\tmessage')
    logger1.info('3\t0\t0\t0\t0\t0')# Test the loggers
    #report_player_status(a_player) #add an Icecream print statement


print(tc("The following people are playing PyRates:", attrs=["underline"]))
for index, player in enumerate(game.players, start=1):
    print(f"\t {index}. {player.name} has {player.money} money to start.")
print("Now we are ready to play...")

print("-----------------------START GAME------------------------") 
logging.info("Game started")
playing=True
print(tc(f"Active player: {game.players[0].name} press 'enter' to draw a card", color = "magenta"))
is_valid = False
while playing:
    while True:
        char = msvcrt.getch()
        result1, result2, result3 = True, True, True # reset validation tests after each card draw
        if char == b'\r':  # Perform the action for Enter here
            drawn_card = game.deck_of_cards.draw_card() # draw a card from the pile
            if len(game.deck_of_cards.cards) < 5: 
                game.shuffle_cards(table) # shuffle deck when only 5 cards remain
            report_drawn_card(game, drawn_card) # report on this card back to the terminal
            
            result1 = tax_card_is_drawn(drawn_card, table, game) # in the event that the tax card is drawn...
            result2 = expedition_card_is_drawn(drawn_card, table) # in the event that the expedition card is drawn...
            result3 = ship_card_is_drawn(drawn_card, table, player, game) # in the event that the ship card is drawn...
            #print(result1, result2, result3)

            # if you have drawn two ships
            if not result3: 
                print(tc("------------------------------------------------------------------", color="red"))
                game.change_order_of_play() #Move current start player to the back of order of play
                time.sleep(2)
                clear_terminal()
                end_of_round(game, table) #End of the round, all remaining cards are placed on the waste pile
                print(f"{game.order_of_play[0].name} to start the next round")
                break

            # only add the card to the table if results 1-3 are false
            if result1 and result2 and result3:
                table.add_card_to_table(drawn_card) # add card to the table
                #print(table.cards_on_table)

            # check to see if there are valid options on the table to select
            is_valid = is_valid_card_on_table(table, player)

        elif char == b'\x1b' and is_valid:  # Perform the action for Esc here
            
            print("You pressed Esc. You may now select a card")
            for a_player in game.order_of_play:
                admiral_check(table, a_player)  # After the round has been stopped, count the number of cards and check for +5 cards       
                check_ship_amount(table, a_player)

                cards_to_draw = int(a_player.extra_card_temp + a_player.extra_card_perm + 1)
                print(tc("---------->  number of cards to draw: "+str(cards_to_draw), color="blue"))
                for draw in range(cards_to_draw):
                    print(tc("---------->  draw number: "+str(draw+1), color="blue"))
                    game_status = select_card_from_table(table, a_player, game, draw) # Player to select a card from the table, append card to player's hand,and remove from table
                    if game_status[0]: break

                print(tc("------------------------------------------------------------------", color="green"))
            
            print(tc("------------------------------------------------------------------", color="red"))
            game.change_order_of_play() #Move current start player to the back of order of play
            time.sleep(2)
            clear_terminal()
            end_of_round(game, table) #End of the round, all remaining cards are placed on the waste pile
            
        
        elif char == b'q': # Perform the action for 'q' which will alow the player to look at the Expedition area
            print("The expedition area contains the following expeditions:")
            for index, cards in enumerate(table.expeditions, start=1):
                print(f'{index}. Symbols: {cards.symbols} vp: {cards.vp}')

            # Check if the player qulaify for any of the expeditions cards
            qualify_for_these = check_expedition(a_player, table)
            if qualify_for_these != []:
                print("You qualify for the following expeditions:")
                for index, cards in enumerate(qualify_for_these, start=1):
                    print(f'{index}. Symbols: {cards.symbols} vp: {cards.vp}') 
                
                # Now you have to choise from these options
                choice = int(input(f"{a_player.name} select a card: "))
                print("0. Not interested yet")
                if 1 <= choice <= len(qualify_for_these):
                    selected_option = qualify_for_these[choice - 1]  
                    a_player.add_card_to_hand(selected_option)
                    a_player.add_money(selected_option.give_money)
                    table.remove_card_to_expeditions(selected_option)
                elif choice == 0:
                    pass
                else:
                    print("Select a valid option")
                          
            else:
                print("You do not have the right cards to swop for expeditions")

        elif char == b'w':
            print(tc("You want to see your cards?", color="green"))
            for card in player.cards:
                print("%s" %(card.name))

        else:

            print("Invalid input - press 'enter' to draw a card, 'q' to look at the exidition area and 'esc' to stop")

print(f'We have a winner!!!')



