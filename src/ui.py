import pygame
import sys
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, BASE_FONT_SIZE, BUTTON, \
                            BUTTON_CENTER, MENU_ITEMS, MENU_COLOUR, MENU_ITEM_HOVER_COLOUR, \
                            BUTTON_COLOUR, BUTTON_HOVER_COLOUR, WHITE, \
                            TEXTBOX_COLOUR_ACTIVE, TEXTBOX_COLOUR_INACTIVE

from src.constants import SPLASH_TEXT, SPLASH_IMAGE
from src.constants import PLAYER_TEXT, PLAYER_IMAGE, MENU_HEIGHT, MENU_WIDTH

def init_pygame(window_title, icon_path):
    """
    Initialise Pygame, set up the window, and load the icon.

    Parameters:
    window_title (str): The title to be displayed on the window.
    icon_path (str): The file path to the icon image.

    Returns:
    pygame.Surface: The window surface created by Pygame.

    Raises:
    pygame.error: If the icon file is not found or cannot be loaded.
    """
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(window_title)

    try:
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
    except pygame.error:
        print("Icon file not found or couldn't be loaded.")
    
    return window

def draw_menu(window, base_font, menu_items, menu_rects):
    """
    Draw the menu items on the window.

    Parameters:
    window (pygame.Surface): The window surface created by Pygame.
    base_font (pygame.font.Font): The font object used to render the menu items.
    menu_items (list[str]): A list of strings representing the menu items to be displayed.
    menu_rects (list[pygame.Rect]): A list of rectangles representing the positions and sizes of the menu items.

    Returns:
    None
    """
    pygame.draw.rect(window, MENU_COLOUR, (0, 0, WINDOW_WIDTH, 50))
    for i, rect in enumerate(menu_rects):
        if rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, MENU_ITEM_HOVER_COLOUR, rect)
        menu_text_surface = base_font.render(menu_items[i], True, WHITE)
        window.blit(menu_text_surface, (rect.x + 10, rect.y + 10))

def draw_button(window, base_font, button, button_text, is_hovered):
    """
    Draw the button on the window.

    Parameters:
    window (pygame.Surface): The window surface created by Pygame.
    base_font (pygame.font.Font): The font object used to render the button text.
    button (pygame.Rect): The rectangle representing the position and size of the button.
    button_text (str): The text to be displayed on the button.
    is_hovered (bool): A flag indicating whether the mouse cursor is currently hovering over the button.

    Returns:
    None
    """
    button_colour = BUTTON_HOVER_COLOUR if is_hovered else BUTTON_COLOUR
    pygame.draw.rect(window, button_colour, button)
    button_text_surface = base_font.render(button_text, True, WHITE)


    # Get the text and button dimensions
    text_width, text_height = button_text_surface.get_size()
    button_width, button_height = button.size

    # Calculate the position to centre the text
    text_x = button.x + (button_width - text_width) // 2
    text_y = button.y + (button_height - text_height) // 2

    # Draw the text on the button
    window.blit(button_text_surface, (text_x, text_y))

    #window.blit(button_text_surface, (button.x + 50, button.y + 10))

