from util import load_json_file
import os

from program import get_python_program_output

P0_SUDOKU_INFO_PATH = "/home/programming/mysite/puzzles/p0_sudoku.html"
P1_DECIPHER_INFO_PATH = "/home/programming/mysite/puzzles/p1_decipher.html"
PUZZLE_PROBLEM_DATA_PATH = "/home/programming/mysite/data/puzzle_problem.json"
PUZZLE_PROBLEM_FOLDER = "/home/programming/mysite/puzzles/"

def get_puzzle_info(puzzle_id):
    info_path = ""

    if puzzle_id == "p0":
        info_path = P0_SUDOKU_INFO_PATH
    elif puzzle_id == "p1":
        info_path = P1_DECIPHER_INFO_PATH

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

def generate_board_html(game_id, prob_input, prob_output, stdout_text):
    board = ""

    if game_id == "p0":
        nums_answer = stdout_text.split()
        input_lines = prob_input.split("\n")
        nums_correct = prob_output.split()

        blank_n = 0

        board += """<table id="game-match-p0-table">"""

        for il in input_lines:
            input_nums = il.split()

            board += """<tr class="game-match-p0-row">"""
            for inp in input_nums:
                if inp == "*":
                    if blank_n < len(nums_answer):
                        answer = nums_answer[blank_n]
                        board += f"""<td class="game-match-p0-td answer {"correct" if len(nums_correct) > blank_n and nums_correct[blank_n]==answer else "incorrect"}">{answer}</td>"""
                        blank_n += 1
                    else:
                        answer = "-"
                        board += f"""<td class="game-match-p0-td answer blank">{answer}</td>"""

                else:
                    board += f"""<td class="game-match-p0-td">{inp}</td>"""

            board += "</tr>"

        board += "</table>"

    return board

def check_game_program(program, game_id, problem_id):
    problem_path = os.path.join(PUZZLE_PROBLEM_FOLDER, problem_id+".json")
    if not os.path.isfile(problem_path): return False, "", "", "", False

    problem_data = load_json_file(problem_path)
    prob_input, prob_output = problem_data["input"], problem_data["output"]

    stdout_text, stderr_text = get_python_program_output(program, prob_input)

    correct = prob_output == stdout_text
    board = generate_board_html(game_id, prob_input, prob_output, stdout_text)

    return True, stdout_text, stderr_text, board, correct

