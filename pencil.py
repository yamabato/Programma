from util import load_json_file

P0_SUDOKU_INFO_PATH = "/home/programming/mysite/puzzles/p0_sudoku.html"
PUZZLE_PROBLEM_DATA_PATH = "/home/programming/mysite/data/puzzle_problem.json"

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

def get_problem_select(puzzle_id):
    puzzle_problem_data = load_json_file(PUZZLE_PROBLEM_DATA_PATH)

    if puzzle_id not in puzzle_problem_data: return False, ""

    problems = puzzle_problem_data[puzzle_id]
    options = ""

    for problem in problems:
        options += f"""<option value="{problem[0]}">{problem[1]}</option>"""

    return True, options