# %%
from dataclasses import dataclass
from pathlib import Path

# %%
@dataclass
class Boat:
    starting_speed: int = 0
    speed_increase_p_ms: int = 1
    current_speed: int = 0

    def get_speed(self) -> current_speed:
        return self.current_speed

    def update_speed(self, time_pushed: int) -> None:
        self.current_speed = self.starting_speed + time_pushed*self.speed_increase_p_ms

    def distance_traveled(self, time: int) -> int:
        return self.current_speed * time

# %%
@dataclass
class Race:
    time_length: int
    record_distance: int

    def beats_record(self, boat: Boat, time_pushed:int) -> bool:
        time_left = self.time_length - time_pushed
        distance_traveled = boat.distance_traveled(time_left)
        return distance_traveled > self.record_distance
    
    def find_all_winning_combinations(self) -> list[int]:
        winning_combinations = []
        for time in range(self.time_length + 1):
            boat = Boat()
            boat.update_speed(time)
            if self.beats_record(boat, time):
                winning_combinations.append(time)
        return winning_combinations
    
    def faster_find_all_winning_combinations(self) -> list[int]:
        range_start = -1
        for time in range(self.time_length+1):
            boat = Boat()
            boat.update_speed(time)
            if self.beats_record(boat, time):
                range_start = time
                break

        range_end = -1
        for time in range(self.time_length, -1, -1):
            boat = Boat()
            boat.update_speed(time)
            if self.beats_record(boat, time):
                range_end = time
                break

        return [time for time in range(range_start, range_end+1)]
   
# %%
def build_races_first_problem(string:str) -> list[Race]:
    lines = string.splitlines()
    times = [int(time) for time in lines[0].split()[1:]]
    distances = [int(distance) for distance in lines[1].split()[1:]]
    
    races = [Race(time, distance) for (time, distance) in zip(times, distances)]
    return races

def build_race_second_problem(string:str) -> Race:
    lines = string.splitlines()
    times = [time for time in lines[0].split()[1:]]
    distances = [distance for distance in lines[1].split()[1:]]

    time = int("".join(times))
    distance = int("".join(distances))

    return Race(time, distance)       
    
# %%
if __name__ == "__main__":
    input_file = Path("input.txt")
    input_text = input_file.read_text()

    # %% Solution to the first problem
    races = build_races_first_problem(input_text)
    product = 1
    for race in races:
        winning_combinations = race.find_all_winning_combinations()
        product *= len(winning_combinations)
    print(product)

    # %% Solution to the second problem.
    race = build_race_second_problem(input_text)
    winning_combinations = race.find_all_winning_combinations()
    print(len(winning_combinations))

    # %% Previous solution takes approx. 1 minute. Smarter way to do things would be taking profit of the fact that the answer is always a single interval.
    # We could find the low and high values of this interval without verifying that all values in the interval are correct (we know they are)
    race = build_race_second_problem(input_text)
    winning_combinations = race.faster_find_all_winning_combinations()
    print(len(winning_combinations))