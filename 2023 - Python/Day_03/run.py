# %%
from dataclasses import dataclass
from pathlib import Path

# %%
@dataclass
class EngineCell:
    value: str
    is_digit: bool
    is_symbol: bool
    is_symbol_adjacent: bool
    adjacent_symbol_id: int

    @classmethod
    def from_string(cls, string:str):
        return EngineCell(
            value=string,
            is_digit=string.isdigit(),
            is_symbol=(not string.isdigit()) and (string != '.'),
            is_symbol_adjacent=False, # Default value for 'is_symbol_adjacent', updated according to the context during the construction of the engine
            adjacent_symbol_id=-1 # Default value for 'adjacent_symbol_id', updated according to the context during the construction of the engine
        )
    
    def add_adjacent_symbol(self, symbol_id:int):
        self.is_symbol_adjacent = True
        self.adjacent_symbol_id = symbol_id

# %%
@dataclass
class Engine:
    schematic: list[list[EngineCell]]
    symbols: list[str]

    @classmethod
    def from_string(cls, string:str):
        schematic: list[list[EngineCell]] = [] # "Array" of EngineCells to fill
        symbols: list[str] = [] # List of symbols, their index is their ID

        lines = string.splitlines()

        # Fill the "array" with EngineCells, without taking the adjency into account first
        for i, line in enumerate(lines):
            schematic.append([])
            for char in line:
                schematic[i].append(EngineCell.from_string(char))

        # Update the "array" with correct values of 'is_symbol_adjacent' and 'adjacent_symbol_id'
        for i, engine_cell_row in enumerate(schematic):
            for j, engine_cell in enumerate(engine_cell_row):
                if engine_cell.is_symbol:
                    symbols.append(engine_cell.value)

                    # Update neighbouring cells
                    for tmp_i in [-1, 0, 1]:
                        for tmp_j in [-1, 0, 1]:
                            if not(tmp_i == 0 and tmp_j == 0):
                                schematic[i+tmp_i][j+tmp_j].add_adjacent_symbol(len(symbols)-1)

        return cls(schematic, symbols)
                
    def find_part_numbers(self, restrict_to_symbol:str=None):
        part_numbers:list[list[int]] = [[] for _ in range(len(self.symbols))]
        reading_number = False
        number_read_string = ""
        number_read_is_adjacent = False
        number_read_associated_symbol = -1

        for i, engine_cell_row in enumerate(self.schematic):
            for j, engine_cell in enumerate(engine_cell_row):
                if engine_cell.is_digit:
                    reading_number = True
                    number_read_string += engine_cell.value
                    number_read_is_adjacent |= engine_cell.is_symbol_adjacent
                    number_read_associated_symbol = max(number_read_associated_symbol, engine_cell.adjacent_symbol_id)
                else:
                    if reading_number and number_read_is_adjacent and ((restrict_to_symbol is None) or restrict_to_symbol == self.symbols[number_read_associated_symbol]):
                        part_numbers[number_read_associated_symbol].append(int(number_read_string))
                    reading_number = False
                    number_read_string = ""
                    number_read_is_adjacent = False
                    number_read_associated_symbol = -1

        return part_numbers


# %% Open the input file
input_file = Path("input.txt")
# input_file = Path("example.txt")
text = input_file.read_text()

# %% Solution to the first problem
engine = Engine.from_string(text)
part_numbers = engine.find_part_numbers()
print(sum([sum(sub_part_numbers) for sub_part_numbers in part_numbers]))

# %% Solution to the second problem
engine = Engine.from_string(text)
part_numbers = engine.find_part_numbers(restrict_to_symbol='*')
gear_numbers = [tmp for tmp in part_numbers if len(tmp) == 2]
gear_ratios = [tmp[0]*tmp[1] for tmp in gear_numbers]
print(sum(gear_ratios))
