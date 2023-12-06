# %% Import needed libraries
from pathlib import Path
from dataclasses import dataclass

# %% Classes defining the data structures in this problem 
@dataclass
class Draw:
    nb_red: int
    nb_green: int
    nb_blue: int

@dataclass
class Game:
    """Data representation of a Game
    """
    id: int
    hands: list[Draw]

    @classmethod
    def from_string(cls, string:str):
        """Create a Game instance from a string description

        Args:
            string (str): The result of the Game.

        Returns:
            Game: Game instance corresponding to the input string
        """
        game_id_string, game_result_string = string.split(':')
        game_id = int(game_id_string.replace("Game ", ""))
        
        hands = []
        for hand_string in game_result_string.split(";"):
            draw = Draw(0, 0, 0)
            for draw_string in hand_string.split(","):
                number, color = draw_string.strip().split(" ")
                number = int(number)
                match color:
                    case "red":
                        draw.nb_red += number
                    case "green":
                        draw.nb_green += number
                    case "blue":
                        draw.nb_blue += number
            hands.append(draw)
        
        return cls(game_id, hands)

    def is_possible(self, bag_content: Draw) -> bool:
        possible = True
        for draw in self.hands:
            locally_possible = (draw.nb_red <= bag_content.nb_red) and (draw.nb_green <= bag_content.nb_green) and (draw.nb_blue <= bag_content.nb_blue)
            possible = possible and locally_possible
        return possible
    
    def least_amount(self) -> Draw:
        min_draw = Draw(0, 0, 0)
        for i, draw in enumerate(self.hands):
            if i==0:
                min_draw = Draw(draw.nb_red, draw.nb_green, draw.nb_blue)
            else:
                min_draw = Draw(
                    max(min_draw.nb_red, draw.nb_red),
                    max(min_draw.nb_green, draw.nb_green),
                    max(min_draw.nb_blue, draw.nb_blue)
                )
        return min_draw                

    def __str__(self) -> str:
        return f"Game {self.id}: {self.hands}"
    
# Script parameters
input_filepath = Path("input")
bag_content = Draw(12, 13, 14)

# %% Open the input file
lines = input_filepath.read_text().splitlines()

# %% Solution to the first half of the problem
possible_ids = []
for line in lines:
    game = Game.from_string(line)
    if game.is_possible(bag_content):
        possible_ids.append(game.id)

print(sum(possible_ids))

# %% Solution to the second half of the problem
powers = []
for line in lines:
    game = Game.from_string(line)
    min_draw = game.least_amount()
    power = min_draw.nb_red * min_draw.nb_green * min_draw.nb_blue
    powers.append(power)
print(sum(powers))
