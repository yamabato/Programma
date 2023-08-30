import os
import math
import random
from collections import defaultdict

from util import generate_random_string, load_json_file, save_json_file, generate_hash, get_now_timestamp
from program import check_python_program
from user import get_displayed_data

MATCH_ROOMS_DATA_FOLDER = "/home/programming/mysite/matchs"
MATCH_KEYS_PATH = "/home/programming/mysite/data/match_id_table.json"
PROBLEMS_DATA_PATH = "/home/programming/mysite/data/problems.json"
PROBLEMS_FOLDER = "/home/programming/mysite/problems"
MATCH_ID_LENGTH = 5

def make_match_data_path(match_id):
    match_data_path = os.path.join(MATCH_ROOMS_DATA_FOLDER, match_id+".json")
    return match_data_path

def check_match_key(match_id, match_key):
    match_keys_data = load_json_file(MATCH_KEYS_PATH)

    if match_key not in match_keys_data: return False
    if match_keys_data[match_key] != match_id: return False

    return True

def create_match_key(match_id):
    match_keys_data = load_json_file(MATCH_KEYS_PATH)

    match_key = generate_random_string()
    while match_key in match_keys_data:
        match_key = generate_random_string()

    match_keys_data[match_key] = match_id
    save_json_file(match_keys_data, MATCH_KEYS_PATH)

    return match_key

def append_participant(username, nickname, team, match_id):
    match_data_path = make_match_data_path(match_id)
    match_data = load_json_file(match_data_path)

    match_data["username"][username] = nickname
    match_data["participants"][username] = (nickname, team)
    match_data["solved"][username] = ()

    save_json_file(match_data, match_data_path)

def create_match_data_file(username, match_id, room_setting):
    match_data = {
        "room_setting": room_setting,
        "participants": {},
        "problems": [],
        "username": {},
        "status": 0,
        "seed": get_now_timestamp(),
        "start": -1,
        "solved": {},
        "displayed": defaultdict(int),
        "problem_number": {},
        "surrender": {},
        "ending_time": -1,
        "clear_time": {},
    }

    match_data_path = make_match_data_path(match_id)
    save_json_file(match_data, match_data_path)

def match_id_exists(match_id):
    match_data_path = make_match_data_path(match_id)
    return os.path.isfile(match_data_path)

def get_match_data(match_id):
    match_data_path = make_match_data_path(match_id)
    return load_json_file(match_data_path)

def save_match_data(match_data, match_id):
    match_data_path = make_match_data_path(match_id)
    save_json_file(match_data, match_data_path)

def make_new_room(username, room_setting):
    room_setting["room_password"] = generate_hash(room_setting["room_password"])

    match_id = generate_random_string(MATCH_ID_LENGTH)
    while match_id_exists(match_id):
        match_id = generate_random_string(MATCH_ID_LENGTH)

    organizer_nickname = room_setting["organizer_nickname"]

    create_match_data_file(username, match_id, room_setting)
    append_participant(username, organizer_nickname, organizer_nickname, match_id)
    match_key = create_match_key(match_id)

    return True, match_id, match_key, ""

def enter_room(enter_info):
    match_id = enter_info["match_id"]
    password = enter_info["password"]
    username = enter_info["username"]
    nickname = enter_info["nickname"]

    if not match_id_exists(match_id):
        return False, {}, "", "部屋が存在しません。"

    match_data = get_match_data(match_id)

    if generate_hash(password) != match_data["room_setting"]["room_password"]:
        return False, {}, "", "部屋コード、あるいはパスワードが間違っています。"

    if username in match_data["username"]:
        return False, {}, "", "既に入室しています。"

    append_participant(username, nickname, nickname, match_id)
    match_key = create_match_key(match_id)

    return True, match_data["room_setting"], match_key, ""

def get_participant_list(match_id, match_key):
    if not check_match_key(match_id, match_key): return False, {}
    match_data = get_match_data(match_id)

    participants = match_data["participants"]

    participantList = defaultdict(list)

    for user in participants.keys():
        nickname, team = participants[user]
        participantList[team].append(nickname)

    return True, participantList

