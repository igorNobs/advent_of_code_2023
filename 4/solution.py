from utils import get_file_dirname, read_file_lines
from math import pow


class Card:
    number: int | None
    winning_numbers: list[int]
    scratched_numbers: list[int]
    worth: int

    def __init__(
            self,
            number = None,
            winning_numbers: list[int] = [],
            scratched_numbers: list[int] = [],
            worth: int = 0
        ):
        self.number = number
        self.winning_numbers = winning_numbers
        self.scratched_numbers = scratched_numbers
        self.worth = worth

    def from_string(self, card_string: str) -> None:
        self.number = int(card_string[5:card_string.index(":")].strip())
        game_numbers = card_string[card_string.index(":") + 1:].strip()
        winning_str = game_numbers.split("|")[0]
        scratched_str = game_numbers.split("|")[1]
        self.winning_numbers = [int(i) for i in winning_str.split(" ") if i.isnumeric()]
        self.scratched_numbers = [int(i) for i in scratched_str.split(" ") if i.isnumeric()]

    def find_len_winners(self) -> int:
        winning_set = set(self.winning_numbers)
        scratched_set = set(self.scratched_numbers)
        winners = scratched_set.intersection(winning_set)
        return len(winners)

    def find_worth(self) -> int:
        if self.find_len_winners() == 0:
            return 0
        self.worth = int(pow(2, self.find_len_winners() - 1))
        return self.worth
    
    def find_next_cards(self) -> list[int]:
        if not self.find_len_winners():
            return []
        return [self.number + i for i in range(1, self.find_len_winners() + 1)]


def parse_cards(card_lines) -> list[Card]:
    cards = []
    for card_line in card_lines:
        c = Card()
        c.from_string(card_line)
        cards.append(c)
    return cards


def find_winners_per_card(card_number: int, all_cards: list[Card]):
    card = all_cards[card_number - 1]
    winners = card.find_next_cards()
    if winners:
        for c in winners.copy():
            winners += find_winners_per_card(c, all_cards)
    return winners
            


def main():
    dirname = get_file_dirname(__file__)
    card_lines = read_file_lines(f"{dirname}/input.txt")
    cards = parse_cards(card_lines)
    
    # sum_worth = 0
    # for c in cards:
    #     sum_worth += c.find_worth()
    # return sum_worth

    sum_won = 0
    for c in cards:
        sum_won += len(find_winners_per_card(c.number, cards))
    return sum_won + len(cards)
