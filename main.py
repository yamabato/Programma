from flask import Flask, render_template, request, redirect, url_for
import json

from lecture import generate_lecture_html, generate_task_cases_data, get_lectures_data
from program import check_python_program, get_python_program_output
from match import make_new_room, enter_room, get_participant_list, start_match, is_started, return_match_next_problem, check_match_program, is_finished
from user import signup, signin, check_auto_signin, record_cleared_task

app = Flask(__name__)

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
        return render_template("index.html", title="Programma", username=username)
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

    ok = start_match(match_id, match_key)
    return {"ok": ok}

@app.route("/started", methods=["GET"])
def match_started():
    match_id = request.args.get("id", "")
    match_key = request.args.get("key", "")
    ok, started, start = is_started(match_id, match_key)
    return {"ok": ok, "started": started, "start": start}

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

@app.route("/next_problem")
def match_next_problem():
    ok, username = get_username()
    if not ok: return {"ok": False, "problem_html": ""}

    match_id = request.args.get("id", "")
    match_key = request.args.get("key", "")

    ok, problem_html = return_match_next_problem(match_id, match_key, username)
    return {"ok": ok, "problem_html": problem_html}

@app.route("/finished", methods=["GET"])
def match_finished():
    ok, username = get_username()
    if not ok: return {"ok": False, "finished": False}

    match_id = request.args.get("id", "")
    match_key = request.args.get("key", "")

    ok, finished = is_finished(match_id, match_key, username)

    return {"ok": ok, "finished": finished}

@app.route("/result", methods=["POST", "GET"])
def result_page():
    if request.method == "POST":
        pass
    else:
        ok, username = get_username()
        if ok:
            return render_template("match_result.html", header_type="match", title="対戦結果", username=username)
        else:
            return redirect(url_for("signin_page"))

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

@app.route("/game", methods=["POST", "GET"])
def game_page():
    if request.method == "POST":
        pass
    else:
        ok, username = get_username()
        if ok:
            gameID = request.args.get("id", "b0")
            return render_template("game.html", header_type="game", title="対戦ゲーム", username=username)
        else:
            return redirect(url_for("signin_page"))


@app.route("/game_match", methods=["POST", "GET"])
def game_match_page():
    if request.method == "POST":
        room_setting = request.data
        if isinstance(room_setting, bytes): room_setting = room_setting.decode()
        room_setting_json = json.loads(room_setting)
        create_new_room(room_setting_json)

    else:
        ok, username = get_username()
        if ok:
            gameID = request.args.get("id", "b0")
            return render_template("game_match.html", header_type="game", title="対戦", username=username)
        else:
            return redirect(url_for("signin_page"))

