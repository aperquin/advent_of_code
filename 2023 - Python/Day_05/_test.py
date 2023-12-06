from pathlib import Path
from run import Range, Map, Almanac

map_example = """seed-to-soil map:
50 98 2
52 50 48"""

almanac_example = Path("example.txt").read_text()

def test_range_constructor_01():
    range_a = Range(destination_start=50, source_start=98, length=2)
    range_b= Range.from_string("50 98 2")
    assert range_a == range_b

def test_range_is_in_range_01():
    range_a= Range.from_string("50 98 2")
    assert range_a.is_in_range(98) and range_a.is_in_range(99)

def test_range_is_in_range_02():
    range_a= Range.from_string("50 98 2")
    assert (not range_a.is_in_range(97)) and (not range_a.is_in_range(100))

def test_range_map_01():
    range_a= Range.from_string("50 98 2")
    assert range_a.map(98) == 50 and range_a.map(99) == 51

def test_range_map_02():
    range_a= Range.from_string("50 98 2")
    assert range_a.map(97) == 97 and range_a.map(100) == 100

def test_map_constructor_01():
    range_1 = Range.from_string("50 98 2")
    range_2 = Range.from_string("52 50 48")
    map_1 = Map("seed", "soil", [range_1, range_2])
    map_2 = Map.from_string(map_example)

    assert map_1 == map_2

def test_map_map_01():
    map_1 = Map.from_string(map_example)
    assert map_1.map(98) == 50 and map_1.map(52) == 54

def test_map_map_02():
    map_1 = Map.from_string(map_example)
    assert map_1.map(100) == 100 and map_1.map(49) == 49

def test_map_is_mapping_01():
    map_1 = Map.from_string(map_example)
    assert map_1.is_mapping_from_to("seed", "soil")

def test_map_is_mapping_02():
    map_1 = Map.from_string(map_example)
    assert (not map_1.is_mapping_from_to("soil", "seed")) and (not map_1.is_mapping_from_to("temperature", "humidity"))

def test_almanac_constructor_01():
    map_1 = Map.from_string(map_example)
    almanac_1 = Almanac.from_string(almanac_example)
    assert almanac_1.seeds == [79, 14, 55, 13] and almanac_1.maps[0] == map_1

def test_almanac_map_01():
    almanac_1 = Almanac.from_string(almanac_example)
    assert almanac_1.map(79, "seed", "fertilizer") == 81 and almanac_1.map(14, "soil", "water") == 49 and almanac_1.map(13, "seed", "location") == 35

def test_range_map_ranges_01():
    range_1 = Range(5, 20, 4)
    range_2 = Range(40, 10, 2)
    result = range_2.map_range(range_1)
    print(result)
    assert result == [Range(5, 20, 4)]

def test_range_map_ranges_02():
    range_1 = Range(5, 20, 7)
    range_2 = Range(40, 10, 2)
    result = range_2.map_range(range_1)
    print(result)
    assert result == [Range(5, 20, 5), Range(40, 25, 2)]

def test_range_map_ranges_03():
    range_1 = Range(5, 20, 9)
    range_2 = Range(40, 10, 2)
    result = range_2.map_range(range_1)
    print(result)
    assert result == [Range(5, 20, 5), Range(40, 25, 2), Range(12, 27, 2)]

def test_range_map_ranges_04():
    range_1 = Range(11, 20, 5)
    range_2 = Range(40, 10, 2)
    result = range_2.map_range(range_1)
    print(result)
    assert result == [Range(41, 20, 1), Range(12, 21, 4)]
    
def test_range_map_ranges_05():
    range_1 = Range(12, 20, 5)
    range_2 = Range(40, 10, 2)
    result = range_2.map_range(range_1)
    print(result)
    assert result == [Range(12, 20, 5)]