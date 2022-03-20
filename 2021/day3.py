import sys
import requests

from bitarray import bitarray
from bitarray.util import ba2int, count_and

_TEST = False


def input(session_id=None):
    if _TEST:
        data = """
            00100
            11110
            10110
            10111
            10101
            01111
            00111
            11100
            10000
            11001
            00010
            01010
        """.strip().replace(" ", "")
    else:
        r = requests.get(
            url="https://adventofcode.com/2021/day/3/input",
            cookies={"session": f"{session_id}"}
        )
        data = r.text
    n = data.find("\n")
    return bitarray(data), n


def part_one(data, n):
    gamma = bitarray()
    for i in range(n):
        count1 = data[i::n].count(1)
        count0 = data[i::n].count(0)
        gamma.append(0 if count0 > count1 else 1)
    return ba2int(gamma) * ba2int(~gamma)


def part_two(data, n):
    oxygen_rating = data
    for i in range(1):
        current_bits = oxygen_rating[i::n]
        count1 = current_bits.count(1)
        count0 = current_bits.count(0)
        remove_bits = current_bits.search(0) if count1 >= count0 else current_bits.search(1)
        # print(remove_bits)


if __name__ == "__main__":
    session_id = sys.argv[1] if not _TEST else None
    data, n  = input(session_id)
    ans_1 = part_one(data, n)
    ans_2 = part_two(data, n)
    print(ans_1, ans_2)
