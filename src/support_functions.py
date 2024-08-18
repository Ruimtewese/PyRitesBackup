
import logging
import os
import datetime
from src.players import Player
from termcolor import colored as tc # Import termcolor module

def clear_log_files(folder_path: str, files) -> None:
    """
    Clear all *.log files in a given directory.

    This function iterates through the provided collection of files and checks if each file
    has a '.log' extension. If a '.log' file is found, it constructs the full file path using
    the provided folder path and the file name, and then removes the file.

    Args:
        folder_path (str): The path to the directory where the log files are located.
        files (collection of files): A collection of file names in the specified directory.

    Returns:
        None: The function does not return any value. It only prints a message indicating that all log files have been cleared.
    """

    # Iterate through the files and delete *.log files
    for file in files:
        if file.endswith(".log"):
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
    
    print("Clear all log files")

def my_logger(a_player:Player, message = "")-> None:
    """
    Simple function to do logging to specific players logger.

    Args:
        a_player (Player): The player object for which the logging is being done.
        message (str): An optional message to be logged along with the player's data. Default is an empty string.

    Returns:
        None: The function does not return any value. It logs the player's data and any provided message to a specific logger.
    """
    
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    id = a_player.id
    name = a_player.name
    money = a_player.money
    vp = a_player.vp
    defence = a_player.defence
    discount = a_player.discount
    extra_card_temp = a_player.extra_card_temp    # more than 3 coloured ships
    extra_card_perm = a_player.extra_card_perm 
    cards = a_player.cards

    logger = logging.getLogger(f'{current_date}_{id}_{name}_logger')
    
    logger.info(f'{money}\t{vp}\t{defence}\t{discount}\t{extra_card_perm}\t{extra_card_temp}\t{message}')
    
    for card in cards:
        logger.info(f'-------------------- {card.name}\t')

def splash_screen():
    """
    Display a splash screen with a stylized game title using the termcolor module.

    The splash screen displays a visually appealing ASCII art representation of the game title.
    The title is printed in red color using the termcolor module.

    Parameters:
    None

    Returns:
    None
    """     
    print(tc("██████╗░██╗░░░██╗██████╗░░█████╗░████████╗███████╗░██████╗", color="red"))
    print(tc("██╔══██╗╚██╗░██╔╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔════╝", color="red"))
    print(tc("██████╔╝░╚████╔╝░██████╔╝███████║░░░██║░░░█████╗░░╚█████╗░", color="red"))
    print(tc("██╔═══╝░░░╚██╔╝░░██╔══██╗██╔══██║░░░██║░░░██╔══╝░░░╚═══██╗", color="red"))
    print(tc("██║░░░░░░░░██║░░░██║░░██║██║░░██║░░░██║░░░███████╗██████╔╝", color="red"))
    print(tc("╚═╝░░░░░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═════╝░", color="red"))
    


def print_color(message, color1):
    """
    Print a colored message to the console using the termcolor module.

    This function takes a message and a color as input and prints the message to the console
    in the specified color using the termcolor module.

    Parameters:
    message (str): The text message to be printed.
    color1 (str): The color in which the message should be printed. The color should be one of the
        available text colors or highlights provided by the termcolor module.

    Returns:
    None: The function does not return any value. It only prints the colored message to the console.
    """
    print(tc(message, color=color1))
        
