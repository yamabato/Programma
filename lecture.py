import os

from util import load_json_file

LECTURES_FOLDER = "/home/programming/mysite/lectures/"
LECTURE_DATA_PATH = "/home/programming/mysite/data/lectures.json"
USERS_DATA_PATH = "/home/programming/mysite/data/users.json"

def normalize_text(line_text):
    return line_text

def generate_paragraph(text):
    return f"<div class='lecture-description lecture-paragraph'>&emsp;{text}</div>"

def generate_plain_text(line_text):
    line_text_normalized = normalize_text(line_text)
    return line_text_normalized

def generate_code(line_text):
    line_text_normalized = normalize_text(line_text)
    return f"<span class='lecture-description lecture-code'>{line_text_normalized}</span>"

def generate_new_line(line_text):
    return "<div class='lecture-description lecture-new-line'><br></div>"

def load_lecture_file(lecture_id):
    lecture_file_lines = []

    lecture_file_path = os.path.join(LECTURES_FOLDER, lecture_id+".lec")

    with open(lecture_file_path, mode="r") as f:
        lecture_file_lines = f.readlines()

    return lecture_file_lines

line_type_dict = {
    "PRG:": 0,
    "PLN:": 1,
    "COD:": 2,
    "NLN:": 3,
    "EPR:": 4,
}

def get_line_content(line):
    line_type = line[:4]
    line_text = line[4:]

    line_type_id = -1

    if line_type in line_type_dict:
        line_type_id = line_type_dict[line_type]
    line_text = line_text.strip()

    return (line_type_id, line_text)

def analyze_lecture_file(lecture_id):
    lecture_file_lines  = load_lecture_file(lecture_id)

    title = ""
    description_lines = []
    code_lines = []
    task_lines = []

    # 0: none, 1: lecture, 2: code, 3: task
    mode = 0

    for line in lecture_file_lines:
        if line[:6] == "TITLE:":
            title = line[6:].strip()
            mode = 0
        elif line[:8] == "LECTURE:":
            mode = 1
            continue
        elif line[:5] == "CODE:":
            mode = 2
            continue
        elif line[:5] == "TASK:":
            mode = 3
            continue

        if mode == 0: continue

        elif mode == 1:
            line_content = get_line_content(line)
            if line_content[0] != -1:
                description_lines.append(line_content)

        elif mode == 2:
            code_lines.append(line)

        elif mode == 3:
            task_lines.append(line)

    return title, description_lines, code_lines, task_lines

def generate_html_document(description_lines):
    html_document = "<div class='lecture-description-text'>"

    text = ""
    for line_content in description_lines:
        line_type, line_text = line_content

        if line_type == 0:
            pass
        elif line_type == 1:
            text += generate_plain_text(line_text)
        elif line_type == 2:
            text += generate_code(line_text)
        elif line_type == 3:
            html_document += "<br>"
        elif line_type == 4:
            html_document += generate_paragraph(text)
            text = ""

    html_document += "</div>"

    return html_document

def generate_initial_code(code_lines):
    return "".join(code_lines)

def generate_task_html(task_lines):
    statement_lines = []
    task_statement_html = ""

    mode = -1 #0: stmt

    for line in task_lines:
        if line[:5] == "STMT:":
            mode = 0
            continue
        if line[:5] == "ESTMT:":
            mode = -1
            continue

        if mode == 0:
            line_content = get_line_content(line)
            if line_content[0] != -1:
                statement_lines.append(line_content)

    task_statement_html = generate_html_document(statement_lines)

    return task_statement_html

special_characters = {
    "::[SPACE];": " ",
    "::[NEWLINE];": "\n",

}
def generate_std_text(text):
    text = text.strip()
    for sign, char in special_characters.items():
        text = text.replace(sign, char)

    return text

def generate_task_cases_data(lecture_id):
    _, _, _, task_lines = analyze_lecture_file(lecture_id)
    cases = []
    case = {}

    #0: case
    mode = -1

    for line in task_lines:
        if line[:5] == "CASE:":
            mode = 0
            case = {"OUTPUT": "", "INPUT": "", "VARS": {}}
            continue
        elif line[:6] == "ECASE:":
            mode = -1
            cases.append(case)
            continue

        if mode == -1: continue

        if line[:7] == "OUTPUT:":
            case["OUTPUT"] = generate_std_text(line[7:])
        elif line[:6] == "INPUT:":
            case["INPUT"] = generate_std_text(line[6:])
        elif line[:4] == "VAR:":
            var_name, var_value_text = line[4:].split(maxsplit=1)
            var_name = var_name.strip()
            var_value = eval(var_value_text.strip())
            case["VARS"][var_name] = var_value

    return cases

def generate_lecture_html(lecture_id):
    title, description_lines, code_lines, task_lines = analyze_lecture_file(lecture_id)

    lecture_html = generate_html_document(description_lines)
    initial_code = generate_initial_code(code_lines)
    task_statement = generate_task_html(task_lines)

    return title, lecture_html, initial_code, task_statement

def get_lectures_data(username):
    lectures_data = load_json_file(LECTURE_DATA_PATH)

    users = load_json_file(USERS_DATA_PATH)

    if username not in users.keys(): return {"ok": False}


    for chapter in lectures_data.values():
        sections = chapter["sections"]
        for section in sections.values():
            lecture_id = section["lecture_id"]
            section["cleared"] = False
            if lecture_id in users[username]["cleared"]:
                section["cleared"] = True


    lectures_data["ok"] = True

    return lectures_data
