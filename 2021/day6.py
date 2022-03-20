import sys
import io
import requests

import numpy as np
from collections import Counter

_TEST = False


def load_input(session_id=None):
    if _TEST:
        return [3, 4, 3, 1, 2]
    r = requests.get(
        url="https://adventofcode.com/2021/day/6/input",
        cookies={"session": f"{session_id}"}
    )
    return list(map(int, r.text.split(",")))


def part_one(data, days):
    data = np.asarray(data, dtype=np.int8)
    arr = np.empty(int(1e8), dtype=data.dtype)
    mask = np.empty(arr.size, dtype=bool)
    n = data.size
    arr[:n] = data[:].copy()
    current = arr[:n]
    mask_current = mask[:n]
    for _ in range(days):
        mask_current = current != 0
        nz_count = np.count_nonzero(mask_current)
        zero_count = n - nz_count
        n += zero_count
        current[mask_current] -= 1
        current[~mask_current] = 6
        current = arr[:n]
        mask_current = mask[:n]
        current[n:n-zero_count-1:-1] = 8
    return current.size


if __name__ == "__main__":
    session_id = sys.argv[1] if not _TEST else None
    data = load_input(session_id)
    ans_1 = part_one(data, 80)
    print(ans_1)
