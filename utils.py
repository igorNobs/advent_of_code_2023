import os


def read_file_lines(path: str) -> list[str]:
    result = []
    with open(path, "r") as f:
        while line := f.readline():
            result.append(line)
    return result


def get_file_dirname(file: str) -> str:
    return os.path.dirname(file)
