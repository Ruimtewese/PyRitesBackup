from src.card import Card, SettlerCaptainPriest, Ship, Tax, Expedition
from src.card import Trader, Witzbold, SailorPirate, Vrou, Admiral, Governor
from src.players import Player
from src.game import Game
from src.table import Table
from src.support_functions import *
import json
import logging
import os
from icecream import ic
from termcolor import colored as tc # Import termcolor module



'''logging.basicConfig(filename='output\logfile2.log', filemode='w', level=logging.DEBUG, 
                format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')'''


def report_drawn_card(game: Game, drawn_card:Card):
    """
    Reports the details of a drawn card in the game.

    Args:
        game (Game): The current game object.
        drawn_card (Card): A card object drawn from the game.

    Prints:
        A formatted message with the details of the drawn card including its name,
        price, and victory points (vp).

        If the drawn card is an instance of SettlerCaptainPriest, it also includes
        the card's symbol.

    Returns:
        None
    """
    a_player = game.order_of_play[0]
    name = game.order_of_play[0].name
    name_data = f"{name} (☼{a_player.money}, {a_player.vp}vp)"
    card = drawn_card.name

    if isinstance(drawn_card, SettlerCaptainPriest): 
        vp = drawn_card.vp
        price = drawn_card.price
        sym = drawn_card.symbol
        print(f"\t{name_data} drew the {card} ({sym}), ☼{price}, vp{vp}")
        #logging.info(f"{name} drew the {card} ({sym}), ☼{price}, vp{vp}")
        logging.info("...card drawn: %s \t %s \t-%im \t+ %ivp" %(name, card, price, vp))

    elif isinstance(drawn_card, Ship):
        give_money = drawn_card.give_money
        attack = drawn_card.attack
        colour = drawn_card.colour
        print(f"\t{name_data} drew the {colour} {card}, ☼{give_money}, φ{attack}")
        #logging.info(f"{name} drew the {colour} {card}, ☼{give_money}, φ{attack}")
        logging.info("...card drawn: %s \t%s \t%s \t+%im \t%ia" %(name, colour, card, give_money, attack))

    elif isinstance(drawn_card, Tax):
        symbol = drawn_card.symbol
        if symbol == "vp":
            text = "min"
        else:
            text = "max"
        print(f"\t{name_data} drew the {card} {text} {symbol}, +☼1") 
        #logging.info(f"{name} drew the {card} {text} {symbol}, +☼1") 
        logging.info("...card drawn: %s \t%s \t%s" %(name, card, text))


    elif isinstance(drawn_card, Expedition):
        symbol = drawn_card.vp
        vp = drawn_card.vp
        print(f"\t{name_data} drew the {card} ({symbol})") 
        #logging.info(f"{name} drew the {card} ({symbol})")  
        logging.info("...card drawn: %s \t%s" %(name, card))
    
    elif isinstance(drawn_card, Trader):
        vp = drawn_card.vp
        card_name = drawn_card.name
        price = drawn_card.price
        colour = drawn_card.colour
        print(f"\t{name_data} drew the {colour} {card}, ☼{price}, vp{vp}") 
        #logging.info(f"{name} drew the {colour} {card}, ☼{price}, vp{vp}")
        logging.info("...card drawn: %s \t%s \t%s \t-%im \t+%ivp" %(name, colour, card_name, price, vp)) 

    elif isinstance(drawn_card, Witzbold):
        vp = drawn_card.vp
        price = drawn_card.price
        print(f"\t{name_data} drew the {card}, ☼{price}, vp{vp}")
        #logging.info(f"{name} drew the {card}, ☼{price}, vp{vp}")
        logging.info("...card drawn: %s \t%s \t-%im \t+%ivp" %(name, card, price, vp))

    else:
        vp = drawn_card.vp
        price = drawn_card.price
        print(f"\t{name_data} drew the {card}, ☼{price}, vp{vp}")
        #logging.info(f"{name} drew the {card}, ☼{price}, vp{vp}")
        logging.info("...card drawn: %s \t%s \t-%im \t+%ivp" %(name, card, price, vp)) 