def get_problem_list(level):
    problems_data = load_json_file(PROBLEMS_DATA_PATH)
    problems = []
    for lv in level:
        problems += problems_data[f"level-{lv}"]

    return problems

def init_match_problems(match_id):
    match_data = get_match_data(match_id)
    displayed = match_data["displayed"]

    room_setting = match_data["room_setting"]
    match_type = room_setting["type"]
    match_problem_count = int(room_setting["count"])
    match_level = room_setting["level"]

    problems = get_problem_list(match_level)
    random.shuffle(problems)
    problems.sort(key=lambda x: displayed[x])

    if match_type == "count":
        problems = problems[:match_problem_count]

    match_data["problems"] = problems
    save_match_data(match_data, match_id)

def start_match(match_id, match_key):
    if not check_match_key(match_id, match_key): return False

    match_data = get_match_data(match_id)

    match_data["status"] = 1
    match_data["start"] = get_now_timestamp() + 10

    room_setting = match_data["room_setting"]

    match_type = room_setting["type"]
    if match_type == "time":
        match_data["ending_time"] = get_now_timestamp() + room_setting["hour"] * 60*60 + room_setting["minute"] * 60

    displayed_data = get_displayed_data()
    displayed = defaultdict(int)

    participants = match_data["participants"].keys()
    match_level = room_setting["level"]
    problems = get_problem_list(match_level)
    for username in participants:
        for problem in problems:
            displayed[problem] = displayed_data[username].count(problem)

    match_data["displayed"] = displayed

    match_data["solved"] = {name: [] for name in participants}
    match_data["problem_number"] = {name: -1 for name in participants}
    match_data["surrender"] = {name: False for name in participants}
    match_data["clear_time"] = {name: math.inf for name in participants}

    save_match_data(match_data, match_id)

    init_match_problems(match_id)

    return True

def is_started(match_id, match_key):
    if not check_match_key(match_id, match_key): return False, False, -1

    match_data = get_match_data(match_id)

    start = match_data["start"]
    status = match_data["status"]
    if status == 1:
        return True, True, start
    return True, False, -1

def get_problem_html(problem_id):
    problem_html_path = os.path.join(PROBLEMS_FOLDER, problem_id+".html")

    problem_html = ""
    with open(problem_html_path, mode="r") as f:
        problem_html = f.read()

    return problem_html

def return_match_next_problem(match_id, match_key, username):
    if not check_match_key(match_id, match_key): return False, ""

    match_data = get_match_data(match_id)
    problems = match_data["problems"]

    problem_number = 0

    user_solved = match_data["solved"][username]
    if -1 not in user_solved:
        problem_number = len(user_solved)
    else:
        problem_number = user_solved.index(-1)

    problem_id = problems[problem_number % len(problems)]

    problem_html = get_problem_html(problem_id)

    match_data["problem_number"][username] = problem_number

    save_match_data(match_data, match_id)

    return True, problem_html

def generate_match_cases(match_id, username):
    match_data = get_match_data(match_id)
    problem_number = match_data["problem_number"][username]
    problems = match_data["problems"]

    problem_id = match_data["problems"][problem_number % len(problems)]

    cases_data = load_json_file(os.path.join(PROBLEMS_FOLDER, problem_id+".json"))

    cases = [{"INPUT": case[0], "OUTPUT": case[1], "VARS": {}} for case in cases_data]

    return cases

def check_match_program(match_id, username, program):
    cases = generate_match_cases(match_id, username)
    correct, input_text, stdout_text, stderr_text = check_python_program(program, cases)

    if correct:
        match_data = get_match_data(match_id)
        problem_number = match_data["problem_number"][username]
        solved = match_data["solved"][username]

        if len(solved) <= problem_number:
            solved += [-1] * (problem_number - len(solved) + 1)
        solved[problem_number] = get_now_timestamp()
        match_data["problem_number"][username] += 1

        room_setting = match_data["room_setting"]
        if room_setting["type"] == "count":
            match_problem_count = int(room_setting["count"])
            if len(solved) - solved.count(-1) >= match_problem_count:
                match_data["clear_time"][username] = get_now_timestamp() - match_data["start"]

        save_match_data(match_data, match_id)

    return correct, stdout_text, stderr_text

