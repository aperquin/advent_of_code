from run import Row, Spring_State

def test_row_constructor_01():
    row_1 = Row([Spring_State.damaged, Spring_State.operational, Spring_State.unknown], [1])
    row_2 = Row.from_string("#.? 1")
    assert  row_1 == row_2

def test_compute_damaged_numbers_01():
    row: Row = Row.from_string(".#..### 1,1,3")
    assert Row.compute_damaged_numbers(row.spring_states) == [1, 3]

def test_compute_damaged_numbers_02():
    row: Row = Row.from_string(".##.### 1,1,3")
    assert Row.compute_damaged_numbers(row.spring_states) == [2, 3]

def test_compute_damaged_numbers_03():
    row: Row = Row.from_string("....### 1,1,3")
    assert Row.compute_damaged_numbers(row.spring_states) == [3]

def test_row_is_valid_01():
    row_1: Row = Row.from_string("???.### 1,1,3")
    row_2: Row = Row.from_string("#.#.### 1,1,3")
    assert row_1.is_valid(row_2.spring_states) 

def test_row_is_valid_02():
    row_1: Row = Row.from_string("???.### 1,1,3")
    row_2: Row = Row.from_string(".##.### 1,1,3")
    assert ~row_1.is_valid(row_2.spring_states)

def test_row_is_valid_03():
    row_1: Row = Row.from_string("???.### 1,1,3")
    row_2: Row = Row.from_string("....### 1,1,3")
    assert ~row_1.is_valid(row_2.spring_states)
    
def test_find_number_valid_arrangements_01():
    row: Row = Row.from_string("???.### 1,1,3")
    assert row.find_number_valid_arrangements() == 1

def test_find_number_valid_arrangements_02():
    row: Row = Row.from_string(".??..??...?##. 1,1,3")
    assert row.find_number_valid_arrangements() == 4

def test_find_number_valid_arrangements_03():
    row: Row = Row.from_string("?#?#?#?#?#?#?#? 1,3,1,6")
    assert row.find_number_valid_arrangements() == 1

def test_find_number_valid_arrangements_04():
    row: Row = Row.from_string("????.#...#... 4,1,1")
    assert row.find_number_valid_arrangements() == 1

def test_find_number_valid_arrangements_05():
    row: Row = Row.from_string("????.######..#####. 1,6,5")
    assert row.find_number_valid_arrangements() == 4

def test_find_number_valid_arrangements_06():
    row: Row = Row.from_string("?###???????? 3,2,1")
    assert row.find_number_valid_arrangements() == 10