def tax_card_is_drawn(drawn_card: Card, table: Table, game: Game):
    """This function runs when a tax card is drawn and looks for two cases: 1) more than 12 cards, and 2) which player
        gets paid tax

    Args:
        drawn_card (Card): Card that is drawn
        table (Table): All the properties of the table
        game (Game): The current game

    Returns:
        Bool : Always returns False, as the tax card goes back to the waste pile
    """
    if isinstance(drawn_card, Tax):
        #print("-------------------TAX CARD---------------")
        # if a tax card is drawn check for the following:
        #   -   A player with 12+ cards in his hand
        #   -   All player with either min VP or max swords depending on the drawn cards

        # Second check is to see who get more money
        symbol = drawn_card.symbol  # can be 'vp' or 'sword'
        min_vp = 100
        max_defence = 0

        # First check is to see if players has too many cards in hand
        for player in game.players:
            if player.money >= 12:
                player.money //= 2 # round down to integer value
                print(f"{player.name} lost half of their money, and now has {player.money}")
                my_logger(player, message = "Tax penalty")
                logging.info("%s \t%im" %(player.name, player.money))
            
            # whilst looping through player, check for min VP and max defence
            min_vp = min(min_vp, player.vp)
            max_defence = max(max_defence, player.defence)

        # find player(s) with lowest/height symbols value
        for player in game.players:
            if symbol == "vp":
                if player.vp == min_vp:
                    player.money += 1
                    print(f"{player.name} +☼1 for having min vp = {player.money}☼")
                    my_logger(player, message = "Tax for min vp")
                    logging.info("--->\t%s \t%im" %(player.name, player.money))
            elif symbol == "sword":
                if player.defence == max_defence:
                    player.money += 1
                    print(f"{player.name} +☼1 for have max defence = {player.money}☼")
                    my_logger(player, message = "Tax for max defence")
                    logging.info("--->\t%s \t%im" %(player.name, player.money))
            else:
                print("Something is wrong")           
          
        # Once done, the tax card is returned to the waste pile
        table.add_card_to_waste(drawn_card)
        return False # Card will not be added to the table
    else:
        return True

def expedition_card_is_drawn(drawn_card: Card, table: Table):
    if isinstance(drawn_card, Expedition):
        # if the expedition card is drawn, move this card to the expedition area on the table
        table.add_card_to_expeditions(drawn_card)
        print("-------> moved to expedition area")
        logging.info("---> Expedition moved to expedition area")
        return False # Card will not be added to the table
    else:
        return True

def ship_card_is_drawn(drawn_card: Card, table: Table, player: Player, game: Game):
    """Check if you attacked by a ship

    Args:
        drawn_card (Card): Card that is drawn
        table (Table): All the properties of the table
        player (Player): Current active player

    Returns:
        Bool: If you bombed out or not
    """
    if isinstance(drawn_card, Ship):
        #print("-------------------SHIP CARD---------------") 
        # Check ship validatity against cards on table and player defences
        # We will need an if-statement here to check, and can only add the card if it is
        # a valid play
     
        # Repeat for each card on the table
        for card in table.cards_on_table:
            if isinstance(card, Ship):
                #print(drawn_card.colour, card.colour)
            # Check if the same colour is drawn
                if drawn_card.colour == card.colour:
                    # Check if player has enough defence
                    if player.defence >= drawn_card.attack:
                        print("You destoyed the pirate ship")
                        logging.info("--->\t%s \tdestroyed pirate ship" %(player.name))
                        return True
                    
                    elif player.defence < drawn_card.attack:
                        print("You are defeated by the pirate attack!")
                        logging.info("--->\t%s \tdefeated by pirate ship" %(player.name))
                        # Once the current player has bombed, players with witzbold get one more money
                        witzbold_check(game, player)
                        return False 
                
        return True
    else:
        return True  

def end_of_round(game: Game, table: Table):
    print("Remaining cards to be placed on waste pile")
    for cards in table.cards_on_table:
        table.add_card_to_waste(cards)
    table.clear_table()
    print(tc(f"Active player: {game.order_of_play[0].name} press 'enter' to start the new round", color = "magenta"))

    '''for item in table.waste_cards:
        print(item.name, end=" ")

    print("")'''
    
           
def is_valid_card_on_table(table: Table, player: Player) -> bool:
    """Check if there is a valid card on the table

    Args:
        table (Table): All the properties of the table
        player (Player): Current active player

    Returns:
        True_False (bool): True if there is a valid card on the table, else False
    """
    True_False = False
    for card in table.cards_on_table:
        if card.price <= player.money or isinstance(card, Ship):
            True_False = True

    return True_False

