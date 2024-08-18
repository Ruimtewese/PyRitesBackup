from src.players import Player
import logging
import os
import datetime

def create_players(number_of_players, temp_names, folder_path, formatter):
    """
    Creates players, assigns initial money, and sets up logging for each player.
    
    Parameters:
    number_of_players (int): Number of players in the game.
    temp_names (list): List of player names.
    folder_path (str): Path to the folder where player log files are stored.
    formatter (logging.Formatter): Formatter for log files.
    
    Returns:
    list: A list of Player objects.
    """
    players = []
    for index, player_name in enumerate(temp_names[:number_of_players], start=1):
        a_player = Player(index, player_name)
        a_player.add_money(3)
        players.append(a_player)

        log_file_path = os.path.join(folder_path, f'{datetime.datetime.now().strftime("%Y-%m-%d")}_{a_player.id}_{a_player.name}_logger.log')
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        logger = logging.getLogger(f'{datetime.datetime.now().strftime("%Y-%m-%d")}_{a_player.id}_{a_player.name}_logger')
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        logger.info(f'This is the logger file for player {a_player.id}, {a_player.name}')
        logger.info('mo=money, vp=victory points, de=defences, di=discount, pe=permanent, te=temporary, ca=cards, message')
        logger.info('3\t0\t0\t0\t0\t0')

    return players
