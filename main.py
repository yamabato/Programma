from flask import Flask, render_template, request, redirect, url_for
import json

from app_info import get_release_log, get_feature_plan
from lecture import generate_lecture_html, generate_task_cases_data, get_lectures_data
from program import check_python_program, get_python_program_output
from contact import record_contact, get_faq_list
from pencil import get_puzzle_info, get_problem_select, check_game_program
from match import make_new_room, enter_room, get_participant_list, start_match, is_started, return_match_next_problem, check_match_program, is_finished, surrender, generate_ranking_html, get_room_info, get_problem_html, get_number_of_problems
from user import signup, signin, check_auto_signin, record_cleared_task

app = Flask(__name__)

import time
@app.route("/test", methods=["GET"])
def test():
    time.sleep(5)
    return {"test": "datadata"}

def get_username():
    signin_id = request.cookies.get("signin_id", "")

    ok, username = check_auto_signin(signin_id)

    return ok, username

def get_posted_data():
    posted_data = request.data
    if isinstance(posted_data, bytes):
        posted_data = posted_data.decode()
    posted_data_json = json.loads(posted_data)
    return posted_data_json

@app.route("/")
def index_page():
    ok, username = get_username()

    if ok:
        faq_html = get_faq_list()
        release_log_html = get_release_log()
        feature_plan_html = get_feature_plan()
        return render_template("index.html", title="Programma", username=username,
                                faq_html=faq_html, release_log_html=release_log_html, feature_plan_html=feature_plan_html)
    else:
        return redirect(url_for("signin_page"))

@app.route("/lectures_data", methods=["POST"])
def return_lectures_data():
    ok, username = get_username()
    if request.method == "POST":
        if ok:
            lectures_data = get_lectures_data(username)
            return lectures_data
        else:
            return {"ok": False}

@app.route("/contact", methods=["POST"])
def receive_contact_content():
    if request.method == "POST":
        ok, username = get_username()
        if ok:
            posted_data_json = get_posted_data()
            contact_content = posted_data_json["content"]
            contact_type = posted_data_json["type"]

            ok = record_contact(username, contact_content, contact_type)

            return {"ok": ok}

@app.route("/registered")
def registered_page():
    return render_template("registered.html")

@app.route("/signin", methods=["POST", "GET"])
def signin_page():
    if request.method== "POST":
        posted_data_json = get_posted_data()
        username = posted_data_json["username"]
        password = posted_data_json["password"]

        ok, signin_id, msg = signin(username, password)
        if ok:
            return {"ok": True, "username": username, "signin_id": signin_id}
        else:
            return {"ok": False, "msg": msg}
    else:
        return render_template("signin.html")

@app.route("/signup", methods=["POST", "GET"])
def signup_page():
    if request.method== "POST":
        posted_data_json = get_posted_data()
        username = posted_data_json["username"]
        password = posted_data_json["password"]

        ok, signin_id, msg = signup(username, password)
        if ok:
            return {"ok": True, "username": username, "signin_id": signin_id}
        else:
            return {"ok": False, "msg": msg}
    else:
        return render_template("signup.html")

@app.route("/lecture", methods=["POST", "GET"])
def lecture_page():

    if request.method == "POST":
        posted_data_json = get_posted_data()

        program = posted_data_json["program"]

        if posted_data_json["type"] == "check":
            lecture_id = request.args.get("lid", "P0101")
            task_cases = generate_task_cases_data(lecture_id)
            correct, input_text, stdout_text, stderr_text = check_python_program(program, task_cases)

            if correct:
                ok, username = get_username()
                record_cleared_task(username, lecture_id)

            return {"correct": correct, "stdout": stdout_text, "stderr": stderr_text}
        elif posted_data_json["type"] == "run":
            stdout_text, stderr_text = get_python_program_output(program)
            return {"stdout": stdout_text, "stderr": stderr_text}
    else:
        ok, username = get_username()
        if ok:
            lecture_id = request.args.get("lid", "P0101")
            title, lecture_html, initial_code, task_statement = generate_lecture_html(lecture_id)
            return render_template("lecture.html", title=title, username=username, lecture_html=lecture_html, initial_code=initial_code, task_html=task_statement)
        else:
            return redirect(url_for("signin_page"))