# Functions for after esc



def admiral_check(table: Table, player: Player) -> None: 
    """Check if player has an Admiral, if True give him 2 money

    Args:
        player (Player): Player that is playing
    """

    # Check for 5 cards on the table
    if len(table.cards_on_table) > 4: 
        five_cards = True
    else:
        five_cards = False

    # For each Admiral in hand add 2 money to player
    for card in player.cards:
        if isinstance(card, Admiral) and five_cards:
            player.add_money(2)
            print(f"{player.name} now have ☼{player.money}, becuse he had an Admiral")
            my_logger(player, message = "Player has admiral")
            logging.info("----c Admiral \t%i ---> %i"%(card.price, player.money))
                

def witzbold_check(game: Game, player: Player) -> None:
    """Once a player is defeated by pirate ship, players with Witzbolds get one more money for each Witzbold

    Args:
        game (Game): This is the current game
        player (Player): This is the current player
    """
    current_player = []
    all_players = []
    remaining_players = []

    current_player = player
    all_players = game.players
    logging.info("---C\tWitzbold check")
    #print("-------> Witzbold check")
    # Remove the current player from the list of players in the game
    if current_player in all_players: 
        remaining_players = all_players[:]
        remaining_players.remove(current_player)
        
    # Then check each of the remaining players hands for a Witzbold and add money
    for player in remaining_players:
        for card in player.cards:
            if isinstance(card, Witzbold):
                print("-------> %s +1 " %(player.name), end='')
                logging.info("---C\t%s received 1 money" %(player.name))
                player.add_money(1)



def card_label_cvs(card: Card)->list:
    """_summary_

    Args:
        card (Card): _description_

    Returns:
        list: _description_
    """
    a, b, c = "##","#","#"

    if isinstance(card, Ship):
        a = "+☼" + str(card.give_money)
        b = "0"
        c = "-"
    elif isinstance(card, Trader):
        a = "-☼" + str(card.price)
        b = str(card.vp)
        c = "+1" + str(card.colour)
    elif isinstance(card,  SettlerCaptainPriest):
        a = "-☼" + str(card.price)
        b = str(card.vp)
        c = str(card.symbol)
    elif isinstance(card,  SailorPirate):
        a = "-☼" + str(card.price)
        b = str(card.vp)
        c = str(card.defence) + "S"
    elif isinstance(card,  Vrou):
        a = "-☼" + str(card.price)
        b = str(card.vp)
        c = str(card.discount)
    elif isinstance(card,  Witzbold):
        a = "-☼" + str(card.price)
        b = str(card.vp)
        c = "+1m"
    elif isinstance(card,  Admiral):
        a = "-☼" + str(card.price)
        b = str(card.vp)
        c = "+2☼"
    elif isinstance(card,  Governor):
        a = "-☼" + str(card.price)
        b = str(card.vp)
        c = "+2☼"
    else:
        print("Error")

    return a, b, c


def determine_traders(player: Player)->list:
    """Detremine the number of traders a player has in his hand

    Args:
        player (Player): The player who's turn it is

    Returns:
        list: Trader values
    """
    traders = []
    number_blue_traders = 0
    number_black_traders = 0
    number_green_traders = 0
    number_red_traders = 0
    number_yellow_traders = 0
    for card in player.cards:
        if isinstance(card, Trader):
            if card.colour == "blue": number_blue_traders += 1
            if card.colour == "black": number_black_traders += 1
            if card.colour == "green": number_green_traders += 1
            if card.colour == "red": number_red_traders += 1
            if card.colour == "yellow": number_yellow_traders += 1
    traders.append(number_blue_traders)
    traders.append(number_black_traders)
    traders.append(number_green_traders)
    traders.append(number_red_traders)
    traders.append(number_yellow_traders)

    return traders

def print_list_options(table: Table, first_player: bool, draw: int)->list:
    """Print the current list of cards to pick from

    Args:
        table (Table): The table of cards
        first_player (_type_): The first player status

     Returns:
        list: The cards on the table      
    """
    # Define a list of options
    options = table.cards_on_table  # -----------------------------------> here we can add a validation check against what the actual player can take from table
    # Display the available options
    a, b, c = "##","#","###"
    print(tc("Select an one of the following cards:", color="yellow"))
    if first_player == False or draw > 0: print("0. To skip turn")
    for index, option in enumerate(options, 1):
        a,b,c = card_label_cvs(option)
        print(f"{index}. {option.name} \t{a}\t{b}\t{c}") # ------------------------------> Add other elements for each type of card
    
    print("999. Inspect your hand")

    return options


