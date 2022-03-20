import sys
import requests

_TEST = False


def load_input(session_id=None):
    if _TEST:
        data = """
            0,9 -> 5,9
            8,0 -> 0,8
            9,4 -> 3,4
            2,2 -> 2,1
            7,0 -> 7,4
            6,4 -> 2,0
            0,9 -> 2,9
            3,4 -> 1,4
            0,0 -> 8,8
            5,5 -> 8,2
        """.strip().replace(" ", "")
    else:
        r = requests.get(
            url="https://adventofcode.com/2021/day/5/input",
            cookies={"session": f"{session_id}"}
        )
        data = r.text
    return data

if __name__ == "__main__":
    session_id = sys.argv[1] if not _TEST else None
    data = load_input(session_id)
    print(data)
