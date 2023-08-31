P0_SUDOKU_INFO_PATH = "/home/programming/mysite/puzzles/p0_sudoku.html"

def get_puzzle_info(puzzle_id):
    info_path = ""

    if puzzle_id == "p0":
        info_path = P0_SUDOKU_INFO_PATH

    else:
        return False, ""

    info = ""
    with open(info_path, mode="r") as f:
        info = f.read()

    return True, info

