import msvcrt
import time
from src.func import (report_drawn_card, end_of_round, tax_card_is_drawn, expedition_card_is_drawn,
                      ship_card_is_drawn, is_valid_card_on_table, select_card_from_table, 
                      check_ship_amount, admiral_check, check_expedition)
from src.func import clear_terminal
import pygame
from src.ui import init_pygame
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, BASE_FONT_SIZE, BUTTON, MENU_ITEMS, \
    MENU_COLOUR, MENU_ITEM_HOVER_COLOUR, BUTTON_COLOUR, BUTTON_HOVER_COLOUR, WHITE, \
    TEXTBOX_COLOUR_ACTIVE, TEXTBOX_COLOUR_INACTIVE

def play_game(game, table, players):
    """
    Handles the game flow including player turns and card draws.
    
    Parameters:
    game (Game): The Game object.
    table (Table): The Table object.
    players (list): List of Player objects.
    """
    window = init_pygame("Playing table", 'images/port_royal.png')
    base_font = pygame.font.Font(None, BASE_FONT_SIZE)
    menu_items = MENU_ITEMS
    menu_rects = [pygame.Rect(i * 100, 0, 100, 50) for i in range(len(menu_items))]
    window.fill((0, 0, 0))

    print(f"Active player: {game.players[0].name} press 'enter' to draw a card")
    playing = True
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
            result3 = ship_card_is_drawn(drawn_card, table, players[0], game)

            if not result3:
                print("------------------------------------------------------------------")
                game.change_order_of_play()
                time.sleep(2)
                clear_terminal()
                end_of_round(game, table)
                print(f"{game.order_of_play[0].name} to start the next round")
                continue

            if result1 and result2 and result3:
                table.add_card_to_table(drawn_card)

            is_valid = is_valid_card_on_table(table, players[0])

        elif char == b'\x1b' and is_valid:  # Esc key
            handle_esc_key(game, table, players[0])

        elif char == b'q':  # 'q' key
            handle_q_key(table, players[0])

        elif char == b'w':  # 'w' key
            handle_w_key(players[0])

        else:
            print("Invalid input - press 'enter' to draw a card, 'q' to look at the expedition area, and 'esc' to stop")

    print('We have a winner!!!')

def handle_esc_key(game, table, player):
    """
    Handles actions when the Esc key is pressed.
    
    Parameters:
    game (Game): The Game object. This object contains the game state, deck of cards, and players.
    table (Table): The Table object. This object represents the game table where cards are placed during the game.
    player (Player): The current Player object. This object represents the player who pressed the Esc key.

    Returns:
    None. The function does not return any value. It performs actions based on the game state and player input.
    """
    print("You pressed Esc. You may now select a card")
    for a_player in game.order_of_play:
        admiral_check(table, a_player)
        check_ship_amount(table, a_player)

        cards_to_draw = a_player.extra_card_temp + a_player.extra_card_perm + 1
        print(f"---------->  number of cards to draw: {cards_to_draw}")
        for draw in range(cards_to_draw):
            print(f"---------->  draw number: {draw + 1}")
            game_status = select_card_from_table(table, a_player, game, draw)
            if game_status[0]:
                break

        print("------------------------------------------------------------------")

    print("------------------------------------------------------------------")
    game.change_order_of_play()
    time.sleep(2)
    clear_terminal()
    end_of_round(game, table)

def handle_q_key(table, player):
    """
    Handles actions when the 'q' key is pressed.
    
    Parameters:
    table (Table): The Table object representing the game table where cards are placed during the game.
    player (Player): The current Player object representing the player who pressed the 'q' key.

    Prints the expeditions in the expedition area, checks if the player qualifies for any expeditions,
    and allows the player to select an expedition card to swap. If the player does not qualify,
    it prints a message indicating that they do not have the right cards to swap for expeditions.
    """
    print("The expedition area contains the following expeditions:")
    for index, cards in enumerate(table.expeditions, start=1):
        print(f'{index}. Symbols: {cards.symbols} vp: {cards.vp}')

    qualify_for_these = check_expedition(player, table)
    if qualify_for_these:
        print("You qualify for the following expeditions:")
        for index, cards in enumerate(qualify_for_these, start=1):
            print(f'{index}. Symbols: {cards.symbols} vp: {cards.vp}')

        choice = int(input(f"{player.name} select a card: "))
        print("0. Not interested yet")
        if 1 <= choice <= len(qualify_for_these):
            selected_option = qualify_for_these[choice - 1]
            player.add_card_to_hand(selected_option)
            player.add_money(selected_option.give_money)
            table.remove_card_to_expeditions(selected_option)
        elif choice == 0:
            pass
        else:
            print("Select a valid option")
    else:
        print("You do not have the right cards to swap for expeditions")

def handle_w_key(player):
    """
    Handles actions when the 'w' key is pressed. This function prints the names of all the cards
    in the player's hand.
    
    Parameters:
    player (Player): The current Player object. This object represents the player who pressed the 'w' key.
                      The Player object has an attribute 'cards' which is a list of Card objects.

    Returns:
    None. The function does not return any value. It prints the names of the player's cards.
    """
    print("You want to see your cards?")
    for card in player.cards:
        print(card.name)
