import random


class Deck:
    """deck object"""

    def __init__(self):

        suits = ['\u2666', '\u2665', '\u2663', '\u2660']
        cards = ['A', '2', '3', '4', '5', '6',
                 '7', '8', '9', 'T', 'J', 'Q', 'K']

        self.content = []
        for card in cards:
            for suit in suits:
                self.content.append(card+suit)

    def show(self):
        """show the content"""
        print(self.content)

    def shuffle(self):
        """shuffle the deck"""
        random.shuffle(self.content)

    def hit(self):
        """hit a card"""
        return self.content.pop()
