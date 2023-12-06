from run import Boat, Race

def test_Boat_update_speed_01():
    boat_1 = Boat()
    boat_1.update_speed(0)

    boat_2 = Boat()
    boat_2.update_speed(2)
    
    assert boat_1.get_speed() == 0 and boat_2.get_speed() == 2

def test_Boat_distance_traveled_01():
    boat_1 = Boat()
    boat_1.update_speed(0)
    
    boat_2 = Boat()
    boat_2.update_speed(1)

    boat_3 = Boat()
    boat_3.update_speed(4)

    boat_4 = Boat()
    boat_4.update_speed(7)

    assert boat_1.distance_traveled(7) == 0 and boat_2.distance_traveled(6) == 6 and boat_3.distance_traveled(3) == 12 and boat_4.distance_traveled(0) == 0

def test_Race_beats_record_01():
    race = Race(7, 9)
    solution = []
    proposed_solution = []
    for i in range(0, 7+1):
        boat = Boat()
        boat.update_speed(i)
        proposed_solution.append(race.beats_record(boat, i))
        solution.append(False if (i<2 or i>5) else True)
    assert solution == proposed_solution

def test_Race_beats_record_01():
    race = Race(15, 40)
    solution = []
    proposed_solution = []
    for i in range(0, 15+1):
        boat = Boat()
        boat.update_speed(i)
        proposed_solution.append(race.beats_record(boat, i))
        solution.append(False if (i<4 or i>11) else True)
    assert solution == proposed_solution
