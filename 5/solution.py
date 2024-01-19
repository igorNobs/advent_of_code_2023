import bisect
from utils import get_file_dirname, read_file_lines


class RangeMapping:
    dest_range_start: int
    src_range_start: int
    range_len: int

    def __init__(
        self,
        dest_range_start: int,
        src_range_start: int,
        range_len: int,
    ) -> None:
        self.dest_range_start = dest_range_start
        self.src_range_start = src_range_start
        self.range_len = range_len

    def __str__(self) -> str:
        return f"src start: {self.src_range_start}, dest start: {self.dest_range_start}, range len: {self.range_len}\n"


class LookupTable:
    ranges: list[RangeMapping]
    src: str
    dest: str

    def __init__(
        self,
        src: str,
        dest: str,
        ranges: list[RangeMapping] | None = None
    ) -> None:
        self.src = src
        self.dest = dest
        if not ranges:
            self.ranges = []

    def add_range(self, search_range: RangeMapping):
        """Add range to the list, keep it sorted by src"""
        bisect.insort(self.ranges, search_range, key=lambda rm: rm.src_range_start)

    def get_destination_for(self, source: int) -> int:
        found_range: RangeMapping = None
        for r in self.ranges:
            if source in range(r.src_range_start, r.src_range_start + r.range_len):
                found_range = r
                break

        if found_range:
            dest_diff = source - found_range.src_range_start
            return found_range.dest_range_start + dest_diff

        return source

    def __str__(self) -> str:
        s = f"[Obj {self.__hash__()}]: {self.src} to {self.dest}\n"
        for r in self.ranges:
            s += str(r)
        return s


def get_seeds(input_lines: list[str]) -> list[int]:
    start_i = input_lines[0].index(":") + 1
    seeds_str = input_lines[0][start_i:].strip()
    # return [int(seed) for seed in seeds_str.split(" ")]
    seed_ranges = [int(seed) for seed in seeds_str.split(" ")]
    seeds = []
    while seed_ranges:
        start = seed_ranges.pop(0)
        rng = seed_ranges.pop(0)
        print(start, rng)
        for i in range(start, start + rng):
            seeds.append(i)
    return seeds


def build_lookups(input_lines: list[str]) -> list[LookupTable]:
    
    def parse_table_name(name_str: str) -> tuple[str, str]:
        end_i = name_str.index("map") - 1
        src_to_dest_str = name_str[:end_i].strip()
        src_to_dest = src_to_dest_str.split("-")
        return src_to_dest[0], src_to_dest[2]
    
    def parse_range_mapping(rm_str: str) -> tuple[str, str, str]:
        mapping_list = [int(i) for i in rm_str.strip().split(" ")]
        return mapping_list[0], mapping_list[1], mapping_list[2]
    
    lookup_tables = []

    for line in input_lines[2:]:
        if len(line.strip()) > 0 and not line[0].isnumeric():
            src, dest = parse_table_name(line)
            table = LookupTable(src, dest)
            lookup_tables.append(table)
        elif len(line.strip()) > 0 and line[0].isnumeric():
            dest_range_start, src_range_start, range_len = parse_range_mapping(line)
            range_mapping = RangeMapping(dest_range_start, src_range_start, range_len)
            lookup_tables[-1].add_range(range_mapping)
    
    return lookup_tables    


def get_seeds_locations(seeds: list[int], lookup_tables: list[LookupTable]) -> list[int]:
    seed_to_location = {s: None for s in seeds}
    for seed in seeds:
        for table in lookup_tables:
            src = seed if seed_to_location[seed] is None else seed_to_location[seed]
            seed_to_location[seed] = table.get_destination_for(src)
    return seed_to_location            


def main():
    dirname = get_file_dirname(__file__)
    input_lines = read_file_lines(f"{dirname}/input.txt")
    seeds = get_seeds(input_lines)
    print(seeds)
    # tables = build_lookups(input_lines)
    # seeds_to_locations = get_seeds_locations(seeds, tables)
    # return min(*seeds_to_locations.values())
