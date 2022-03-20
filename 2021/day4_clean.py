import numpy as np

numbers, *boards = open("input.txt", "r")
boards = np.loadtxt(boards, dtype=np.int8).reshape(-1, 5, 5)
numbers = np.loadtxt(numbers.split(','), dtype=np.int8)

all_rounds = np.logical_or.accumulate(boards[np.newaxis, ...] == numbers.reshape(-1, 1, 1, 1))
find_bingo = (all_rounds.all(axis=3) | all_rounds.all(axis=2)).any(axis=-1)
bingo_rounds = find_bingo.argmax(axis=0)
bingo_order = bingo_rounds.argsort()
mask = all_rounds[bingo_rounds[bingo_order], bingo_order, ...]
scores = numbers[bingo_rounds[bingo_order]] * boards[bingo_order].sum(axis=(1, 2), where=~mask)

print(scores)
