from run import Mirror, Mirror2, Symmetry, np

example_1 = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
"""

example_2 = """#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

def test_mirror_constructor_01():
    mirror_1 = Mirror(np.array([
        [0, 1, 0, 0],
        [1, 1, 0, 1],
        [0, 0, 1, 1]
    ]))

    mirror_2 = Mirror.from_string("""#.##\n..#.\n##..""")

    assert np.array_equal(mirror_1.pattern, mirror_2.pattern)

def test_horizontal_symmetry_01():
    mirror: Mirror = Mirror.from_string(example_1)
    assert mirror.has_horizontal_symmetry_at(5)
    assert ~mirror.has_horizontal_symmetry_at(6)
    assert ~mirror.has_horizontal_symmetry_at(2)

def test_horizontal_symmetry_02():
    mirror: Mirror = Mirror.from_string(example_2)
    assert ~mirror.has_horizontal_symmetry_at(4)
    assert ~mirror.has_horizontal_symmetry_at(5)
    assert ~mirror.has_horizontal_symmetry_at(2)

def test_vertical_symmetry_01():
    mirror: Mirror = Mirror.from_string(example_1)
    assert ~mirror.has_vertical_symmetry_at(5)
    assert ~mirror.has_vertical_symmetry_at(6)
    assert ~mirror.has_vertical_symmetry_at(2)

def test_vertical_symmetry_02():
    mirror: Mirror = Mirror.from_string(example_2)
    assert mirror.has_vertical_symmetry_at(4)
    assert ~mirror.has_vertical_symmetry_at(5)
    assert ~mirror.has_vertical_symmetry_at(2)    

def test_find_symmetry_01():
    mirror: Mirror = Mirror.from_string(example_1)
    assert mirror.find_symmetry() == (Symmetry.horizontal, 5)

def test_find_symmetry_02():
    mirror: Mirror = Mirror.from_string(example_2)
    assert mirror.find_symmetry() == (Symmetry.vertical, 4)

def test_find_symmetry_03():
    mirror: Mirror2 = Mirror2.from_string(example_1)
    assert mirror.find_symmetry() == (Symmetry.vertical, 3)

def test_find_symmetry_04():
    mirror: Mirror2 = Mirror2.from_string(example_2)
    assert mirror.find_symmetry() == (Symmetry.vertical, 1)