def select_card_from_table(table: Table, player: Player, game: Game, draw: int) -> Card:
    """Function which consider all the cards on the table and ask the current player to
        select a card. This function could be repeated for multiple draws by one player

    Args:
        table (Table): Table object containing the cards on table
        player (Player): The current player to draw cards
        game (Game): The current game

    """
    report_player_status(player) # Only for debugging

    #cards_to_draw = int(player.extra_card_temp + player.extra_card_perm + 1)
    
    discount = player.discount  # Check the current players hands for Vrou cards
    traders = determine_traders(player) # Check how many traders the current player has
    if player == game.order_of_play[0]: # Check is the current player is the first player
        first_player = True
    else:
        first_player = False

    #print(tc("---------->  number of cards to draw: "+str(cards_to_draw), color="blue"))
    #for draw in range(cards_to_draw):
    #print(tc("---------->  draw number: "+str(draw), color="blue"))
    game_status = end_of_game(game) # set initial game status value
    # Define a list of options
    options = print_list_options(table, first_player, draw)
    
    # Ask the user for their selection
    while True:
        try:
            # If you are not fist player, price is +1
            second_player = 0
            if first_player == False: 
                second_player = 1
                #choice = int(input(f"Other player: {player.name} has ☼{player.money} and {player.vp}vp, select a card: "))
                choice = int(input(tc("Other player(s): %s has ☼%i and %ivp, select a card: " %(player.name, player.money, player.vp), color = "cyan")))

            else:
                #choice = int(input(f"Active player: {player.name} has ☼{player.money} and {player.vp}vp, select a card: "))
                choice = int(input(tc("Active player: %s has ☼%i and %ivp, select a card: " %(player.name, player.money, player.vp), color = "cyan")))

            if 1 <= choice <= len(options):
                selected_option = options[choice - 1]
                
                # check if drawn card is ship, take the money, and remove card from table to waste pile
                if isinstance(selected_option, Ship):
                    if selected_option.colour == "blue": 
                        player.add_money(selected_option.give_money + traders[0])
                        my_logger(player, message = f"Blue ship (+Trader) {selected_option.give_money} + {traders[0]}")
                    if selected_option.colour == "black": 
                        player.add_money(selected_option.give_money + traders[1])
                        my_logger(player, message = f"Black ship (+Trader) {selected_option.give_money} + {traders[1]}")
                    if selected_option.colour == "green": 
                        player.add_money(selected_option.give_money + traders[2])
                        my_logger(player, message = f"Green ship (+Trader) {selected_option.give_money} + {traders[2]}")
                    if selected_option.colour == "red": 
                        player.add_money(selected_option.give_money + traders[3])
                        my_logger(player, message = f"Red ship (+Trader) {selected_option.give_money} + {traders[3]}")
                    if selected_option.colour == "yellow": 
                        player.add_money(selected_option.give_money + traders[4])
                        my_logger(player, message = f"Yellow ship (+Trader) {selected_option.give_money} + {traders[4]}")

                    table.remove_card_to_table(selected_option)
                    table.add_card_to_waste(selected_option)
                    if first_player == False: 
                        game.order_of_play[0].add_money(1)
                        my_logger(game.order_of_play[0], message = "Subsequant player took a ship")
                        player.add_money(-1)
                        my_logger(player, message = "Ship (+Trader)")
                    print("You took a ship worth ☼%i, you now have ☼%i" %(selected_option.give_money, player.money))
                    logging.info("%s took %s worth %i, and now have %i" %(player.name, selected_option.name, selected_option.give_money, player.money))
                    break
                
                # check if drawn card is not ship, and if player has enough money to buy
                elif player.money >= selected_option.price - discount + second_player:
                    # pay for the card you bought
                    cost_of_card = 0 - (selected_option.price - discount)
                    player.add_money(cost_of_card)
                    if first_player == False: 
                        game.order_of_play[0].add_money(1)
                        my_logger(game.order_of_play[0], message = "Subsequant player took a functional card")
                        player.add_money(-1)
                        my_logger(player, message = "Functional card on %s someone's round - %s" %(game.order_of_play[0].name, selected_option.name))
                    else:
                        my_logger(player, message = "Functional card - %s" %(selected_option.name))


                    # add any cards benefits to the players hand
                    if isinstance(selected_option, Vrou): 
                        player.add_discount(1)
                        my_logger(player, message = f"Bought a Vrou for {selected_option.price}")
                    if isinstance(selected_option, Governor): 
                        player.add_extra_card_perm()
                        my_logger(player, message = f"Bought a Govenor for {selected_option.price}")

                    # missing if-statements??????????????????

                    # Add VP to the player who bought the cards
                    print(tc("Victory Points!!", color= "white", on_color="on_red"))
                    player.add_vp(selected_option.vp)

                    # add card to hand by removing card from table
                    player.add_card_to_hand(selected_option)
                    table.remove_card_to_table(selected_option)

                    game_status = end_of_game(game) # check if game has finished or not

                    print("You took %s worth %svp, you now have %ivp" %(selected_option.name, selected_option.vp, player.vp))
                    logging.info("%s took %s worth %svp, and now have %ivp" %(player.name, selected_option.name, selected_option.vp, player.vp))
                    break
                else:
                    print("You don't have enough money, try another card")
                    logging.info("%s selected invalid card from table" %(player.name))
            
            elif choice == 0:   # player choose to skip turn
                break
            
            elif choice == 999:
                print(tc("Here is your cards:", color="green"))
                for card in player.cards:
                    print("%s" %(card.name))


            else:
                print("Invalid choice. Please enter a valid number.")

        except ValueError:
            print(f"Invalid input. Please enter an integer between 0 and {len(options)}.")

    report_player_status(player) # Only for debugging

    return game_status


