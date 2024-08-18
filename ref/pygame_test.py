import pygame
import sys
import os

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1400, 900
BASE_FONT_SIZE = 36
BUTTON = pygame.Rect(300, 500, 200, 50)
MENU_ITEMS = ["File", "Edit", "Help"]
MENU_COLOUR = (30, 30, 30)
MENU_ITEM_HOVER_COLOUR = (50, 50, 50)
BUTTON_COLOUR = (0, 200, 0)
BUTTON_HOVER_COLOUR = (0, 255, 0)
WHITE = (255, 255, 255)
TEXTBOX_COLOUR_ACTIVE = (0, 255, 255)
TEXTBOX_COLOUR_INACTIVE = (50, 50, 50)

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
    window.blit(button_text_surface, (button.x + 50, button.y + 10))

def slash_screen_window():
    """
    Initial screen before player input.

    This function sets up the initial game window, displays a menu, and a start button.
    It handles user input for menu item selection and button click events.

    Parameters:
    None

    Returns:
    None
    """
    window = init_pygame("Welcome to PyRites", 'images/port_royal.png')
    base_font = pygame.font.Font(None, BASE_FONT_SIZE)
    menu_items = MENU_ITEMS
    menu_rects = [pygame.Rect(i * 100, 0, 100, 50) for i in range(len(menu_items))]
    button = BUTTON
    button_text = "Start"

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
        draw_button(window, base_font, button, button_text, button.collidepoint(pygame.mouse.get_pos()))
        pygame.display.update()

def player_input():
    """
    Get player names and confirm.

    This function initializes a game window, displays a menu, and textboxes for player names.
    It handles user input for menu item selection, textbox focus, and button click events.
    When the 'Confirm' button is clicked, it writes the non-empty player names to a file and prints the number of players.

    Parameters:
    None

    Returns:
    None
    """
    window = init_pygame("Player name input", 'images/port_royal.png')
    base_font = pygame.font.Font(None, BASE_FONT_SIZE)
    menu_items = MENU_ITEMS
    menu_rects = [pygame.Rect(i * 100, 0, 100, 50) for i in range(len(menu_items))]
    textboxes = [pygame.Rect(300, 100 + i * 60, 400, 50) for i in range(5)]
    labels = [f"Player {i+1}" for i in range(5)]
    player_names = ["", "", "", "", ""]
    active_textbox = 0
    button = BUTTON
    button_text = "Confirm"

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
                    confirmed = True

            if event.type == pygame.KEYDOWN and not confirmed:
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
        for i, textbox in enumerate(textboxes):
            pygame.draw.rect(window, TEXTBOX_COLOUR_ACTIVE if i == active_textbox else TEXTBOX_COLOUR_INACTIVE, textbox)
            label_surface = base_font.render(labels[i], True, WHITE)
            window.blit(label_surface, (textbox.x - 150, textbox.y + 10))
            text_surface = base_font.render(player_names[i], True, WHITE)
            window.blit(text_surface, (textbox.x + 5, textbox.y + 10))
        draw_button(window, base_font, button, button_text, button.collidepoint(pygame.mouse.get_pos()))
        pygame.display.update()

        if confirmed:
            non_empty_names = [name for name in player_names if name.strip()]
            os.makedirs('output', exist_ok=True)  # Ensure the output directory exists
            try:
                with open('output/player_names.txt', 'w') as f:
                    for name in non_empty_names:
                        f.write(f"{name}\n")
                print(f"Number of players with names: {len(non_empty_names)}")
            except IOError as e:
                print(f"Failed to write to file: {e}")

            window.fill((0, 0, 0))
            pygame.display.update()
            pygame.time.wait(2000)
            running = False

if __name__ == "__main__":
    slash_screen_window()
    player_input()
