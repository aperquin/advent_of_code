from run import ScratchCard

def test_from_string():
    a = ScratchCard(1, [41, 48, 83, 86, 17], [83, 86, 6, 31, 17, 9, 48, 53])
    b = ScratchCard.from_string("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
    assert a.id == b.id and a.winning_numbers == b.winning_numbers and a.numbers_you_have == b.numbers_you_have

def test_winning_numbers_you_have_01():
    a = ScratchCard.from_string("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
    assert a.winning_numbers_you_have().sort() == [48, 83, 17, 86].sort()

def test_winning_numbers_you_have_02():
    a = ScratchCard.from_string("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19")
    assert a.winning_numbers_you_have().sort() == [48, 83, 17, 86].sort()

def test_winning_numbers_you_have_03():
    a = ScratchCard.from_string("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1")
    assert a.winning_numbers_you_have().sort() == [48, 83, 17, 86].sort()

def test_winning_numbers_you_have_04():
    a = ScratchCard.from_string("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83")
    assert a.winning_numbers_you_have().sort() == [48, 83, 17, 86].sort()

def test_winning_numbers_you_have_05():
    a = ScratchCard.from_string("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36")
    assert a.winning_numbers_you_have().sort() == [48, 83, 17, 86].sort()

def test_winning_numbers_you_have_06():
    a = ScratchCard.from_string("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11")
    assert a.winning_numbers_you_have().sort() == [48, 83, 17, 86].sort()

def test_score_01():
    a = ScratchCard.from_string("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
    assert a.score() == 8