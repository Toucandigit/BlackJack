import random

class Card(object):
    def __init__(self, num):
        assert isinstance(num, str)
        suits = {"D","S","C","H","d","s","c","h"}
        assert num[0] in suits
        if num[0].lower() == "d":
            self.suit = 0
        elif num[0].lower() == "s":
            self.suit = 1
        elif num[0].lower() == "c":
            self.suit = 2
        else:
            self.suit = 3

        if num[1].lower() == "k":
            self.value = 13
        elif num[1].lower() == "q":
            self.value = 12
        elif num[1].lower() == "j":
            self.value = 11
        elif num[1].lower() == "a":
            self.value = 1
        else:
            dig = int(num[1:])
            assert 1 < dig < 11
            self.value = dig

    def face(self):
        return self.value == 1 or self.value > 10

    def __str__(self):
        result = ""
        suit_dict = {0:"D", 1:"S", 2:"C", 3:"H"}
        result += suit_dict[self.suit]

        face_dict = {1:"A", 11:"J", 12:"Q", 13:"K"}
        if self.value != 1 and self.value < 11:
            result += str(self.value)
        else:
            result += face_dict[self.value]
        return result

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.value == other.value and self.suit == other.suit
        else:
            return NotImplemented

    @classmethod
    def from_nums(cls, suit, value):
        assert 0 <= suit < 4
        result = ""
        suit_dict = {0: "D", 1: "S", 2: "C", 3: "H"}
        result += suit_dict[suit]
        assert 0 < value <= 13
        face_dict = {1: "A", 11: "J", 12: "Q", 13: "K"}
        if value == 1 or value > 10:
            result += face_dict[value]
        else:
            result += str(value)
        return cls(result)

class Deck(object):
    def __init__(self):
        self.deck = []#first is on top of deck
        for suit in range(4):
            for val in range(1, 14):
                self.deck.append(Card.from_nums(suit, val))
        self.out = []

    def take_top(self):
        card = self.deck.pop(0)
        self.out.append(card)
        return card

    def shuffle_in(self, card):
        assert isinstance(card, Card)
        if card in self.out:
            self.out.remove(card)
            self.deck.insert(random.randint(0, len(self.deck) - 1), card)

    def shuffle(self):
        temp_list = []
        while len(self.out) != 0:
            self.deck.append(self.out.pop(0))
        while len(self.deck) != 0:
            temp_list.append(self.deck.pop(random.randint(0, len(self.deck) - 1)))
        self.deck = temp_list