def splash_screen_window():
    """
    Initial screen before player input.

    This function sets up the initial game window, displays a menu, and a start button.
    It handles user input for menu item selection and button click events.

    Parameters:
    None

    Returns:
    None
    """
    window = init_pygame(SPLASH_TEXT, SPLASH_IMAGE)
    base_font = pygame.font.Font(None, BASE_FONT_SIZE)
    menu_items = MENU_ITEMS
    menu_rects = [pygame.Rect(i * MENU_WIDTH, 0, MENU_WIDTH, MENU_HEIGHT) for i in range(len(menu_items))]
    button = BUTTON_CENTER
    button_text = "Start"

    # Load the image
    image = pygame.image.load(SPLASH_IMAGE)  # Update with your image path
    image_rect = image.get_rect(center=(window.get_width() // 2, window.get_height() // 2))


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, rect in enumerate(menu_rects):
                    if rect.collidepoint(mouse_pos):
                        print(f"{menu_items[i]} menu clicked!")

                if button.collidepoint(mouse_pos):
                    running = False

        window.fill((0, 0, 0))
        draw_menu(window, base_font, menu_items, menu_rects)
        window.blit(image, image_rect)  # Draw the image on the window
        draw_button(window, base_font, button, button_text, button.collidepoint(pygame.mouse.get_pos()))
        pygame.display.update()

def player_input():
    """
    This function handles the player name input window. It displays a series of textboxes for the players to enter their names,
    and a confirm button to proceed. The function also handles user input, such as keyboard events and mouse clicks, to update
    the textbox contents and trigger the confirm action.

    Parameters:
    None

    Returns:
    list: A list of strings representing the player names entered by the user. The list may contain empty strings if the user
          did not enter a name for a particular player.
    """

    window = init_pygame(PLAYER_TEXT, PLAYER_IMAGE)
    base_font = pygame.font.Font(None, BASE_FONT_SIZE)
    menu_items = MENU_ITEMS
    menu_rects = [pygame.Rect(i * MENU_WIDTH, 0, MENU_WIDTH, MENU_HEIGHT) for i in range(len(menu_items))]

    textboxes = [pygame.Rect(200, 100 + i * 60, 400, 50) for i in range(5)]
    labels = [f"Captain {i+1}" for i in range(5)]
    player_names = ["", "", "", "", ""]
    active_textbox = 0
    button = BUTTON
    button_text = "Confirm"

    # Load the image
    image = pygame.image.load(PLAYER_IMAGE)  # Update with your image path
    image = pygame.transform.scale(image, (image.get_width() // 3, image.get_height() // 3))

    # Calculate image rectangle position for top-right corner
    image_rect = image.get_rect(
        topright=(window.get_width() - 10, 10))  # Adjust the position slightly from the edges
    
    # image_rect = image.get_rect(center=(window.get_width() // 2, window.get_height() // 2))

    warning_text = ""
    warning_font = pygame.font.Font(None, 24)  # Font for warning message

    confirmed = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, rect in enumerate(menu_rects):
                    if rect.collidepoint(mouse_pos):
                        print(f"{menu_items[i]} menu clicked!")

                for i, textbox in enumerate(textboxes):
                    if textbox.collidepoint(event.pos):
                        active_textbox = i

                if button.collidepoint(event.pos):
                    non_empty_names = [name for name in player_names if name.strip()]
                    if len(non_empty_names) >= 2:
                        confirmed = True
                    else:
                        warning_text = "Please enter at least two player names."

            if event.type == pygame.KEYDOWN and not confirmed:
                warning_text = ""
                if active_textbox < len(player_names):
                    if event.key == pygame.K_TAB:
                        active_textbox = (active_textbox + 1) % len(textboxes)
                    elif event.key == pygame.K_BACKSPACE:
                        player_names[active_textbox] = player_names[active_textbox][:-1]
                    elif event.key == pygame.K_RETURN:
                        if player_names[active_textbox].strip() or active_textbox == len(player_names) - 1:
                            active_textbox += 1
                    else:
                        player_names[active_textbox] += event.unicode

        window.fill((0, 0, 0))
        draw_menu(window, base_font, menu_items, menu_rects)
        window.blit(image, image_rect)  # Draw the image on the window
        for i, textbox in enumerate(textboxes):
            pygame.draw.rect(window, TEXTBOX_COLOUR_ACTIVE if i == active_textbox else TEXTBOX_COLOUR_INACTIVE, textbox)
            label_surface = base_font.render(labels[i], True, WHITE)
            window.blit(label_surface, (textbox.x - 150, textbox.y + 10))
            text_surface = base_font.render(player_names[i], True, WHITE)
            window.blit(text_surface, (textbox.x + 5, textbox.y + 10))
        draw_button(window, base_font, button, button_text, button.collidepoint(pygame.mouse.get_pos()))

        # Display the warning message if needed
        if warning_text:
            warning_surface = warning_font.render(warning_text, True, (255, 0, 0))  # Red colour for warning
            window.blit(warning_surface, (200, 450))

        pygame.display.update()

        if confirmed:
            try:
                with open('output/player_names.txt', 'w') as f:
                    for name in non_empty_names:
                        f.write(f"{name}\n")
                print(f"Number of players with names: {len(non_empty_names)}")
            except IOError as e:
                print(f"Failed to write to file: {e}")

            pygame.quit()  # Close Pygame
            running = False

    return player_names

if __name__ == "__main__":
    splash_screen_window()
    player_input()
