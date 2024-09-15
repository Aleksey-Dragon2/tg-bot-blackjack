from . import deck
class Player:
    def __init__(self):
        self.deck = []
        self.user_cards = []
        self.dealer_cards = []
        self.user_score = 0
        self.dealer_score = 0

    def add_user_card(self, card):
        self.user_cards.append(card)
        self.user_score = self.calculate_score(self.user_cards)

    def add_dealer_card(self, card):
        self.dealer_cards.append(card)
        self.dealer_score = self.calculate_score(self.dealer_cards)

    def reset(self, deck):
        self.deck = deck
        self.user_cards.clear()
        self.dealer_cards.clear()
        self.user_score = 0
        self.dealer_score = 0

    @staticmethod
    def calculate_score(cards):
        return deck.summa_cards(cards)
