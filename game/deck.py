import random
import bot.database as db
from config.language import GAME_RESULT, WIN_GAME, LOSE_GAME,DRAW_GAME

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


def summa_cards(mylist, user_score):
    score = 0
    ace_count = 0
    
    for card in mylist:
        card = card.split()
        
        if card[1] in ["Валет", "Дама", "Король"]:
            score += 10
        elif card[1] == "Туз":
            ace_count += 1
            score += 11
        else:
            score += int(card[1])

    while score > 21 and ace_count:
        score -= 10 
        ace_count -= 1
    
    return score

def calculate_result(player, user_id):
    game_info=GAME_RESULT(player)
    if player.user_score > player.dealer_score and player.user_score < 22 or player.dealer_score > 21 and player.user_score < 22:
        db.add_win(user_id)
        return f"{WIN_GAME}\n\n{game_info}"
    elif player.user_score < player.dealer_score and player.dealer_score < 22 or player.user_score > 21 and player.dealer_score < 22:
        db.add_lose(user_id)
        return f"{LOSE_GAME}\n\n{game_info}"
    else:
        db.add_game(user_id)
        return f'{DRAW_GAME}\n\n{game_info}'

