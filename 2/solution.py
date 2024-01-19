from utils import get_file_dirname, read_file_lines


AVAILABLE = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


class Draw:
    def __init__(
        self,
        red: int = 0,
        green: int = 0,
        blue: int = 0,
    ) -> None:
        self.red = red
        self.green = green
        self.blue = blue

    def possible(self) -> bool:
        return self.red <= AVAILABLE["red"] \
            and self.green <= AVAILABLE["green"] \
            and self.blue <= AVAILABLE["blue"]
    
    def populate_from_str(self, draw_str: str):
        for cubes in draw_str.split(", "):
            if "red" in cubes:
                _num = int(cubes.replace(" red", ""))
                self.red = _num
            if "green" in cubes:
                _num = int(cubes.replace(" green", ""))
                self.green = _num
            if "blue" in cubes:
                _num = int(cubes.replace(" blue", ""))
                self.blue = _num


class Game:
    def __init__(self, id: int) -> None:
        self.id = id
        self.draws: list[Draw] = []

    def possible(self) -> bool:
        return all([draw.possible() for draw in self.draws])
    
    def add_draw(self, draw_str: str):
        d = Draw()
        d.populate_from_str(draw_str)
        self.draws.append(d)

    def get_power(self):
        max_red = 0
        max_green = 0
        max_blue = 0
        for draw in self.draws:
            if draw.red > max_red:
                max_red = draw.red
            if draw.green > max_green:
                max_green = draw.green
            if draw.blue > max_blue:
                max_blue = draw.blue
        max_red = max_red if max_red > 0 else 1
        max_green = max_green if max_green > 0 else 1
        max_blue = max_blue if max_blue > 0 else 1
        return max_red * max_blue * max_green

def main():
    dirname = get_file_dirname(__file__)
    games = read_file_lines(f"{dirname}/input.txt")
    # parse input
    parsed_games = []
    for game in games:
        _g = game.split(":")
        parsed_game = Game(int(_g[0].replace("Game ", "")))
        for _d in _g[1].split("; "):
            parsed_game.add_draw(_d.strip())
        parsed_games.append(parsed_game)
    # sum of possible game IDs
    sum = 0
    for game in parsed_games:
        # if game.possible():
        sum += game.get_power()
    
    return sum
