from util import load_json_file, save_json_file, generate_random_string, generate_hash, get_now_timestamp

USERS_DATA_PATH = "/home/programming/mysite/data/users.json"
DISPLAYED_DATA_PATH = "/home/programming/mysite/data/displayed.json"
SIGNED_IN_USERS_DATA_PATH = "/home/programming/mysite/data/signed_in_users.json"

def signup(username, password):
    password_hashed = generate_hash(password)
    password = password.strip()

    users = load_json_file(USERS_DATA_PATH)

    if username in users: return False, "", "そのユーザー名は既に使われています"
    if username== "": return False, "", "ユーザー名が空です"
    if password == "": return False, "", "パスワードが空です"

    users[username] = {"password": password_hashed, "cleared": []}

    save_json_file(users, USERS_DATA_PATH)

    displayed_data = get_displayed_data()
    displayed_data[username] = []
    save_json_file(displayed_data, DISPLAYED_DATA_PATH)

    return *authoricate(username, password), ""

def signin(username, password):
    ok, signin_id = authoricate(username, password)
    if not ok: return False, "", "ユーザー名あるいはパスワードに誤りがあります"
    return True, signin_id, ""

def authoricate(username, password):
    users = load_json_file(USERS_DATA_PATH)

    if username not in users: return False, ""

    if users[username]["password"] != generate_hash(password):
        return False, ""

    signed_in_users = load_json_file(SIGNED_IN_USERS_DATA_PATH)

    signin_id = generate_random_string()
    now = get_now_timestamp()
    age = 60 * 60 * 24 * 7 # 7 days
    expiration = now + age
    signed_in_users[signin_id] = {"username": username, "expiration": expiration}

    save_json_file(signed_in_users, SIGNED_IN_USERS_DATA_PATH)

    return True, signin_id

def check_auto_signin(signin_id):
    signed_in_users = load_json_file(SIGNED_IN_USERS_DATA_PATH)

    if signin_id not in signed_in_users.keys(): return False, ""

    signin_data = signed_in_users[signin_id]
    now = get_now_timestamp()

    if signin_data["expiration"] < now:
        return False, ""

    return True, signin_data["username"]

def record_cleared_task(username, lecture_id):
    users = load_json_file(USERS_DATA_PATH)

    if username not in users: return False

    users[username]["cleared"].append(lecture_id)

    save_json_file(users, USERS_DATA_PATH)

def append_displayed_problem(username, problem):
    displayed_data = load_json_file(DISPLAYED_DATA_PATH)
    displayed_data[username].append(problem)
    save_json_file(displayed_data, DISPLAYED_DATA_PATH)

def get_displayed_problems(username):
    displayed_data = get_displayed_data()
    return displayed_data[username]

def get_displayed_data():
    displayed_data = load_json_file(DISPLAYED_DATA_PATH)
    return displayed_data









