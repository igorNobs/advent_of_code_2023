from utils import get_file_dirname, read_file_lines


WORD_NUMS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def get_word(substring: str) -> int:
    for word in WORD_NUMS.keys():
        if word in substring:
            return WORD_NUMS[word]
    return 0


def get_num(char: str) -> int:
    try:
        return int(char)
    except ValueError:
        return 0


def calibration_nums(calibration_str: str):
    num1 = None
    for i in range(len(calibration_str)):
        word_num = get_word(calibration_str[0:i])
        char_num = get_num(calibration_str[i])
        if not word_num and not char_num:
            continue
        num1 = word_num or char_num
        break
    num2 = None
    for j in range(len(calibration_str)-1, -1, -1):
        word_num = get_word(calibration_str[j:])
        char_num = get_num(calibration_str[j])
        if not word_num and not char_num:
            continue
        num2 = word_num or char_num
        break
    return int(f"{num1}{num2}")


def main():
    dirname = get_file_dirname(__file__)
    codes = read_file_lines(f"{dirname}/input.txt")

    running_sum = 0
    for code in codes:
        running_sum += calibration_nums(code)
    return running_sum
