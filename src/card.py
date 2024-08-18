import json
from input.setting import *
import random


class Card():
    """Parent class for all cards
    """

    def __init__(self, price) -> None:
        self.price = price
         
        

class Trader(Card):
    def __init__(self, color) -> None:
        super().__init__()
        self.color = color
        if self.price == 3:
                self.vp = 1
        else:
                self.vp = 2

                

class SettlerCaptainPriest(Card):
    """Settler Captain Priest

    Args:
        Card (Class): Cards main class
    """
    def __init__(self, price, symbol) -> None:
        """Initialize the SettlerCaptainPriest class.

        This method initializes the SettlerCaptainPriest class with the given price and symbol.
        It also sets the victory points (vp) to 1 and assigns a name based on the symbol.

        Args:
            price (int): The cost of the card.
            symbol (str): The symbol of the person represented by the card.
                It can be one of the following: "†" (priest), "⚓" (captain), "⌂" (settler), or "†⚓⌂" (jack of all trades).

        Returns:
            None
        """

        super().__init__(price)
        self.symbol = symbol
        self.vp = 1
        if symbol == "†":
            self.name = "priest"

        elif symbol == "⚓":
            self.name = "captain"

        elif symbol == "⌂":
            self.name = "settler"
        
        elif symbol == "†⚓⌂":
            self.name = "jack of all trades"


class SailorPirate(Card):
    """Sailors will fight the pirates

    Args:
        Card (Class): Cards main class
    """
    def __init__(self, price, defence) -> None:
        """Initiation of the class

        Args:
            price (int): this is the price of the card
            defence (int): the defence or resistance that this sailor will give
        """
        super().__init__(price)
        self.name = "sailor"
        self.defence = defence
        if self.price == 3:   # <-------------------------------------- Victory points for sailors are not correct
            self.vp = 1
        elif self.price == 5:
            self.vp = 2
        else:
            self.vp = 3


class Vrou(Card):
    """Vrou will arrange discount on future buys

    Args:
        Card (Class): Cards main class
    """
    def __init__(self, price) -> None:
        """Initiation of the class

        Args:
            price (int): this is the price of the card
        """
        super().__init__(price)
        self.name = "vrou"
        self.discount = -1
        if self.price == 7:
            self.vp = 2
        else:
            self.vp = 3

class Witzbold(Card):
    """Witzbold give you one money if another player crashes out

    Args:
        Card (Class): Cards main class
    """

    def __init__(self, price) -> None:
        """Initiation of the class

        Args:
            price (int): this is the price of the card
        """
        super().__init__(price)
        self.name = "witzbold"
        if self.price == 7:
            self.vp = 2
        else:
            self.vp = 3

class Admiral(Card):
    """Admiral gives you 2 coins for 5 or more cards on the table on your turn

    Args:
        Card (Class): Cards main class
    """
    def __init__(self, price) -> None:
        """Initiation of the class

        Args:
            price (int): this is the price of the card
        """
        super().__init__(price)
        self.name = "admiral"
        if self.price == 5:
            self.vp = 1
        elif self.price == 7:
            self.vp = 2
        else:
            self.vp = 3

class Governor(Card):
    """Governor gives you 1 more turn

    Args:
        Card (Class): Cards main class
    """
    def __init__(self, price) -> None:
        """Initiation of this class
        """
        super().__init__(price)
        self.name = "governor"
        self.vp = 0
        self.price = 8


class Ship(Card):
    """Ship gives you money

    Args:
        Card (Class): Cards main class
    """

    def __init__(self, give_money, colour, attack, price=0) -> None:
        """Initiation of this class
        """
        super().__init__(price)
        self.name = "ship"
        self.give_money = give_money
        self.colour = colour
        self.attack = attack
        self.vp = 0

class Trader(Card):
    """Trader gives you more money for a specific colour ships

    Args:
        Card (Class): Cards main class
    """
    def __init__(self, price, colour) -> None:
        """Initiation of this class
        """
        super().__init__(price)
        self.name = "trader"
        self.colour = colour
 
        if self.price == 3:
            self.vp = 1

        elif self.price == 5:
            self.vp = 2

class Tax(Card):
    """Tax card for min victory points and max swords

    Args:
        Card (Class): Cards main class
    """
    def __init__(self, symbol, price=0) -> None:
        """Initiation of this class
        """
        super().__init__(price)
        self.name = "tax"
        self.symbol = symbol


class Expedition(Card):
    def __init__(self, symbol, vp, give_money, code1, code2, code3, price=0) -> None:
        """Expidition card

        Args:
            symbol (str): Symbol of Expedition
            vp (int): Vp of Expedition
            give_money (int): Money the Expedition is giving you
            code (tulpe): Used to check if you can buy it
            price (int, optional): Expedition does not have a price. Defaults to 0.
        """
        super().__init__(price)
        self.name = "expidition"
        self.symbols = symbol
        self.vp = vp
        self.give_money = give_money
        self.code1 = code1
        self.code2 = code2
        self.code3 = code3

        

        
