from src.func import check_ship_amount
from src.card import Ship, Vrou, Witzbold, SettlerCaptainPriest, Trader, Admiral, SailorPirate, Governor
from src.table import Table
from src.players import Player


def test_check_ship_amount():

    table = Table()
    player = Player(1, "p1")

    player.reset_extra_card_temp()
    card1 = Ship(2,"red",2)
    table.add_card_to_table(card1)
    check_ship_amount(table, player)
    assert player.extra_card_temp == 0

    player.reset_extra_card_temp()
    card2 = Ship(2,"yellow",2)
    table.add_card_to_table(card2)
    check_ship_amount(table, player)
    assert player.extra_card_temp == 0    

    player.reset_extra_card_temp()
    card3 = Ship(2,"blue",2)
    table.add_card_to_table(card3)
    check_ship_amount(table, player)
    assert player.extra_card_temp == 0    

    player.reset_extra_card_temp()
    card4 = Ship(2,"green",2)
    table.add_card_to_table(card4)
    check_ship_amount(table, player)
    assert player.extra_card_temp == 1    

    player.reset_extra_card_temp()
    card5 = Ship(2,"black",2)
    table.add_card_to_table(card5)
    check_ship_amount(table, player)
    assert player.extra_card_temp == 2   