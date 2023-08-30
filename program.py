import subprocess
import datetime
import json
import os

from util import generate_random_string

RECORD_VARS = """
import json
_vars = dict()
_global_vars = list(globals().items())
for _n, _v in _global_vars:
    if _n in {0}:
        _vars[_n] = _v
with open("{1}", mode="w") as f:
    json.dump(_vars, f)
"""

def run_python_program(program, input_text="", record_vars=[]):
    now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f") + generate_random_string(2)
    program_file_name = os.path.join("/home/programming/mysite/programs/", now+".py")
    stdout_file_name = os.path.join("/home/programming/mysite/programs/", now+"_stdout.txt")
    stderr_file_name = os.path.join("/home/programming/mysite/programs/", now+"_stderr.txt")
    vars_file_name = os.path.join("/home/programming/mysite/programs/", now+"_vars.json")

    program_str = program
    if isinstance(program_str, bytes):
        program_str = program.decode()

    program_str += RECORD_VARS.format(list(record_vars), vars_file_name)
    with open(program_file_name, mode="w") as f:
        f.write(program_str)

    with open(vars_file_name, mode="w") as f:
        json.dump({}, f)

    subprocess.run(["python3", program_file_name],
            stdout=open(stdout_file_name, mode="w"),
            stderr=open(stderr_file_name, mode="w"),
            input=input_text, text=True,
            timeout=5,
    )

    stderr_text = ""
    with open(stderr_file_name, mode="r") as f:
        stderr_text = f.read()

    stderr_text = stderr_text.replace("/home/programma/mysite/programs/", "")

    with open(stderr_file_name, mode="w") as f:
        f.write(stderr_text)

    return program_file_name, stdout_file_name, stderr_file_name, vars_file_name

def get_python_program_output(program):
    _, stdout_file_name, stderr_file_name, _ = run_python_program(program)

    stdout_text = ""
    stderr_text = ""

    with open(stdout_file_name, mode="r") as f:
        stdout_text = "".join(f.readlines())

    with open(stderr_file_name, mode="r") as f:
        stderr_text = "".join(f.readlines())

    return stdout_text, stderr_text

def check_case(program, case):
    input_text = case["INPUT"]
    expected_output = case["OUTPUT"]
    record_vars = case["VARS"]

    _, stdout_file_name, stderr_file_name, vars_file_name = run_python_program(program, input_text, record_vars.keys())

    stderr_text = ""
    stdout_text = ""

    with open(stdout_file_name, mode="r") as f:
        stdout_text = "".join(f.readlines())

    with open(stderr_file_name, mode="r") as f:
        stderr_text = "".join(f.readlines())

    with open(vars_file_name, mode="r") as f:
        var_list = json.load(f)

    correct = True
    if stderr_text != "":
        correct = False
    elif stdout_text != expected_output:
        correct = False

    for name, value in var_list.items():
        if name not in var_list:
            correct = False
            break
        if var_list[name] != case["VARS"][name]:
            correct = False
            break

    return correct, input_text, stdout_text, stderr_text

def check_python_program(program, cases):
    correct = True

    input_text = ""
    stdout_text = ""
    stderr_text = ""

    for case in cases:
        c, it, ot, et = check_case(program, case)

        correct &= c
        input_text += it
        stdout_text += ot
        stderr_text += et

    return correct, input_text, stdout_text, stderr_text