class DeckOfCards():

    def __init__(self) -> None:
        """initiation of the deck of cards
        """
        self.cards = []
        self.remaining_cards = len(self.cards)

    def create_deck(self):
         
        #print("\t Reading json file")
        with open(deck_settings_file, 'r') as file:
            data = json.load(file) 
  
        #create the admiral deck
        for admiral in data["admiral"]["price"]:
            self.cards.append(Admiral(admiral))
        #print("\t Buidling admiral deck - OK")
        
        #create the governor deck
        for governor in data["governor"]["price"]:
            self.cards.append(Governor(governor))
        #print("\t Buidling governor deck - OK")

        #create the witzbold deck
        for witzbold in data["witzbold"]["price"]:
            self.cards.append(Witzbold(witzbold))
        #print("\t Buidling witzbold deck - OK")

        #create the vrou deck
        for vrou in data["vrou"]["price"]:
            self.cards.append(Vrou(vrou))
        #print("\t Buidling vrou deck - OK")

        #create the tax deck
        for tax in data["tax"]["symbol"]:
            self.cards.append(Tax(tax))
        #print("\t Buidling tax deck - OK")

        #create the sailor deck
        for index, sailor in enumerate(data["sailor"]["price"], start=0):
            price = data["sailor"]["price"][index]
            defences = data["sailor"]["defences"][index]
            self.cards.append(SailorPirate(price, defences))
        
        #print("\t Buidling sailer deck - OK")

        #create the captain deck
        for index, scp in enumerate(data["captain"]["price"], start=0):
            price = data["captain"]["price"][index]
            symbol = "⚓"
            self.cards.append(SettlerCaptainPriest(price, symbol))

        #print("\t Buidling captain deck - OK")

        #create the priest deck
        for index, scp in enumerate(data["priest"]["price"], start=0):
            price = data["priest"]["price"][index]
            symbol = "†"
            self.cards.append(SettlerCaptainPriest(price, symbol))

        #print("\t Buidling priest deck - OK")

        #create the settler deck
        for index, scp in enumerate(data["settler"]["price"], start=0):
            price = data["settler"]["price"][index]
            symbol = "⌂"
            self.cards.append(SettlerCaptainPriest(price, symbol))

        #print("\t Buidling settler deck - OK")

        #create the jack of all trades deck
        for index, scp in enumerate(data["jack of all trades"]["price"], start=0):
            price = data["jack of all trades"]["price"][index]
            symbol = "†⚓⌂"
            self.cards.append(SettlerCaptainPriest(price, symbol))

        #print("\t Buidling jack of all trades deck - OK")

        def ship_deck(data, ships:str, colour:str):
            """function for building ships

            Args:
                ship (str): ship key in json file
                colour (str): ship colour
            """
            for index, ship in enumerate(data[ships]["give_money"], start=0):
                give_money = data[ships]["give_money"][index]
                attack = data[ships]["attack"][index]
                self.cards.append(Ship(give_money, colour, attack))
    
            #print("\t Buidling %s ship deck - OK" %(colour))

        #create the ship deck
        ships = ["red_ship", "black_ship", "blue_ship", "green_ship", "yellow_ship"]
        colour = ["red", "black", "blue", "green", "yellow"]
        for index, ship in enumerate(ships, start=0):
            ship_deck(data, ships[index], colour[index])


        #create the expidition deck
        for index, expidition in enumerate(data["expidition"]["vp"], start=0):
            vp = data["expidition"]["vp"][index]
            sym = data["expidition"]["symbols"][index]
            a = ""
            code1 = 0
            code2 = 0
            code3 = 0

            for symbol in sym:
                if symbol == "1":
                    a += "⚓"
                    code1 += 1
                if symbol == "2":
                    a += "†"
                    code2 += 1
                if symbol == "3": 
                    a += "⌂"
                    code3 += 1

        

            give_money = data["expidition"]["give_money"][index]
            self.cards.append(Expedition(a, vp, give_money, code1, code2, code3))

        full_code = code1 + code2 + code3

            #print("\t Buidling expedition deck - OK")

        #create the trader deck
        for index, trader in enumerate(data["trader"]["price"], start=0):
            price = data["trader"]["price"][index]
            colour = data["trader"]["colour"][index]
            self.cards.append(Trader(price, colour))
        #print("\t Buidling trader deck - OK")

        self.remaining_cards = len(self.cards)



    def draw_card(self) -> Card:
        """draw a card from the deck of cards

        Returns:
            Card: Cards main class
        """
        drawn_card_number = random.randint(0, self.remaining_cards)
        #print("Random number: %i" %(drawn_card_number))
        drawn_card = self.cards[drawn_card_number-1]
        #print("Number of card in deck: %i"%(len(self.cards)))

        # Assuming self.cards is a list of cards
        if drawn_card in self.cards:
            self.cards.remove(drawn_card)
            self.remaining_cards = len(self.cards)
        else:
            # Handle the case where the card is not in the list
            print("The drawn card is not in the list.")

        return drawn_card
    
    def append(list):
        pass
    


    

 
 