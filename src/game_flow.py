import msvcrt
import time
from src.func import (report_drawn_card, end_of_round, tax_card_is_drawn, expedition_card_is_drawn,
                      ship_card_is_drawn, is_valid_card_on_table, select_card_from_table, 
                      check_ship_amount, admiral_check, check_expedition)
from src.func import clear_terminal
import pygame
from src.ui import init_pygame, draw_menu
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, BASE_FONT_SIZE, BUTTON, MENU_ITEMS, \
    MENU_COLOUR, MENU_ITEM_HOVER_COLOUR, BUTTON_COLOUR, BUTTON_HOVER_COLOUR, WHITE, \
    TEXTBOX_COLOUR_ACTIVE, TEXTBOX_COLOUR_INACTIVE

from src.constants import GAME_TEXT, GAME_IMAGE, BASE_FONT_SIZE_HALF, MENU_HEIGHT, MENU_WIDTH


def play_game(game, table, players):
    """
    Handles the game flow including player turns and card draws.
    
    Parameters:
    game (Game): The Game object.
    table (Table): The Table object.
    players (list): List of Player objects.
    """
    window = init_pygame(GAME_TEXT, GAME_IMAGE)
    base_font = pygame.font.Font(None, BASE_FONT_SIZE)
    menu_items = MENU_ITEMS
    menu_rects = [pygame.Rect(i * MENU_WIDTH, 0, MENU_WIDTH, MENU_HEIGHT) for i in range(len(menu_items))]

    # Load the image
    image = pygame.image.load(GAME_IMAGE)  # Update with your image path
    image = pygame.transform.scale(image, (image.get_width() // 3, image.get_height() // 3))

    # Calculate image rectangle position for top-right corner
    image_rect = image.get_rect(
        topright=(window.get_width() - 10, 10))  # Adjust the position slightly from the edges

    window.fill((0, 0, 0))
    draw_menu(window, base_font, menu_items, menu_rects)
    window.blit(image, image_rect)  # Draw the image on the window

    # Draw horizontal white line in the center of the screen
    center_y = window.get_height() // 2
    horizontal_margin = 20  # Distance from the screen edge
    pygame.draw.line(window, (255, 255, 255), (horizontal_margin, center_y), (window.get_width() - horizontal_margin, center_y), 2)

    # Draw vertical white line from the left edge of the image to the horizontal line
    vertical_margin = 20  # Distance from the image and horizontal line
    image_left_x = image_rect.left
    image_left_y = image_rect.top + image_rect.height + vertical_margin
    pygame.draw.line(window, (255, 255, 255), (image_left_x, image_left_y), (image_left_x, center_y - vertical_margin), 2)

    # Render and draw the expedition box
    text_margin = 20
    text_font = pygame.font.Font(None, BASE_FONT_SIZE_HALF)  # Font size 36 for "Expeditions"
    text_surf = text_font.render("Expeditions", True, (255, 255, 255))  # Render the text
    text_rect = text_surf.get_rect(center=(image_rect.left + image_rect.width // 2, image_rect.bottom + text_margin))  # Centered below the image
    window.blit(text_surf, text_rect)  # Draw the text on the window

    # Draw six grey rectangles in two rows of three, equally spaced between the first vertical line and the edge of the screen
    num_rows = 2
    num_columns = 3
    rect_height = 30  # Height of each rectangle
    first_line_x = image_left_x
    rect_margin = 10  # Margin from the vertical line and rectangles
    row_spacing = 20  # Spacing between rows
    column_spacing = 10  # Spacing between columns

    # Calculate the total available width for rectangles
    available_width = window.get_width() - first_line_x - rect_margin
    # Calculate the width of each rectangle based on the available width, column spacing, and margins
    total_spacing = (num_columns - 1) * column_spacing + 2 * rect_margin
    rect_width = (available_width - total_spacing) / num_columns

    # Calculate spacing including margins
    spacing_x = column_spacing + rect_width

    for i in range(num_rows):  # For two rows
        for j in range(num_columns):  # For three rectangles per row
            x_pos = first_line_x + rect_margin + j * spacing_x
            y_pos = image_rect.bottom + 50 + i * (rect_height + row_spacing)  # Positioned in rows with spacing
            rect = pygame.Rect(x_pos, y_pos, rect_width, rect_height)  # Create rectangle
            pygame.draw.rect(window, (128, 128, 128), rect)  # Draw grey rectangle




    # Render and draw the text "Hallo world" at the top-left corner
    menu_margin = 10
    top_left_font = pygame.font.Font(None, BASE_FONT_SIZE_HALF)  # Font size 36 for "Hallo world"
    top_left_text_surf = top_left_font.render("Playing table", True, (255, 255, 255))  # Render the text
    top_left_text_rect = top_left_text_surf.get_rect(topleft=(10, MENU_HEIGHT + menu_margin))  # Positioned at top-left corner with padding
    window.blit(top_left_text_surf, top_left_text_rect)  # Draw the text on the window

    # Render and draw the text "Hallo world" at the top-left corner
    menu_margin = 10
    top_left_font = pygame.font.Font(None, BASE_FONT_SIZE_HALF)  # Font size 36 for "Hallo world"
    top_left_text_surf = top_left_font.render("Playing table", True, (255, 255, 255))  # Render the text
    top_left_text_rect = top_left_text_surf.get_rect(topleft=(10, MENU_HEIGHT + menu_margin))  # Positioned at top-left corner with padding
    window.blit(top_left_text_surf, top_left_text_rect)  # Draw the text on the window

    # Draw four equally spaced vertical lines from the horizontal line to the bottom of the screen
    num_lines = 4
    player_margin = 20  # Margin from the edge of the screen
    line_spacing = (window.get_width() - 2 * player_margin) / (num_lines + 1)  # Calculate spacing between lines
    
    for i in range(1, num_lines + 1):
        x_pos = player_margin + i * line_spacing
        pygame.draw.line(window, (255, 255, 255), (x_pos, center_y + player_margin), (x_pos, window.get_height() - player_margin), 2)

    # Render and draw five equally spaced text labels "Captain X" below the horizontal line
    num_labels = 5
    label_font = pygame.font.Font(None, BASE_FONT_SIZE_HALF)  # Font size 36 for "Captain X"
    label_margin = 10  # Margin from the horizontal line and text

    # Calculate spacing between labels
    label_spacing = (window.get_width() - 2 * label_margin) / (num_labels)
    for i in range(num_labels):
        label_surf = label_font.render(f"Captain {i + 1}", True, (255, 255, 255))  # Render the text
        x_pos = label_margin + i * label_spacing + label_spacing // 2
        y_pos = center_y + label_margin + label_surf.get_height()
        label_rect = label_surf.get_rect(center=(x_pos, y_pos))
        window.blit(label_surf, label_rect)  # Draw the label on the window























    pygame.display.update()







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