def is_finished(match_id, match_key, username):
    if not check_match_key(match_id, match_key): return False, False

    match_data = get_match_data(match_id)
    room_setting = match_data["room_setting"]
    match_type = room_setting["type"]

    finished = False

    if match_type == "time":
        ending_time = match_data["ending_time"]
        now_timestamp = get_now_timestamp()
        if now_timestamp >= ending_time:
            finished = True

    elif match_type == "count":
        solved = match_data["solved"][username]
        match_problem_count = int(room_setting["count"])

        if len(solved) - solved.count(-1) >= match_problem_count:
            finished = True
    else:
        surrendered = list(match_data["surrender"].values())
        if match_data["surrender"][username]:
            finished = True
        if surrendered.count(True) >= len(surrendered)-1:
            finished = True

    return True, finished

def rank_numbering(ranked_list, data):
    last = ""
    rank = 1
    rank_numbered_list = []
    for n, user in enumerate(ranked_list):
        if last in data and data[user] != data[last]:
            rank = n + 1
        rank_numbered_list.append((user, rank))

    return rank_numbered_list

def get_ranking(match_id):
    match_data = get_match_data(match_id)
    room_setting = match_data["room_setting"]
    match_type = room_setting["type"]

    participants = match_data["participants"].keys()
    problem_number_data = match_data["problem_number"]
    clear_time_data = match_data["clear_time"]


    if match_type == "time":
        ranking = sorted(participants , key=lambda x: problem_number_data[x], reverse=True)
        sort_data = {user: str(problem_number_data[user]) for user in participants}
    elif match_type == "count":
        solved_problems_ranking = sorted(participants, key=lambda x: problem_number_data[x], reverse=True)
        ranking = sorted(solved_problems_ranking, key=lambda x: clear_time_data[x])
        sort_data = {user: str(clear_time_data[user])+str(problem_number_data[user]) for user in participants}
    else:
        clear_time_ranking = sorted(participants, key=lambda x: clear_time_data[x])
        ranking = sorted(clear_time_ranking, key=lambda x: problem_number_data[x])
        sort_data = {user: str(clear_time_data[user])+str(problem_number_data[user]) for user in participants}

    rank_numbered_list = rank_numbering(ranking, sort_data)

    return rank_numbered_list

def format_timestamp(timestamp):
    hour = 0
    minute = 0
    second = 0

    hour = int(timestamp // (60*60))
    minute = int(timestamp // (60*60) % 60)
    second = int(timestamp % 60 // 1)

    return f"{hour:02}:{minute:02}:{second:02}"

def generate_ranking_html(match_id, match_key, username):
    if not check_match_key(match_id, match_key): return False, "", "", -1

    html = ""

    ranking = get_ranking(match_id)

    match_data = get_match_data(match_id)
    problem_number_data = match_data["problem_number"]
    clear_time_data = match_data["clear_time"]
    surrender_data = match_data["surrender"]
    participants = match_data["participants"]

    user_nickname = ""
    user_rank = ""

    rank_class = ""
    for user, rank in ranking:
        if rank <= 3:
            rank_class = f"rank{rank}"
        nickname = participants[user][0]
        solved_count = problem_number_data[user] + 1
        clear_time = format_timestamp(clear_time_data[user])

        html += """<tr class="match-ranking-table-row">"""
        html += f"""<td class="match-ranking-table-td {rank_class}">#{rank}</td>"""
        html += f"""<td class="match-ranking-table-td {rank_class}">{nickname}</td>"""
        html += f"""<td class="match-ranking-table-td {rank_class}">{solved_count}</td>"""
        html += f"""<td class="match-ranking-table-td {rank_class}">{clear_time}</td>"""
        html += "</tr>"

        if user == username:
            user_nickname = nickname
            user_rank = rank

    return True, html, user_nickname, user_rank






