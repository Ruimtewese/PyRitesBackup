from src.card import Card


class Table():
    """main Table class
    """
    def __init__(self) -> None:
        """class initiation
        """
        self.cards_on_table = []
        self.waste_cards = []
        self.expeditions = []
        self.alive = True
        self.ship_cards = 0


    def add_card_to_table(self, card: Card):
        """this function adds a card to the table

        Args:
            card (Card): this is the drawn card
        """
        self.cards_on_table.append(card)
 
    def remove_card_to_table(self, card: Card):
        """this function removes a card to the table

        Args:
            card (Card): this is the drawn card
        """
        self.cards_on_table.remove(card)

 
    def clear_table(self):
        """this function will clear the table. Reset the 'cards_on_table' variable
        """
        self.cards_on_table = []       

    def add_card_to_waste(self, card: Card):
        """this function adds a card to the waste pile

        Args:
            card (Card): this is the drawn card
        """
        self.waste_cards.append(card)

    def clear_waste(self):
        """this function will clear the waste pile. Reset the 'waste_cards' variable
        """
        self.waste_cards = []  

    def add_card_to_expeditions(self, card: Card):
        """this function adds a card to the expedition area

        Args:
            card (Card): this is the drawn card
        """
        self.expeditions.append(card)

    def remove_card_to_expeditions(self, card: Card):
        """this function removes a card to the expedition area

        Args:
            card (Card): this is the drawn card
        """
        self.expeditions.pop(card)

    def add_ship_cards(self):
        self.ship_cards += 1
        print("------------------------------------->%i ships on table" %self.ship_cards)

    def zero_ship_cards(self):
        self.ship_cards = 0

    def set_alive_status(self, status):
        self.alive = status

    




