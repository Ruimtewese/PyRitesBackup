from src.card import DeckOfCards
from src.game import Game
from src.table import Table
from src.setup import configure_logging, setup_game_environment
from src.players_setup import create_players
from src.game_flow import play_game
from src.func import clear_terminal
from src.support_functions import splash_screen

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
    folder_path = setup_game_environment()
    formatter = configure_logging(folder_path)

    # Get number of players
    number_of_players = 2  # Replace with user input if necessary

    # Creating table and deck of cards
    table = Table()
    doc = DeckOfCards()
    doc.create_deck()

    game = Game(doc)
    temp_names = ["Rowland", "Divan"]
    players = create_players(number_of_players, temp_names, folder_path, formatter)
    for player in players:
        game.add_player(player)

    print(f"The following people are playing PyRites:")
    for index, player in enumerate(game.players, start=1):
        print(f"\t {index}. {player.name} has {player.money} money to start.")
    print("Now we are ready to play...")

    print("START GAME")
    play_game(game, table, players)

if __name__ == "__main__":
    clear_terminal()
    splash_screen()
    main()
