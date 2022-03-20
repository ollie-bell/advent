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
        numbers, *boards = io.StringIO(r.text)
        boards = np.loadtxt(boards, dtype=np.int8).reshape(-1, 5, 5)
        numbers = np.loadtxt(numbers.split(','), dtype=np.int8)
    return numbers, boards


# @profile
def my_answer(numbers, boards):
    mask = np.zeros_like(boards, dtype=bool)
    check_prev = np.zeros(boards.shape[0], dtype=bool)
    for n in numbers: 
        mask[boards == n] = True
        check_bingo = (mask.all(axis=2) | mask.all(axis=1)).any(axis=-1)
        if check_bingo.any() and not check_prev.any():
            pos = check_bingo.argmax()
            board = boards[pos]
            score1 = n * board.sum(where=~mask[pos])
        if check_bingo.all():
            pos = (check_bingo & check_prev).argmin()
            board = boards[pos]
            score2 = n * board.sum(where=~mask[pos])
            return score1, score2
        check_prev = check_bingo


# @profile
def my_answer2(numbers, boards):
    all_rounds = np.logical_or.accumulate(boards[np.newaxis, ...] == numbers.reshape(-1, 1, 1, 1))
    find_bingo = (all_rounds.all(axis=3) | all_rounds.all(axis=2)).any(axis=-1)
    bingo_rounds = find_bingo.argmax(axis=0)
    bingo_order = bingo_rounds.argsort()
    mask = all_rounds[bingo_rounds[bingo_order], bingo_order, ...]
    return numbers[bingo_rounds[bingo_order]] * boards[bingo_order].sum(axis=(1, 2), where=~mask)


# @profile
def reddit_answer(numbers, boards):
    n = numbers.reshape(-1,1,1,1)
    b = boards.reshape(1,-1,5,5)
    m = (n == b).cumsum(0)
    s = (n * b * (1-m)).sum((2,3))
    w = (m.all(2) | m.all(3)).any(2).argmax(0)
    return s[w].diagonal()[w.argsort()[[0,-1]]]


# @profile
def reddit_answer2(numbers, boards):
    b = boards
    for n in numbers:
        b[b == n] = -1
        m = (b == -1)
        win = (m.all(1) | m.all(2)).any(1)
        if win.any():
            score = (b * ~m)[win].sum() * n
            b = b[~win]


if __name__ == "__main__":
    session_id = sys.argv[1] if not _TEST else None
    numbers, boards = load_input(session_id)
    print(my_answer(numbers, boards))
    print(my_answer2(numbers, boards)[[0, -1]])
    print(reddit_answer(numbers, boards.astype(int)))
    print(reddit_answer2(numbers, boards.astype(int)))
