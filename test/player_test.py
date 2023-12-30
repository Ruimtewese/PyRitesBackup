from src.card import Admiral, Witzbold, Vrou, SailorPirate, SettlerCaptainPriest, Trader
from src.card import Governor, Ship, Tax, Expedition
from src.card import DeckOfCards
from src.table import Table
from src.players import Player


def test_PlayerClass():

    # Create dummy cards
    a_vrou = Vrou(9)
    a_witzbold = Witzbold(7)
      


        
    # Check the class initiation
    a_player = Player(1, "Bobbejaan")
    assert a_player.id == 1
    assert a_player.name == "Bobbejaan"
    assert a_player.money == 0
    assert a_player.vp == 0
    assert a_player.cards == []
    assert a_player.defence == 0
    assert a_player.discount == 0
    assert a_player.extra_card_temp == 0    # more than 3 coloured ships
    assert a_player.extra_card_perm == 0

    # Test defence
    a_player.add_defence(1)
    assert a_player.defence == 1

    # Test money
    a_player.add_money(1)
    assert a_player.money == 1

    # Add a Vrou to the players hand
    a_player.add_card_to_hand(a_vrou)
    assert len(a_player.cards) == 1
    assert isinstance(a_player.cards[0], Vrou)

    # Add a Witzbold to the players hand
    a_player.add_card_to_hand(a_witzbold)
    assert len(a_player.cards) == 2
    assert isinstance(a_player.cards[0], Vrou)
    assert isinstance(a_player.cards[1], Witzbold)


    # a_player.add_extra_card_perm()

    # a_player.add_extra_card_temp()

    # a_player.add_vp()




