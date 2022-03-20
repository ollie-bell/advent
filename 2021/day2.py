import sys
import io
import requests

import pandas as pd

_TEST = False


def load_input(session_id=None):
    if _TEST:
        return pd.DataFrame(
            data=[["forward", 5], ["down", 5], ["forward", 8], ["up", 3], ["down", 8], ["forward", 2]], 
            columns=["direction", "units"]
        )
    r = requests.get(
        url="https://adventofcode.com/2021/day/2/input",
        cookies={"session": f"{session_id}"}
    )
    with io.StringIO(r.text) as f:
        data = pd.read_table(f, delimiter=" ", names=["direction", "units"])
    return data


def part_one(input):
    grouped_sum = input.groupby("direction").sum()
    return int(grouped_sum.loc["forward"] * (grouped_sum.loc["down"] - grouped_sum.loc["up"]))


def part_two(input):
    input.loc[input["direction"] == "up", "units"] *= -1
    input["direction"].replace({"down": 0, "up": 0, "forward": 1}, inplace=True)
    delta_pos = input.direction * input.units
    delta_aim = input.units - delta_pos
    delta_depth = delta_pos * delta_aim.cumsum()
    return delta_pos.sum() * delta_depth.sum()


if __name__ == "__main__":
    session_id = sys.argv[1] if not _TEST else None
    input = load_input(session_id)
    ans_1 = part_one(input)
    ans_2 = part_two(input)
    print(ans_1, ans_2)
