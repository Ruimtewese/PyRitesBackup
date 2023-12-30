
from src.card import DeckOfCards

def test_number_of_cards():
    doc = DeckOfCards()
    doc.create_deck()

    assert doc.remaining_cards == 120


