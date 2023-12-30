
from src.card import Card, DeckOfCards
from src.game import Game
from src.table import Table

def test_create_game():
    doc = DeckOfCards()
    doc.create_deck()
    game = Game(doc)
    game.add_player("Test Player1")
    game.add_player("Test Player2")

    assert isinstance(game, Game) == True; game.number_of_players == 2; game.players[0] == "Test Player1" ; game.players[1] == "Test Player2"

def test_shuffle_cards():
    doc = DeckOfCards()
    doc.create_deck()
    game = Game(doc)
    table = Table()

    game.shuffle_cards(table)
    
    assert game.deck_of_cards == []