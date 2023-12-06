# %%
from dataclasses import dataclass
from pathlib import Path

def clean_string(string):
    string = " ".join(string.split()) # Remove redundant whitespaces
    return string

@dataclass
class ScratchCard:
    id: int
    winning_numbers: list[int]
    numbers_you_have: list[int]

    def winning_numbers_you_have(self) -> list[int]:
        winning_set = set(self.winning_numbers)
        own_numbers_set = set(self.numbers_you_have)
        return list(own_numbers_set.intersection(winning_set))

    def score(self) -> int:
        card_score = 0
        own_winning_numbers = self.winning_numbers_you_have()

        for i in range(len(own_winning_numbers)):
            if i==0:
                card_score += 1
            else:
                card_score *= 2

        return card_score

    @classmethod
    def from_string(cls, string:str):
        id_string, lists_string = string.split(':')
        card_id = int(id_string.split(" ")[-1])
        winning_numbers_string, numbers_you_have_string = lists_string.split('|')
        winning_numbers = [int(number.strip()) for number in clean_string(winning_numbers_string).strip().split(' ')]
        numbers_you_have = [int(number.strip()) for number in clean_string(numbers_you_have_string).strip().split(' ')]
        
        return cls(card_id, winning_numbers, numbers_you_have)

# %%        
@dataclass
class ScrachCardPile:
    scratch_cards: list[ScratchCard]

    @classmethod
    def from_string(cls, string:str):
        scratch_cards = []
        scratch_card_nb = []
        for line in input_text.splitlines():
            scratch_cards.append(ScratchCard.from_string(line))
        return cls(scratch_cards)
    
    def play(self):
        pile_length = len(self.scratch_cards)
        scratch_card_nb = [1 for _ in range(pile_length)]
        for i, scratch_card in enumerate(self.scratch_cards):
            winning_numbers = scratch_card.winning_numbers_you_have()
            id_cards_to_add = [i+j+1 for j in range(len(winning_numbers)) if i+j+1 < pile_length]
            for id_card_to_add in id_cards_to_add:
                scratch_card_nb[id_card_to_add] += scratch_card_nb[i]
            print(scratch_card_nb)
        return sum(scratch_card_nb)

# %%
input_file = Path("input.txt")
input_text = input_file.read_text()

# %% Solution to the first problem
total_score = 0
for string in input_text.splitlines():
    scratch_card = ScratchCard.from_string(string)
    total_score += scratch_card.score()
print(total_score)

# %% Solution to the second problem
scratch_card_pile = ScrachCardPile.from_string(input_text)
scratch_card_pile.play()
