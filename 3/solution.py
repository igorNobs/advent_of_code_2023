from utils import get_file_dirname, read_file_lines
import pdb


def is_symbol(character: str) -> bool:
    return character != "." and not character.isnumeric() and character != "\n"


def is_gear(character: str) -> bool:
    return character == "*"


def scan_360_of(
        lines: list[str],
        i: int,
        j: int,
    ) -> list[tuple[int, int]]:
    """
    @return: All positions where numbers are found 360 around the symbol
    """
    positions = []
    start_j = j - 1 if j > 0 else 0
    check_span_j = 3 if j > 0 else 2

    # check three positions starting i - 1 & j - 1
    if i > 0:
        start_i = i - 1
        try:
            for k in range(start_j, start_j + check_span_j):
                if lines[start_i][k].isnumeric():
                    positions.append((start_i, k))
        except IndexError:
            pass

    # check three positions starting i & j - 1
    try:
        for k in range(start_j, start_j + check_span_j):
            if lines[i][k].isnumeric():
                positions.append((i, k))
    except IndexError:
        pass

    # check three positions starting i + 1 & j - 1
    if i < len(lines) - 1:
        start_i = i + 1
        try:
            for k in range(start_j, start_j + check_span_j):
                if lines[start_i][k].isnumeric():
                    positions.append((start_i, k))
        except IndexError:
            pass
    return positions


def get_numbers_boundaries(lines: list[str], positions: list[tuple[int, int]]) -> set[tuple[int, int]]:
    boundaries = set()
    for position in positions:
        i, j = position
        left_boundary = 0
        right_boundary = len(lines[i]) - 1
        for k in range(j, -1, -1):
            if lines[i][k].isnumeric():
                left_boundary = k
                continue
            break
        for k in range(j, len(lines[i])):
            if lines[i][k].isnumeric():
                right_boundary = k
                continue
            break
        boundaries.add((i, left_boundary, right_boundary))
    return boundaries


def get_all_nums_sum(lines: list[str], boundaries: set[tuple]):
    sum = 0
    for b in boundaries:
        line, left, right = b
        sum += int(lines[line][left:right+1])
    return sum


def get_all_nums_product(lines: list[str], boundaries: set[tuple]):
    sum = 1
    for b in boundaries:
        line, left, right = b
        sum = sum * int(lines[line][left:right+1])
    return sum


def main():
    dirname = get_file_dirname(__file__)
    schematic_lines = read_file_lines(f"{dirname}/input.txt")
    all_boundaries = set()
    sum = 0
    # detect a symbol and scan 360 degrees around a symbol, locating a number
    # given an arbitrary position of a cursor in a number string find it's left and right boundaries
    for i in range(len(schematic_lines)):
        for j in range(len(schematic_lines[i])):
            if is_gear(schematic_lines[i][j]):
                number_positions_around_symbol = scan_360_of(schematic_lines, i, j)
                boundaries = get_numbers_boundaries(schematic_lines, number_positions_around_symbol)
                if len(boundaries) == 2:
                    sum += get_all_nums_product(schematic_lines, boundaries)

                # all_boundaries.update(
                #     get_numbers_boundaries(schematic_lines, number_positions_around_symbol)
                # )
    # return get_all_nums_sum(schematic_lines, all_boundaries)
    return sum