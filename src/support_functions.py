
import logging
import os
import datetime
from src.players import Player
from termcolor import colored as tc # Import termcolor module

def clear_log_files(folder_path: str, files):
    """Funnction to clear all *.log files in a given directory
    Args:
        folder_path (str): foldr path
        files (collection of files): all the files in this locations
    """

    # Iterate through the files and delete *.log files
    for file in files:
        if file.endswith(".log"):
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
    
    print("Clear all log files")

def my_logger(a_player:Player, message = "")-> None:
    """Simple function to do logging to specific players logger

    Args:
        index (int): Player index number
        a_player (Player): The player
        message (str): _description_
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
    """     
    print(tc("██████╗░██╗░░░██╗██████╗░░█████╗░████████╗███████╗░██████╗", color="red"))
    print(tc("██╔══██╗╚██╗░██╔╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔════╝", color="red"))
    print(tc("██████╔╝░╚████╔╝░██████╔╝███████║░░░██║░░░█████╗░░╚█████╗░", color="red"))
    print(tc("██╔═══╝░░░╚██╔╝░░██╔══██╗██╔══██║░░░██║░░░██╔══╝░░░╚═══██╗", color="red"))
    print(tc("██║░░░░░░░░██║░░░██║░░██║██║░░██║░░░██║░░░███████╗██████╔╝", color="red"))
    print(tc("╚═╝░░░░░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═════╝░", color="red"))
    


def print_color(message, color1):
    """Available text colors:
    black, red, green, yellow, blue, magenta, cyan, white, light_magenta, light_cyan,
      light_grey,dark_grey, light_red, light_green, light_yellow, light_blue 

Available text highlights:
    on_black, on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white,
      on_light_grey, on_dark_grey, on_light_red, on_light_green, on_light_yellow,
       on_light_blue, on_light_magenta, on_light_cyan.
    """
    print(tc(message, color=color1))
        
