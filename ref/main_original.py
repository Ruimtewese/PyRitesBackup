from src.card import DeckOfCards, Ship
from src.players import Player
from src.game import Game
from src.table import Table
from src.func import (report_drawn_card, end_of_round, tax_card_is_drawn, expedition_card_is_drawn,
                      ship_card_is_drawn, is_valid_card_on_table, select_card_from_table, 
                      check_ship_amount, admiral_check, check_expedition)
from src.func import clear_terminal, report_player_status
from src.support_functions import *
import json
import os
import datetime
import time
import logging
import msvcrt

def main():
    """
    The main function orchestrates the game flow, including setting up the game, handling player turns, 
    and managing the game state. It also includes logging and user interaction.

    Parameters:
    None

    Returns:
    None
    """

    # Start of Game
    print_color("-----------------------STARTING THE GAME----------------------", "blue") 
    folder_path = "output"  # Replace with actual folder path
    files = os.listdir(folder_path)  # List all files in the folder
    clear_log_files(folder_path, files)

    # Set up logging
    logging.basicConfig(filename=os.path.join(folder_path, 'logfile.log'), filemode='w', level=logging.DEBUG, 
                        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Get number of players
    while True:
        try:
            number_of_players = 2  # Replace with user input if necessary
            if number_of_players < 2 or number_of_players > 5:
                print("Invalid input. Please enter a number between 2 and 5.")
            else:
                break
        except ValueError:
            print("Invalid number of players. Please enter a value from 2 to 5.")

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    logging.info("Prepare the game")

    # Creating table and deck of cards
    table = Table()
    logging.info("Table created")

    doc = DeckOfCards()
    doc.create_deck()
    logging.info(f"Deck of cards created, total number of cards {doc.remaining_cards}")

    game = Game(doc)

    # Create players and set up logging
    temp_names = ["Rowland", "Divan"]
    for index, player in enumerate(range(number_of_players), start=1):
        name_of_player = temp_names[index-1]
        a_player = Player(index, name_of_player)
        a_player.add_money(3)
        game.add_player(a_player)

        log_file_path = os.path.join(folder_path, f'{current_date}_{a_player.id}_{a_player.name}_logger.log')
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        logger = logging.getLogger(f'{current_date}_{a_player.id}_{a_player.name}_logger')
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        logger.info(f'This is the logger file for player {a_player.id}, {a_player.name}')
        logger.info('mo=money, vp=victory points, de=defences, di=discount, pe=permanent, te=temporary, ca=cards, message')
        logger.info('3\t0\t0\t0\t0\t0')

    print(tc("The following people are playing PyRites:", attrs=["underline"]))
    for index, player in enumerate(game.players, start=1):
        print(f"\t {index}. {player.name} has {player.money} money to start.")
    print("Now we are ready to play...")

    print("-----------------------START GAME------------------------") 
    logging.info("Game started")
    playing = True
    print(tc(f"Active player: {game.players[0].name} press 'enter' to draw a card", color="magenta"))

    while playing:
        char = msvcrt.getch()
        result1, result2, result3 = True, True, True  # Reset validation tests after each card draw
        if char == b'\r':  # Enter key
            drawn_card = game.deck_of_cards.draw_card()
            if len(game.deck_of_cards.cards) < 5:
                game.shuffle_cards(table)
            report_drawn_card(game, drawn_card)
            result1 = tax_card_is_drawn(drawn_card, table, game)
            result2 = expedition_card_is_drawn(drawn_card, table)
            result3 = ship_card_is_drawn(drawn_card, table, player, game)

            if not result3:
                print(tc("------------------------------------------------------------------", color="red"))
                game.change_order_of_play()
                time.sleep(2)
                clear_terminal()
                end_of_round(game, table)
                print(f"{game.order_of_play[0].name} to start the next round")
                continue

            if result1 and result2 and result3:
                table.add_card_to_table(drawn_card)

            is_valid = is_valid_card_on_table(table, player)

        elif char == b'\x1b' and is_valid:  # Esc key
            print("You pressed Esc. You may now select a card")
            for a_player in game.order_of_play:
                admiral_check(table, a_player)
                check_ship_amount(table, a_player)

                cards_to_draw = a_player.extra_card_temp + a_player.extra_card_perm + 1
                print(tc(f"---------->  number of cards to draw: {cards_to_draw}", color="blue"))
                for draw in range(cards_to_draw):
                    print(tc(f"---------->  draw number: {draw + 1}", color="blue"))
                    game_status = select_card_from_table(table, a_player, game, draw)
                    if game_status[0]:
                        break

                print(tc("------------------------------------------------------------------", color="green"))

            print(tc("------------------------------------------------------------------", color="red"))
            game.change_order_of_play()
            time.sleep(2)
            clear_terminal()
            end_of_round(game, table)

        elif char == b'q':  # 'q' key
            print("The expedition area contains the following expeditions:")
            for index, cards in enumerate(table.expeditions, start=1):
                print(f'{index}. Symbols: {cards.symbols} vp: {cards.vp}')

            qualify_for_these = check_expedition(a_player, table)
            if qualify_for_these:
                print("You qualify for the following expeditions:")
                for index, cards in enumerate(qualify_for_these, start=1):
                    print(f'{index}. Symbols: {cards.symbols} vp: {cards.vp}')

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
                print("You do not have the right cards to swap for expeditions")

        elif char == b'w':  # 'w' key
            print(tc("You want to see your cards?", color="green"))
            for card in player.cards:
                print(card.name)

        else:
            print("Invalid input - press 'enter' to draw a card, 'q' to look at the expedition area, and 'esc' to stop")

    print('We have a winner!!!')

if __name__ == "__main__":
    clear_terminal()
    splash_screen()
    main()
