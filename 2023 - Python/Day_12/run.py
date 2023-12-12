# %%
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

# %%
Spring_State = Enum("Spring_State", ["operational", "damaged", "unknown"])

# %%
@dataclass
class Row:
    spring_states: list[Spring_State]
    damaged_numbers: list[int]

    @classmethod
    def from_string(cls, string: str):
        spring_states_string, damaged_numbers_string = string.strip().split(" ")
        
        spring_states = []
        for spring_states_char in spring_states_string:
            match spring_states_char:
                case ".":
                    spring_states.append(Spring_State.operational)
                case "#":
                    spring_states.append(Spring_State.damaged)
                case "?":
                    spring_states.append(Spring_State.unknown)

        damaged_numbers = []
        for damaged_number_char in damaged_numbers_string.split(','):
            damaged_numbers.append(int(damaged_number_char))

        return cls(spring_states, damaged_numbers)

    @staticmethod
    def compute_damaged_numbers(spring_states: list[Spring_State]) -> list[int]:
        damaged_numbers = []
        
        # Fing group of damaged springs and count them
        parsing_damaged_group = False
        damaged_group_size = 0
        for spring_state in spring_states:
            if spring_state == Spring_State.damaged:
                parsing_damaged_group = True
                damaged_group_size += 1
            else:
                if parsing_damaged_group:
                    damaged_numbers.append(damaged_group_size)
                    damaged_group_size = 0
                    parsing_damaged_group = False
        
        # Deal with the case of a group of damaged springs at the end of the sequence
        if parsing_damaged_group:
            damaged_numbers.append(damaged_group_size)

        return damaged_numbers

    def is_valid(self, spring_states: list[Spring_State]) -> bool:
        if len(spring_states) != len(self.spring_states):
            return False
        
        correct_sequence = True # Not necessary if we assume the sequence was correctly built
        # for i, spring_state in enumerate(spring_states):
        #     correct_sequence = correct_sequence and ((spring_state == self.spring_states[i]) or (self.spring_states[i] == Spring_State.unknown))

        correct_damage = self.compute_damaged_numbers(spring_states) == self.damaged_numbers

        return correct_sequence and correct_damage
    
    def find_number_valid_arrangements(self) -> int:
        def recursive_function(i: int, building_states: list[Spring_State]):
            # Terminal case: we built the entire sequence
            if len(building_states) == len(self.spring_states):
                if self.is_valid(building_states):
                    return 1
                else:
                    return 0
            
            # General Case: we build all valid possible sequences recursively
            else:
                # TODO : Add a "if still possible" check
                if self.spring_states[i] != Spring_State.unknown:
                    return recursive_function(i+1, building_states + [self.spring_states[i]])
                else:
                    return recursive_function(i+1, building_states + [Spring_State.damaged]) + recursive_function(i+1, building_states + [Spring_State.operational])
                
        return recursive_function(0, [])

# %%
class Row2(Row):
    @classmethod
    def from_string(cls, string: str):
        spring_states_string, damaged_numbers_string = string.strip().split(" ")
        spring_states_string = "?".join([spring_states_string for _ in range(5)])
        damaged_numbers_string = ",".join([damaged_numbers_string for _ in range(5)])
        return super().from_string(f"{spring_states_string} {damaged_numbers_string}")

# %%
input_file = Path("example.txt")
input_text = input_file.read_text()

# %% Solution to the first problem
from tqdm import tqdm 
total_number = 0
for line in tqdm(input_text.splitlines()):
    total_number += Row.from_string(line).find_number_valid_arrangements()
print(total_number)

# %% Solution to the second problem
from tqdm import tqdm 
total_number = 0
for line in tqdm(input_text.splitlines()):
    total_number += Row2.from_string(line).find_number_valid_arrangements()
print(total_number)
