import sys
import io
import requests

import numpy as np

_TEST = False


def load_input(session_id=None):
    if _TEST:
        numbers = np.array(
            [7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1],
            dtype=np.int8
        )
        boards = np.array(
            [
                [
                    [22, 13, 17, 11, 0],
                    [8, 2, 23, 4, 24],
                    [21, 9, 14, 16, 7],
                    [6, 10, 3, 18, 5],
                    [1, 12, 20, 15, 19]
                ], 
                [
                    [3, 15, 0, 2, 22],
                    [9, 18, 13, 17, 5],
                    [19, 8, 7, 25, 23],
                    [20, 11, 10, 24, 4],
                    [14, 21, 16, 12, 6]
                ],
                [
                    [14, 21, 17, 24, 4],
                    [10, 16, 15, 9, 19],
                    [18,  8, 23, 26, 20],
                    [22, 11, 13, 6, 5],
                    [2,  0, 12, 3, 7]
                ]
            ], 
            dtype=np.int8
        )
    else:
        r = requests.get(
            url="https://adventofcode.com/2021/day/4/input",
            cookies={"session": f"{session_id}"}
        )
        with io.StringIO(r.text) as f:
            data = f.read().split("\n\n")
        numbers = np.fromstring(data[0], sep=",", dtype=int)
        boards = [d.replace("\n", " ").replace("  ", " ").strip() for d in data[1:]]
        boards = [np.fromstring(b, sep=" ", dtype=int).reshape(5, 5) for b in boards]
        boards = np.stack(boards, axis=0)
    return numbers, boards


def part_one(numbers, boards):
    for n in numbers:
        boards[boards == n] = -1
        sums = np.stack([boards.sum(axis = i) for i in (1, 2)], axis=-1)
        if (sums == -5).any():
            winning_board = boards[np.where(sums == -5)[0][0]]
            return winning_board[winning_board >= 0].sum() * n


def part_two(numbers, boards):
    check_prev = np.zeros(boards.shape[0], dtype=bool)
    for n in numbers:
        boards[boards == n] = -1
        sums = np.stack([boards.sum(axis = i) for i in (1, 2)], axis=-1)
        check = (sums == -5).any(axis=(1, 2))
        if check.all():
            winning_board = boards[np.where(check != check_prev)[0][0]]
            return winning_board[winning_board >= 0].sum() * n
        check_prev = check


if __name__ == "__main__":
    session_id = sys.argv[1] if not _TEST else None
    numbers, boards = load_input(session_id)
    ans_1 = part_one(numbers, boards.copy())
    ans_2 = part_two(numbers, boards.copy())
    print(ans_1, ans_2)
