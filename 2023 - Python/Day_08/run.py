# %%
from dataclasses import dataclass
from abc import ABC, abstractmethod
from pathlib import Path
from multiprocessing import Pool
from itertools import repeat

# %%
@dataclass
class Node:
    _id: str
    _left_id: str
    _right_id: str

    @classmethod
    def from_string(cls, string: str):
        current_id, remaining_string = string.split(" = ")
        left_id, right_id = remaining_string.replace("(", "").replace(")", "").split(", ")
        return cls(current_id, left_id, right_id)

    def next_node_id(self, instruction: str) -> str:
        if instruction == "L":
            return self._left_id
        elif instruction == "R":
            return self._right_id
        else:
            raise ValueError("Instruction should be one either 'L' or 'R'.")

# %%
@dataclass
class Network(ABC):
    _nodes: dict[str, Node]

    @abstractmethod
    def compute_starting_nodes(self) -> list[Node]: pass

    @abstractmethod
    def compute_ending_nodes(self) -> list[Node]: pass

    @classmethod
    def from_string(cls, string: str):
        lines = string.splitlines()

        nodes = dict()
        for line in lines:
            node = Node.from_string(line)
            nodes[node._id] = node

        return cls(nodes)

    def nb_steps_solve(self, starting_nodes: list[str], ending_nodes: list[str], instruction: str) -> int:
        print(starting_nodes)
        current_node_ids = starting_nodes
        nb_steps = 0
        i = 0
        while not all([node_id in ending_nodes for node_id in current_node_ids ]):#current_node_id != "ZZZ":
            instruction_char = instruction[i]
            current_node_ids = [self._nodes[node_id].next_node_id(instruction_char) for node_id in current_node_ids]
            nb_steps += 1
            if i < len(instruction) - 1:
                i += 1
            else:
                i = 0

        return nb_steps, current_node_ids
    
    def nb_steps_solve_multithread(self, instruction: str) -> int:
        starting_nodes = self.compute_starting_nodes()
        ending_nodes = self.compute_ending_nodes()

        print(starting_nodes)
        print(ending_nodes)

        print("=============")

        for i in range(len(starting_nodes)):
            print(self.nb_steps_solve([starting_nodes[i]], ending_nodes, instruction))

        print(*zip([[starting_nodes[i]] for i in range(len(starting_nodes))], repeat(ending_nodes), repeat(instruction)))
       
        print("=============")
        
        with Pool(len(starting_nodes)) as pool:
            print("Pool Started")
            result = pool.starmap(self.nb_steps_solve, zip([[starting_nodes[i]] for i in range(len(starting_nodes))], repeat(ending_nodes), repeat(instruction)))
        return result


class Network1(Network):
    def compute_starting_nodes(self) -> list[Node]:
        return ["AAA"]
    
    def compute_ending_nodes(self) -> list[Node]:
        return ["ZZZ"]
    
class Network2(Network):
    def _find_nodes_ids_ending_with(self, letter: str) -> list[str]:
        node_ids = []
        for node_key in self._nodes:
            node = self._nodes[node_key]
            if node._id.endswith(letter):
                node_ids.append(node._id)

        return node_ids

    def compute_starting_nodes(self) -> list[Node]:
        return self._find_nodes_ids_ending_with("A")
    
    def compute_ending_nodes(self) -> list[Node]:
        return self._find_nodes_ids_ending_with("Z")
        

# %%
input_file = Path("input.txt")
input_text = input_file.read_text()

# %% Solution to the first problem
instruction_str, network_str  = input_text.split("\n\n")
network = Network1.from_string(network_str)
print(network.nb_steps_solve(network.compute_starting_nodes(), network.compute_ending_nodes(), instruction_str))

# # # %% Solution to the second problem : not working
# # instruction_str, network_str  = input_text.split("\n\n")
# # network = Network2.from_string(network_str)
# # print(network.nb_steps_solve(instruction_str))

# # %%
# instruction_str, network_str  = input_text.split("\n\n")
# network = Network2.from_string(network_str)
# print(network.nb_steps_solve_multithread(instruction_str))
# # %%
