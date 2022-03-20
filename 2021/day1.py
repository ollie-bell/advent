import sys
import io
import requests

import numpy as np

_TEST = False


def load_input(session_id):
    if _TEST:
        return np.array([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
    r = requests.get(
        url="https://adventofcode.com/2021/day/1/input",
        cookies={"session": f"{session_id}"}
    )
    with io.StringIO(r.text) as f:
        data = np.loadtxt(f)
    return data


def part_one(input):
    diffs = input[1:] - input[:-1]
    return np.count_nonzero(diffs > 0)


def part_two(input):
    sums = np.convolve(input, [1, 1, 1], mode="valid")
    return part_one(sums)


if __name__ == "__main__":
    session_id = sys.argv[1] if not _TEST else None
    input = load_input(session_id)
    ans_1 = part_one(input)
    ans_2 = part_two(input)
    print(ans_1, ans_2)
