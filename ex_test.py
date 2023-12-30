from src.card import Expedition, SettlerCaptainPriest
from src.table import Table
from src.players import Player
from src.func import check_expedition
        
player = Player(1, "a_player")
table = Table()

# Create all the expedition cards, so that all the cards can be checked
expedition_cards = {"card1": {"name":"c1", "vp": 4, "money": 2, "code1":2, "code2":0, "code3":0},
                    "card2": {"name":"c2", "vp": 4, "money": 2, "code1":0, "code2":2, "code3":0},
                    "card3": {"name":"c3", "vp": 4, "money": 2, "code1":0, "code2":0, "code3":2},
                    "card4": {"name":"c4", "vp": 6, "money": 3, "code1":2, "code2":0, "code3":1},
                    "card5": {"name":"c5", "vp": 6, "money": 3, "code1":0, "code2":2, "code3":1},
                    "card6": {"name":"c6", "vp": 5, "money": 3, "code1":1, "code2":1, "code3":1}
                    }
expedition_options = []
for card_key, card_data in expedition_cards.items():
    new_card = Expedition(card_data["name"], 
                        card_data["vp"], 
                        card_data["money"], 
                        card_data["code1"], 
                        card_data["code2"], 
                        card_data["code3"])
    expedition_options.append(new_card)

# Create a few anchor, crossi and house cards to later add to player hand
scp = []
symbols = ["⚓" , "†" , "⌂", "⚓" , "†" , "⌂"]
for symbol in symbols:
    new_card = SettlerCaptainPriest(4, symbol)
    scp.append(new_card)

for card in scp:
    print(card.name)

# first test: two anchors in expedition area, player have no cards
print('----TEST ONE--------')
table.add_card_to_expeditions(expedition_options[0])
print(check_expedition(player, table) )

# second test: two anchors in expedition area, player have one anchor cards, then two cards
print('----TEST TWO--------')
player.add_card_to_hand(scp[0])
print(check_expedition(player, table))   
player.add_card_to_hand(scp[3])
print(check_expedition(player, table)) 

