from run import Card1, Card2, Hand1, Hand2, Hand_Enum

def test_Card_01():
    assert Card1.from_string("A").relative_strength(Card1.from_string("J") ) > 0
    assert Card1.from_string("8").relative_strength(Card1.from_string("Q")) < 0
    assert Card1.from_string("3").relative_strength(Card1.from_string("3")) == 0
    assert Card1.from_string("J").relative_strength(Card1.from_string("8") ) > 0
    assert Card2.from_string("J").relative_strength(Card2.from_string("8") ) < 0

def test_Hand1_01():
    assert Hand1.from_string("32T3K 765").type == Hand_Enum.one_pair
    assert Hand1.from_string("T55J5 684").type == Hand_Enum.three_of_a_kind
    assert Hand1.from_string("KK677 28").type == Hand_Enum.two_pair
    assert Hand1.from_string("KTJJT 220").type == Hand_Enum.two_pair
    assert Hand1.from_string("QQQJA 483").type == Hand_Enum.three_of_a_kind


def test_Hand1_02():
    assert Hand1.from_string("32T3K 765").relative_strength(Hand1.from_string("KK677 28")) < 0
    assert Hand1.from_string("T55J5 684").relative_strength(Hand1.from_string("KTJJT 220")) > 0
    assert Hand1.from_string("KK677 28").relative_strength(Hand1.from_string("KTJJT 220")) > 0

def test_Hand2_01():
    assert Hand2.from_string("32T3K 765").type == Hand_Enum.one_pair
    assert Hand2.from_string("T55J5 684").type == Hand_Enum.four_of_a_kind
    assert Hand2.from_string("KK677 28").type == Hand_Enum.two_pair
    assert Hand2.from_string("KTJJT 220").type == Hand_Enum.four_of_a_kind
    assert Hand2.from_string("QQQJA 483").type == Hand_Enum.four_of_a_kind

# T55J5 684
# KK677 28
# KTJJT 220
# QQQJA 483
