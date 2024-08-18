# constants.py
import pygame

# Window dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 1400, 900

# Font sizes
BASE_FONT_SIZE = 36

# UI Elements
BUTTON = pygame.Rect(200, 500, 200, 50)
BUTTON_CENTER = pygame.Rect((WINDOW_WIDTH - 200) / 2, (WINDOW_HEIGHT - 50) / 2, 200, 50)

# Menu
MENU_ITEMS = ["File", "Edit", "Help"]
MENU_COLOUR = (30, 30, 30)
MENU_ITEM_HOVER_COLOUR = (50, 50, 50)

# Colours
BUTTON_COLOUR = (0, 200, 0)
BUTTON_HOVER_COLOUR = (0, 255, 0)
WHITE = (255, 255, 255)
TEXTBOX_COLOUR_ACTIVE = (0, 255, 255)
TEXTBOX_COLOUR_INACTIVE = (50, 50, 50)

# Splash screen data
SPLASH_TEXT = "pyRites - Welcome to PyRites"
SPLASH_IMAGE = 'images/pyRites.png'

# Splash screen data
PLAYER_TEXT = "pyRites -Player name input"
PLAYER_IMAGE = 'images/pyRites.png'