def check_ship_amount(table:Table, player: Player):
    """Check table for more than 4 ships and give extra draws to the current player

    Args:
        table (Table): Game table
        palyer (Player): Current player
    """
    number_of_ships = 0
    player.extra_card_temp = 0
    for card in table.cards_on_table:
        if isinstance(card, Ship):
            number_of_ships += 1
    if number_of_ships == 4: 
        player.add_extra_card_temp()
    elif number_of_ships == 5: 
        player.add_extra_card_temp()
        player.add_extra_card_temp()

def check_expedition(player: Player, table: Table) ->list:
    """Check if player can trade in for an expedition

    Args:
        player (Player): Current player 
        table (Table): Table of cards
    Returns:
        list: expedition cards that the player can buy
    """

    # Build player code, then check against all expedition cards
    posible_expedition_cards = []
    code1, code2, code3 = 0, 0, 0
    full_code = str(code1) + str(code2) + str(code3)

    for card in player.cards:
        if isinstance(card, SettlerCaptainPriest):
            if card.name == "captain": code1 += 1
            if card.name == "priest": code2 += 1
            if card.name == "settler": code3 += 1
            full_code = str(code1) + str(code2) + str(code3)
    #print("Player code: %s" %full_code)

    for expedition in table.expeditions:
        #print(f"Exped value: {code1}{code2}{code3}")
        #print(f"Table value: {expedition.code1 - code1}{expedition.code2 - code2}{expedition.code3 - code3}")
        if (expedition.code1 - code1 <= 0 and expedition.code2 - code2 <= 0 and expedition.code3 - code3 <= 0):
            #print("append card")
            posible_expedition_cards.append(expedition)



    return posible_expedition_cards 



def end_of_game(game: Game)->list:
    """The end of the is trigger when a player reach 12vp

    Args:
        game (Game): The current game

    Returns:
        list: [True/False, winner]
    """
    game_finish = False
    winner = ""

    for player in game.players:
        if player.vp >= 12:
            game_finish = True
            winner = player.name

    return game_finish, winner        



def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')



def report_player_status(player: Player):
    """Function for reporting player status

    Args:
        player (Player): Current player
    """
    '''
    ic(player.name)
    ic(player.money)
    ic(player.vp)
    ic(player.discount)
    ic(player.defence)
    ic(player.extra_card_perm)
    ic(len(player.cards))

    for card in player.cards:
        ic(card.name)
        ic(card.vp)
        if isinstance(card, SailorPirate): ic(card.defence)

        '''
    pass










