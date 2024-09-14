import random

def get_deck():
    deck_cards=[]
    for i in range(2,11):
        deck_cards.append(f"♥️ {i}")
    deck_cards.append(f"♥️ Валет")
    deck_cards.append(f"♥️ Дама")
    deck_cards.append(f"♥️ Король")
    deck_cards.append(f"♥️ Туз")

    for i in range(2,11):
        deck_cards.append(f"♧ {i}")
    deck_cards.append(f"♧ Валет")
    deck_cards.append(f"♧ Дама")
    deck_cards.append(f"♧ Король")
    deck_cards.append(f"♧ Туз")

    for i in range(2,11):
        deck_cards.append(f"♦️ {i}")
    deck_cards.append(f"♦️ Валет")
    deck_cards.append(f"♦️ Дама")
    deck_cards.append(f"♦️ Король")
    deck_cards.append(f"♦️ Туз")

    for i in range(2,11):
        deck_cards.append(f"♤ {i}")
    deck_cards.append(f"♤ Валет")
    deck_cards.append(f"♤ Дама")
    deck_cards.append(f"♤ Король")
    deck_cards.append(f"♤ Туз")

    return deck_cards

def get_card(deck_cards):
    card=random.choice(deck_cards)
    deck_cards.pop(deck_cards.index(card))
    return card


def summa_cards(mylist):
    score=0
    for card in mylist:
        card=card.split()
        if card[1]=="Валет" or card[1]=="Дама" or card[1]=="Король":
            score+=10
        elif card[1]=="Туз":
            if score+11>21:
                score+=1
            else:
                score+=11
        else: 
            score+=int(card[1])
    return int(score)