@app.route("/new", methods=["POST", "GET"])
def new_room_page():
    ok, username = get_username()
    if not ok: return redirect(url_for("signin_page"))

    if request.method == "POST":
        posted_data_json = get_posted_data()
        ok, match_id, match_key, errmsg = make_new_room(username, posted_data_json)
        return {"ok": ok, "match_id": match_id, "match_key": match_key, "errmsg": errmsg}
    else:
        return render_template("new_room.html", header_type="match", title="部屋作成", username=username)

@app.route("/no_of_prob", methods=["POST"])
def return_number_of_problems():
    posted_data_json = get_posted_data()
    level = posted_data_json["level"]

    number = get_number_of_problems(level)

    return {"number": number}

@app.route("/enter", methods=["POST", "GET"])
def enter_page():
    if request.method == "POST":
        posted_data_json = get_posted_data()
        ok, match_setting, match_key, errmsg = enter_room(posted_data_json)
        return {"ok": ok, "match_key": match_key, "match_setting": match_setting, "errmsg": errmsg}
    else:
        ok, username = get_username()
        if ok:
            return render_template("enter_room.html", header_type="match", title="入室", username=username)
        else:
            return redirect(url_for("signin_page"))

@app.route("/wait", methods=["POST", "GET"])
def match_wait_page():
    if request.method == "POST":
        pass
    else:
        ok, username = get_username()
        if ok:
            return render_template("match_wait.html", header_type="match", title="対戦待ち", username=username)
        else:
            return redirect(url_for("signin_page"))

@app.route("/participants", methods=["GET"])
def return_participant_list():
    match_id = request.args.get("id", "")
    match_key = request.args.get("key", "")
    ok, participant_list = get_participant_list(match_id, match_key)

    return {"ok": ok, "participant_list": participant_list}

@app.route("/start", methods=["GET"])
def match_start_request():
    match_id = request.args.get("id", "")
    match_key = request.args.get("key", "")

    ok, ending_time = start_match(match_id, match_key)
    return {"ok": ok, "ending_time": ending_time}

@app.route("/started", methods=["GET"])
def match_started():
    match_id = request.args.get("id", "")
    match_key = request.args.get("key", "")
    ok, started, start, ending_time = is_started(match_id, match_key)
    return {"ok": ok, "started": started, "start": start, "ending_time": ending_time}

@app.route("/count_down", methods=["GET"])
def count_down_page():
    start = request.args.get("start", "")
    return render_template("count_down.html", start=start)

@app.route("/match", methods=["POST", "GET"])
def match_page():
    if request.method == "POST":
        posted_data_json = get_posted_data()

        program = posted_data_json["program"]

        if posted_data_json["type"] == "run":
            stdout_text, stderr_text = get_python_program_output(program)
            return {"stdout": stdout_text, "stderr": stderr_text}
        else:
            ok, username = get_username()
            match_id = request.args.get("id", "")
            #match_key = request.args.get("key", "")

            correct, stdout_text, stderr_text = check_match_program(match_id, username, program)

            return {"correct": correct, "stdout": stdout_text, "stderr": stderr_text}
    else:
        ok, username = get_username()
        if ok:
            return render_template("match.html", header_type="match", title="対戦", username=username)
        else:
            return redirect(url_for("signin_page"))

@app.route("/rule_info", methods=["GET"])
def return_rule_info():
    match_id = request.args.get("id", "")
    match_key = request.args.get("key", "")

    return get_room_info(match_id, match_key)

@app.route("/next_problem")
def match_next_problem():
    ok, username = get_username()
    if not ok: return {"ok": False, "problem_html": ""}

    match_id = request.args.get("id", "")
    match_key = request.args.get("key", "")

    ok, problem_html, rest = return_match_next_problem(match_id, match_key, username)
    return {"ok": ok, "problem_html": problem_html, "rest": rest}

