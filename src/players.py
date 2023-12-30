
from src.card import Card
from src.money import Money

class Player(Money):
    def __init__(self, id:int, name:str) -> None:
        """ Main Player class

        Args:
            id (int): order of play
            name (str): name of the player
        """
        self.id = id
        self.name = name
        self.money = 0
        self.vp = 0
        self.cards = []
        self.defence = 0
        self.discount = 0
        self.extra_card_temp = 0    # more than 3 coloured ships
        self.extra_card_perm = 0    # in case player have govener(s)

    def add_vp(self, vp:int) -> None:
        """function for adding victory points to a player

        Args:
            vp (int): amount of victory points this player has scored
        """
        self.vp += vp

    def add_money(self, amount:int) -> None:
        """function for adding money to a player's purse

        Args:
            amount (int): amount of money this player has obtained (positive or negative)
        """
        self.money += amount


    def set_money(self, amount:int) -> None:
        """function for setting money in player's purse

        Args:
            amount (int): amount of money this player has
        """
        self.money = amount

    def add_defence(self, defence:int) -> None:
        """function for adding to a player's defence strenght

        Args:
            amount (int): amount of defence this player has obtained (positive or negative)
        """
        self.defence += defence

    def add_card_to_hand(self, card: Card) -> None:
        """function to add a card to a player's hand

        Args:
            card (Card): the card which the player has added to his hand
        """
        self.cards.append(card)

    def remove_card_from_hand(self, card: Card) -> None:
        """function to remove a card from a player's hand

        Args:
            card (Card): the card which the player has removed from his hand
        """
        self.cards.remove(card)

    def add_discount(self, amount:int) -> None:
        """Function for adding to a player's discount, i.e. players owns a vrou

        Args:
            amount (int): amount of discount cards the player has
        """
        self.money = amount


    def add_extra_card_temp(self) -> None:
        """Function for adding the number of extras cards a player may draw 
            on this turn based on the number of ships this is set only for a particular round

        Args:
            none, the function always add 1
        """
        self.extra_card_temp += 1

    def reset_extra_card_temp(self) -> None:
        """Function for resetting the number of extras cards a player may draw on this turn to 0

        Args:
            none, the function always add 1
        """
        self.extra_card_temp = 0

    def add_extra_card_perm(self) -> None:
        """Function for adding the number of extras cards a player may draw 
            on this turn based on the number of vrou cards - this is set for the duration of the game

        Args:
            none, the function always add 1
        """
        self.extra_card_perm += 1