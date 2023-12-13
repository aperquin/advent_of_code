# %%
from dataclasses import dataclass
from pathlib import Path
from enum import Enum
from abc import ABC, abstractmethod
import numpy as np

Surface = Enum("Surface", ["ash", "rock"])
Symmetry = Enum("Symmetry", ["horizontal", "vertical"])

# %%
@dataclass
class MirrorAbstract(ABC):
    pattern: np.ndarray

    @classmethod
    def from_string(cls, string: str):
        pattern = []
        for line in string.strip().splitlines():
            # row = [Surface.rock if char == '#' else Surface.ash for char in line]
            row = [0 if char == '#' else 1 for char in line]
            pattern.append(row)

        return cls(np.array(pattern))

    def has_horizontal_symmetry_at(self, index: int) -> bool:
        # Split the pattern around the given index
        left_pattern = self.pattern[:, :index]
        right_pattern = self.pattern[:, index:]

        # Resize the parts to be equal length
        len_difference = abs(left_pattern.shape[-1] - right_pattern.shape[-1])
        if left_pattern.shape[-1] > right_pattern.shape[-1]:
            left_pattern = left_pattern[:, len_difference:]
        elif left_pattern.shape[-1] < right_pattern.shape[-1]:
            right_pattern = right_pattern[:, :-len_difference]

        # Flip the right pattern to check if it is equal to the left one
        right_pattern = np.flip(right_pattern, axis=-1)

        return self.array_equal_has_symmetry(left_pattern, right_pattern)

    def has_vertical_symmetry_at(self, index: int) -> bool:
        # Split the pattern around the given index
        up_pattern = self.pattern[:index, :]
        down_pattern = self.pattern[index:, :]

        # Resize the parts to be equal length
        len_difference = abs(up_pattern.shape[0] - down_pattern.shape[0])
        if up_pattern.shape[0] > down_pattern.shape[0]:
            up_pattern = up_pattern[len_difference:, :]
        elif up_pattern.shape[0] < down_pattern.shape[0]:
            down_pattern = down_pattern[:-len_difference, :]

        # Flip the down pattern to check if it is equal to the upper one
        down_pattern = np.flip(down_pattern, axis=0)

        return self.array_equal_has_symmetry(up_pattern, down_pattern)

    def find_symmetry(self) -> tuple[Symmetry, int]:
        # Check horizontal symmetry
        length = self.pattern.shape[-1]
        for i in range(length-1):
            if self.array_equal_find_symmetry(self.pattern[:, i], self.pattern[:, i+1]):
                if self.has_horizontal_symmetry_at(i+1):
                    return (Symmetry.horizontal, i+1)
        
        # Check vertical symmetry
        length = self.pattern.shape[0]
        for i in range(length-1):
            if self.array_equal_find_symmetry(self.pattern[i, :], self.pattern[i+1, :]):
                if self.has_vertical_symmetry_at(i+1):
                    return (Symmetry.vertical, i+1)
                
        raise Exception("No symmetry found")
    
    @staticmethod
    @abstractmethod
    def array_equal_find_symmetry(array1: np.ndarray, array2: np.ndarray) -> bool:
        raise NotImplementedError()
    
    @staticmethod
    @abstractmethod
    def array_equal_has_symmetry(array1: np.ndarray, array2: np.ndarray) -> bool:
        raise NotImplementedError()
    
# %%
class Mirror(MirrorAbstract):
    @staticmethod
    def array_equal_find_symmetry(array1: np.ndarray, array2: np.ndarray) -> bool:
        return np.array_equal(array1, array2)
    
    @staticmethod
    def array_equal_has_symmetry(array1: np.ndarray, array2: np.ndarray) -> bool:
        return np.array_equal(array1, array2)
    
# %%
class Mirror2(MirrorAbstract):
    @staticmethod
    def array_equal_find_symmetry(array1: np.ndarray, array2: np.ndarray) -> bool:
        return np.count_nonzero(array1 != array2) <= 1
    
    @staticmethod
    def array_equal_has_symmetry(array1: np.ndarray, array2: np.ndarray) -> bool:
        return np.count_nonzero(array1 != array2) == 1
        

# %%
if __name__ == "__main__":
    # %%
    input_file = Path("input.txt")
    input_text = input_file.read_text().strip()

    # %% Solution to the first problem
    total = 0
    for mirror_string in input_text.split("\n\n"):
        mirror = Mirror.from_string(mirror_string)
        symmetry_type, symmetry_index = mirror.find_symmetry()

        if symmetry_type == Symmetry.horizontal:
            total += symmetry_index
        elif symmetry_type == Symmetry.vertical:
            total += 100*symmetry_index

    print(total)

    # %% Solution to the second problem
    total = 0
    for mirror_string in input_text.split("\n\n"):
        mirror = Mirror2.from_string(mirror_string)
        symmetry_type, symmetry_index = mirror.find_symmetry()

        if symmetry_type == Symmetry.horizontal:
            total += symmetry_index
        elif symmetry_type == Symmetry.vertical:
            total += 100*symmetry_index

    print(total)
