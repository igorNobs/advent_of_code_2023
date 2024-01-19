import sys
import importlib


if __name__ == "__main__":
    advent_day = sys.argv[1]
    solution = importlib.import_module(f"{advent_day}.solution")
    result = solution.main()
    print(result)