class BJBoard(object):
    def __init__(self, pl = 500):
        self._deck = Deck()
        self._deck.shuffle()
        self._house_cards = []
        self._player_cards = []
        self._house_score = 0
        self._player_score = pl

    def _player_draw(self):
        self._player_cards.append(self._deck.take_top())

    def _house_draw(self):
        self._house_cards.append(self._deck.take_top())

    def _check_bust(self):
        aces = 0
        total = 0
        for card in self._player_cards:
            if card.value == 1:
                aces += 1
            elif card.value > 10:
                total += 10
            else:
                total += card.value
        if total > 21:
            return True
        else:
            if 21 - total > 11 + aces - 1:
                while aces != 0:
                    if 21 - total > 11:
                        aces -= 1
                        total += 11
                    else:
                        aces -= 1
                        total += 1
            else:
                while aces != 0:
                    aces -= 1
                    total += 11

    def _check_house(self):
        aces = 0
        total = 0
        for card in self._house_cards:
            if card.value == 1:
                aces += 1
            elif card.value > 10:
                total += 10
            else:
                total += card.value
        if total > 21:
            return True
        else:
            if 21 - total > 11 + aces - 1:
                while aces != 0:
                    if 21 - total > 11:
                        aces -= 1
                        total += 11
                    else:
                        aces -= 1
                        total += 1
            else:
                while aces != 0:
                    aces -= 1
                    total += 11
            return total > 21

    def _print_deck(self, deck):
        result = ""
        for card in deck:
            result += str(card) + " "
        print(result)

    def _player_total(self):
        aces = 0
        total = 0
        for card in self._player_cards:
            if card.value == 1:
                aces += 1
            elif card.value > 10:
                total += 10
            else:
                total += card.value
        if 21 - total > 11 + aces - 1:
            while aces != 0:
                if 21 - total > 11:
                    aces -= 1
                    total += 11
                else:
                    aces -= 1
                    total += 1
        else:
            while aces != 0:
                aces -= 1
                total += 11
        return total

    def _house_total(self):
        aces = 0
        total = 0
        for card in self._house_cards:
            if card.value == 1:
                aces += 1
            elif card.value > 10:
                total += 10
            else:
                total += card.value
        if 21 - total > 11 + aces - 1:
            while aces != 0:
                if 21 - total > 11:
                    aces -= 1
                    total += 11
                else:
                    aces -= 1
                    total += 1
        else:
            while aces != 0:
                aces -= 1
                total += 11
        return total

    def reset(self):
        self._player_cards = []
        self._house_cards = []
        self._deck.shuffle()

    def play(self):
        while True:
            if self._player_score <= 0:
                print("Oh no, you have run out of money! You currently have " + str(self._player_score) + "!")
                break
            bet = input("Select an amount to bet! You currently have " + str(self._player_score) + ".")
            while True:
                if isinstance(bet, (int, float)):
                    if 0 < bet <= self._player_score:
                        break
                    else:
                        bet = input("Sorry, you cannot bet that much. Try again.")
                else:
                    bet = input("Sorry, that's not a number. Try again.")
            self._player_draw()
            self._house_draw()
            self._player_draw()
            self._house_draw()
            print("You have:")
            self._print_deck(self._player_cards)
            print("The house has:" + str(self._house_cards[0]))
            print("Your current total is " + str(self._player_total()))
            if self._player_total() != 21:
                while True:
                    answer = raw_input("Hit or stand? [h/s]")
                    while answer not in {"h", "s"}:
                        answer = raw_input("Sorry, didn't quite get that.")
                    if answer == "s":
                        break
                    self._player_draw()
                    print("You drew a " + str(self._player_cards[-1]))
                    print("You have:")
                    self._print_deck(self._player_cards)
                    print("Your total is " + str(self._player_total()) + ".")
                    if self._player_total() >= 21:
                        break
            else:
                print("You have 21!")
            if self._player_total() > 21:
                print("Bust! You lost " + str(bet) + "!")
                self._player_score -= bet
                self._house_score -= bet
                print("The houses hand was:")
                self._print_deck(self._house_cards)
            else:
                print("The houses hand is:")
                self._print_deck(self._house_cards)
                while not self._house_total() >= 17:
                    self._house_draw()
                    print("The house drew a " + str(self._house_cards[-1]) + ".")
                    print("Houses total is " + str(self._house_total()) + ".")
                    if self._house_total() > 21:
                        print("The house busts! You win " + str(bet))
                        self._player_score += bet
                        self._house_score -= bet
            if not (self._check_bust() or self._check_house()):
                print("Your score was " + str(self._player_total()) + ".")
                print("The houses score was " + str(self._house_total()) + ".")
                if self._player_total() > self._house_total():
                    print("You won! You win " + str(bet) + "!")
                    self._player_score += bet
                    self._house_score -= bet
                elif self._house_total() > self._player_total():
                    print("You lost! You lose " + str(bet) + "!")
                    self._player_score -= bet
                    self._house_score += bet
                else:
                    print("It's a tie! No one wins or loses.")
            print("You currently have " + str(self._player_score) + ".")
            response = raw_input("Would you like to play again? [y/n]")
            while response not in {"y", "n"}:
                response = raw_input("Sorry, I didn't quite get that.")
            if response == "n":
                print("Thanks for playing!")
                break
            self.reset()

brd = BJBoard()
brd.play()