@app.route("/problem_test")
def problem_test_page():
    prob_id = request.args.get("id", "")

    prob_html = get_problem_html(prob_id)

    return render_template("problem_test.html", prob_html=prob_html)


@app.route("/finished", methods=["GET"])
def match_finished():
    ok, username = get_username()
    if not ok: return {"ok": False, "finished": False}

    match_id = request.args.get("id", "")
    match_key = request.args.get("key", "")

    ok, finished = is_finished(match_id, match_key, username)

    return {"ok": ok, "finished": finished}

@app.route("/ranking", methods=["GET"])
def return_match_ranking():
    match_id = request.args.get("id", "")
    match_key = request.args.get("key", "")

    ok, match_ranking, _, _ = generate_ranking_html(match_id, match_key, "", True)

    return {"ok": ok, "match_ranking": match_ranking}

@app.route("/surrender", methods=["GET"])
def receive_surrender():
    ok, username = get_username()
    if ok:
        match_id = request.args.get("id", "")
        match_key = request.args.get("key", "")
        ok = surrender(match_id, match_key, username)

        return {"ok": ok}
    else:
        return redirect(url_for("signin_page"))


@app.route("/result", methods=["POST", "GET"])
def result_page():
    if request.method == "POST":
        pass
    else:
        ok, username = get_username()
        if ok:
            match_id = request.args.get("id", "")
            match_key = request.args.get("key", "")
            ok, ranking_html, room_name, nickname, rank = generate_ranking_html(match_id, match_key, username)
            if ok:
                return render_template("match_result.html", header_type="match", title="対戦結果",
                        username=username, room_name=room_name, ranking_html=ranking_html, nickname=nickname, rank=rank)

            return redirect(url_for("enter_page"))
        else:
            return redirect(url_for("signin_page"))

"""
@app.route("/table", methods=["POST", "GET"])
def table_game_page():
    if request.method == "POST":
        pass
    else:
        ok, username = get_username()
        if ok:
            return render_template("table_game.html", header_type="game", title="対戦ゲーム", username=username)
        else:
            return redirect(url_for("signin_page"))
"""

@app.route("/pencil", methods=["POST", "GET"])
def pencil_game_page():
    if request.method == "POST":
        pass
    else:
        ok, username = get_username()
        if ok:
            return render_template("pencil_game.html", header_type="game", title="ペンシルパズル", username=username)
        else:
            return redirect(url_for("signin_page"))

@app.route("/puzzle", methods=["POST", "GET"])
def puzzle_page():
    if request.method == "POST":
        pass
    else:
        ok, username = get_username()
        if ok:
            game_id = request.args.get("id", "p0")
            ok, puzzle_info = get_puzzle_info(game_id)
            ok, problem_select = get_problem_select(game_id)
            return render_template("game.html", header_type="game", title="ペンシルパズル", username=username,
                                    game_info=puzzle_info, problem_select=problem_select)
        else:
            return redirect(url_for("signin_page"))

@app.route("/game", methods=["POST"])
def run_game_program():
     if request.method == "POST":
        posted_data_json = get_posted_data()

        program = posted_data_json["program"]

        if posted_data_json["type"] == "run":
            stdout_text, stderr_text = get_python_program_output(program)
            return {"stdout": stdout_text, "stderr": stderr_text}

@app.route("/game_match", methods=["POST", "GET"])
def game_match_page():
    if request.method == "POST":
        posted_data_json = get_posted_data()

        program = posted_data_json["program"]
        game_id = posted_data_json["game_id"]
        problem_id = posted_data_json["problem_id"]

        if posted_data_json["type"] == "submit":
            ok, stdout_text, stderr_text, board, correct = check_game_program(program, game_id, problem_id)
            return {"ok": ok, "stdout": stdout_text, "stderr": stderr_text, "board": board, "correct": correct}

    else:
        ok, username = get_username()
        if ok:
            game_id = request.args.get("id", "p0")
            ok, problem_select = get_problem_select(game_id)
            return render_template("game_match.html", header_type="game", title="パズル", username=username, problem_select=problem_select)
        else:
            return redirect(url_for("signin_page"))

