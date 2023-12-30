
from src.card import Admiral, Witzbold, Vrou, SailorPirate, SettlerCaptainPriest, Trader
from src.card import Governor, Ship, Tax, Expedition
from src.card import DeckOfCards

def test_admiral():
    card1 = Admiral(5)
    card2 = Admiral(7)
    card3 = Admiral(9)
    assert card1.price == 5; card1.vp == 1; card2.price == 7; card2.vp == 2; card3.price == 9; card3.vp == 3

def test_witzbold():
    card1 = Witzbold(7)
    card2 = Witzbold(9)
    assert card1.price == 7; card1.vp == 2; card2.price == 9; card2.vp == 3

def test_vrou():
    card1 = Vrou(7)
    card2 = Vrou(9)
    assert card1.price == 7; card1.vp == 2; card1.discount == -1; card2.price == 9; card2.vp == 3; card2.discount == -1

def test_number_of_ships():
    doc = DeckOfCards()
    doc.create_deck()
    # Create a new list containing instances of the Ship class
    ship_instances = [item for item in doc.cards if isinstance(item, Ship)]
    # Use a list comprehension to find all ships of a colour
    black_ships = [ship for ship in ship_instances if ship.colour == "black"]
    red_ships = [ship for ship in ship_instances if ship.colour == "red"]
    blue_ships = [ship for ship in ship_instances if ship.colour == "blue"]
    yellow_ships = [ship for ship in ship_instances if ship.colour == "yellow"]
    green_ships = [ship for ship in ship_instances if ship.colour == "green"]

    assert len(black_ships) == 10; len(red_ships) == 10; len(blue_ships) == 10; len(yellow_ships) == 10; len(green_ships)


def test_number_of_individual_cards():
    doc = DeckOfCards()
    doc.create_deck()
    
    # Create a new list containing instances of Cards
    ship_instances = len([item for item in doc.cards if isinstance(item, Ship)])
    admiral_instances = len([item for item in doc.cards if isinstance(item, Admiral)])
    trader_instances = len([item for item in doc.cards if isinstance(item, Trader)])
    scp_instances = len([item for item in doc.cards if isinstance(item, SettlerCaptainPriest)])
    sp_instances = len([item for item in doc.cards if isinstance(item, SailorPirate)])
    vrou_instances = len([item for item in doc.cards if isinstance(item, Vrou)])
    witzbold_instances = len([item for item in doc.cards if isinstance(item, Witzbold)])
    governor_instances = len([item for item in doc.cards if isinstance(item, Governor)])
    expedition_instances = len([item for item in doc.cards if isinstance(item, Expedition)])
    tax_instances = len([item for item in doc.cards if isinstance(item, Tax)])



    assert ship_instances == 50; admiral_instances == 6; trader_instances == 10; scp_instances == 18
    assert sp_instances == 13; vrou_instances == 4; witzbold_instances == 5; governor_instances == 4
    assert expedition_instances == 6; tax_instances == 6

