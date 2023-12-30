from src.table import Table
from src.card import DeckOfCards
from src.players import Player
import time
import logging

class Game():
    def __init__(self, cards) -> None:
        self.players = []
        self.number_of_players = len(self.players)
        self.deck_of_cards = cards
        self.order_of_play = []

    def add_player(self, player: Player) -> None:
        """Add a player to the game

        Args:
            player (Player): The player to be added
        """
        self.players.append(player)
        self.order_of_play.append(player)


    def shuffle_cards(self, table: Table):
        """Shuffle the deck of cards

        Args:
            table (Table): Table which contains the waste pile
        """
        print("......................................shuffling deck again......................................")
        time.sleep(2) # Pause for 2 seconds
        for card in table.waste_cards:
            self.deck_of_cards.append(card)
        self.waste_cards = []

    def change_order_of_play(self):
        """Change the order of play by moving the player[0] to the back of the queue 
        """
        self.order_of_play.append(self.order_of_play.pop(0))
        logging.info("--->\t%s \t is the new start player" %(self.order_of_play[0].name))
