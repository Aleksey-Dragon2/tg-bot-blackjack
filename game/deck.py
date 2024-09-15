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


def summa_cards(mylist,user_score):
    score=0
    for card in mylist:
        card=card.split()
        if card[1]=="Валет" or card[1]=="Дама" or card[1]=="Король":
            score+=10
        elif card[1]=="Туз": # переделать механику подсчета очков
            if user_score+11>21:
                score+=1
            else:
                score+=11
        else: 
            score+=int(card[1])
    return int(score)

def calculate_result(player):
    game_info = f"Карты дилера: {player.dealer_cards}\nСумма дилера: {player.dealer_score}\nВаши карты: {player.user_cards}\nСумма карт: {player.user_score}"
    if player.user_score > player.dealer_score and player.user_score < 22 or player.dealer_score > 21 and player.user_score < 22:
        return f"Win,\n{game_info}"
    elif player.user_score < player.dealer_score and player.dealer_score < 22 or player.user_score > 21 and player.dealer_score < 22:
        return f"lose,\n{game_info}"
    else:
        return f'ничья,\n{game_info}'

