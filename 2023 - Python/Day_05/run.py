# %%
from dataclasses import dataclass
from pathlib import Path

# %%
@dataclass
class Range:
    destination_start: int
    source_start: int
    length: int

    @classmethod
    def from_string(cls, string: str):
        destination_start, source_start, length = string.split(" ")
        return cls(int(destination_start), int(source_start), int(length))

    def is_in_range(self, value: int) -> bool:
        return value >= self.source_start and value < (self.source_start + self.length)

    def map(self, value: int) -> int:
        if self.is_in_range(value):
            return self.destination_start + value - self.source_start
        else:
            return value
        
    def map_range(self, _range) -> list:
        # print(self)
        # print(_range)
        result = []

        # Interval that falls before the range:
        # gap = min(_range.length, self.source_start - _range.destination_start)
        gap = self.source_start - _range.destination_start
        if gap > 0:
            length = min(_range.length, gap)
            # print(gap, length)
            result.append(Range(_range.destination_start, _range.source_start, length))
            _range = Range(_range.destination_start + length, _range.source_start + length, _range.length - length)
        
        # print(result)
        # print("=====")
        # print(self)
        # print(_range)

        # Interval that intersects with the range
        gap = self.source_start - _range.destination_start
        if gap <= 0 and abs(gap) < self.length:
            length = min(_range.length, self.length + gap)
            # print(gap, length)
            result.append(Range(self.destination_start - gap, _range.source_start, length))
            _range = Range(_range.destination_start + length, _range.source_start + length, _range.length - length)

        # print(result)
        # print("=====")
        # print(self)
        # print(_range)

        # Interval that falls after the range
        if _range.length > 0:
            result.append(_range)

        # print("~~~~~~")
        return result

# %%
@dataclass
class Map:
    source: str
    destination: str
    ranges: list[Range]

    @classmethod
    def from_string(cls, string: str):
        lines = string.splitlines()

        # Find the labels for source/destination
        map_label = lines[0].replace(" map:", "")
        source_label, destination_label = map_label.split("-to-")

        # Find the ranges
        ranges = []
        for line in lines[1:]:
            ranges.append(Range.from_string(line))

        return cls(source_label, destination_label, ranges)

    def map(self, value: int) -> int:
        for _range in self.ranges:
            if _range.is_in_range(value):
                return _range.map(value)
        return value
    
    def map_range(self, _range:Range) -> list:
        result = [_range]
        for blob in self.ranges:
            result.extend(blob.map_range(result[-1]))
        return result
    
    def is_mapping_from(self, source: str) -> bool:
        return source == self.source
    
    def mapping_to(self) -> str:
        return self.destination

    def is_mapping_from_to(self, source: str, destination: str) -> bool:
        return source == self.source and destination == self.destination

# %%
@dataclass
class Almanac:
    seeds: list[int]
    maps: list[Map]

    @classmethod
    def from_string(cls, string: str):
        entries = string.split("\n\n")

        seeds = [int(seed) for seed in entries[0].replace("seeds: ", "").split(" ")]

        maps = []
        for line in entries[1:]:
            if line != "":
                maps.append(Map.from_string(line))

        return cls(seeds, maps)
    
    def find_mapping_from(self, source:str) -> Map|None:
        for mapping in self.maps:
            if mapping.is_mapping_from(source):
                return mapping

    def map(self, value: int, source: str, destination: str):
        current_source = source
        current_value = value
        while current_source != destination:
            mapping = self.find_mapping_from(current_source)
            current_source = mapping.mapping_to()
            current_value = mapping.map(current_value)
        return current_value
    
    def map_range(self, _range: Range, source: str, destination: str) -> list[Range]:
        current_source = source
        current_ranges = [_range]
        while current_source != destination:
            mapping = self.find_mapping_from(current_source)
            current_source = mapping.mapping_to()
            current_ranges.extend(mapping.map_range(current_ranges[-1]))
        return current_ranges

# %%
input_file = Path("example.txt")
input_text = input_file.read_text()

# %% Solution to the first problem
almanac = Almanac.from_string(input_text)
location_numbers = []
for seed in almanac.seeds:
    location_numbers.append(almanac.map(seed, "seed", "location"))
print(min(location_numbers))

# %% Solution to the second problem 
from tqdm import tqdm
almanac = Almanac.from_string(input_text)

# # Too inefficient, would take dozens of hours !
# seeds = almanac.seeds
# location_numbers = []
# for i in tqdm(range(int(len(seeds)/2))):
#     start_seed = seeds[2*i]
#     length = seeds[2*i + 1]
#     for seed in tqdm(range(start_seed, start_seed + length)):
#         location_numbers.append(almanac.map(seed, "seed", "location"))
# print(min(location_numbers))

# TODO : Does not work, currently
almanac = Almanac.from_string(input_text)
for seed in almanac.seeds:
    print(almanac.map(seed, "seed", "location"))
    print(almanac.map_range(Range(seed, seed, 1), "seed", "location"))

