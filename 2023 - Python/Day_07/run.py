# %%
from typing import Generic, TypeVar
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

# %%
Card_Enum = TypeVar("Card_Enum")
Card_Enum1 = Enum("Card_Enum", ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"])
Card_Enum2 = Enum("Card_Enum", ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"])

@dataclass
class Card:
    type: Card_Enum

    def __init__(self, card_enum:Card_Enum, string:str):
        self.type = card_enum[string]
    
    def relative_strength(self, card):
        return self.type.value - card.type.value
    
class Card1(Card): # Card definition for the first problem
    @classmethod
    def from_string(cls, string: str):
        return cls(Card_Enum1, string)
    
class Card2(Card): # Card definition for the second problem
    @classmethod
    def from_string(cls, string: str):
        return cls(Card_Enum2, string)    

# %%
Hand_Enum = Enum("Hand_Enum", ["high_card", "one_pair", "two_pair", "three_of_a_kind", "full_house", "four_of_a_kind", "five_of_a_kind"])
class Hand:
    cards: list[Card]
    bid: int
    type: Hand_Enum

    def __init__(self, card_class:Card, string:str) -> None:
        cards_string, bid_string = string.split()

        cards = []        
        for card_char in cards_string:
            cards.append(card_class.from_string(card_char))

        hand_type = self.compute_hand_type(cards_string)

        self.cards = cards
        self.bid = int(bid_string)
        self.type = hand_type

    @classmethod
    def from_string(cls, string:str):
        raise NotImplementedError()

    def compute_hand_type(self, cards_string: str):
        raise NotImplementedError()

    def relative_strength(self, hand) -> int:
        difference = self.type.value - hand.type.value
        if difference == 0:
            i = 0
            while difference == 0 and i < len(self.cards):
                self_card = self.cards[i]
                other_card = hand.cards[i]
                difference = self_card.relative_strength(other_card)
                i += 1
        return difference

# Hand definition for the first problem
class Hand1(Hand):
    @classmethod
    def from_string(cls, string:str):
        return cls(Card1, string)
    
    def compute_hand_type(self, cards_string:str):
        cards_char_set = set(cards_string)
        nb_cards = [cards_string.count(card_char) for card_char in cards_char_set]
        nb_cards.sort(reverse=True)
        
        match nb_cards[0]:
            case 5:
                hand_type = Hand_Enum.five_of_a_kind
            case 4:
                hand_type = Hand_Enum.four_of_a_kind
            case 3:
                if nb_cards[1] == 2:
                    hand_type = Hand_Enum.full_house
                else:
                    hand_type = Hand_Enum.three_of_a_kind
            case 2:
                if nb_cards[1] == 2:
                    hand_type = Hand_Enum.two_pair
                else:
                    hand_type = Hand_Enum.one_pair
            case 1:
                hand_type = Hand_Enum.high_card

        return hand_type

# Hand definition for the second problem    
class Hand2(Hand):
    @classmethod
    def from_string(cls, string:str):
        return cls(Card2, string)
    
    def compute_hand_type(self, cards_string:str):
        # Remove jokers if there are any
        nb_jokers = cards_string.count(Card_Enum2.J.name)
        cards_string = cards_string.replace("J", "")

        cards_char_set = set(cards_string)
        nb_cards = [cards_string.count(card_char) for card_char in cards_char_set]
        nb_cards.sort(reverse=True)

        if len(nb_cards) == 0:
            hand_type = Hand_Enum.five_of_a_kind
        else:
            match nb_cards[0]:
                case 5:
                    hand_type = Hand_Enum.five_of_a_kind
                case 4:
                    match nb_jokers:
                        case 0:
                            hand_type = Hand_Enum.four_of_a_kind
                        case 1:
                            hand_type = Hand_Enum.five_of_a_kind
                case 3:
                    if len(nb_cards) > 1 and nb_cards[1] == 2:
                        hand_type = Hand_Enum.full_house
                    else:
                        match nb_jokers:
                            case 0:
                                hand_type = Hand_Enum.three_of_a_kind
                            case 1:
                                hand_type = Hand_Enum.four_of_a_kind
                            case 2:
                                hand_type = Hand_Enum.five_of_a_kind
                case 2:
                    if len(nb_cards) > 1 and nb_cards[1] == 2:
                        match nb_jokers:
                            case 0:
                                hand_type = Hand_Enum.two_pair
                            case 1:
                                hand_type = Hand_Enum.full_house
                    else:
                        match nb_jokers:
                            case 0:
                                hand_type = Hand_Enum.one_pair
                            case 1:
                                hand_type = Hand_Enum.three_of_a_kind
                            case 2:
                                hand_type = Hand_Enum.four_of_a_kind
                            case 3:
                                hand_type = Hand_Enum.five_of_a_kind
                case 1:
                    match nb_jokers:
                        case 0:
                            hand_type = Hand_Enum.high_card
                        case 1:
                            hand_type = Hand_Enum.one_pair
                        case 2:
                            hand_type = Hand_Enum.three_of_a_kind
                        case 3:
                            hand_type = Hand_Enum.four_of_a_kind
                        case 4:
                            hand_type = Hand_Enum.five_of_a_kind

        return hand_type

# %%
def build_hands(hand_class:Hand, string:str) -> list[Hand]:
    return [hand_class.from_string(line) for line in string.splitlines()]

def bubble_sort(hand_list:list[Hand]) -> list[Hand]:
    for i in range(len(hand_list)-1, 0, -1):
        for j in range(i):
            if hand_list[j+1].relative_strength(hand_list[j]) < 0:
                hand_list[j+1], hand_list[j] = hand_list[j], hand_list[j+1]
    return hand_list

# %%
input_file = Path("input.txt")
input_text = input_file.read_text()

# %% Solution to the first problem
hands = build_hands(Hand1, input_text)
hands = bubble_sort(hands)
total_winnings = 0
for rank, hand in enumerate(hands):
    total_winnings += (rank+1) * hand.bid
print(total_winnings)

# %% Solution to the second problem
hands = build_hands(Hand2, input_text)
hands = bubble_sort(hands)
total_winnings = 0
for rank, hand in enumerate(hands):
    total_winnings += (rank+1) * hand.bid
print(total_winnings)
