import json
import random
import string
import hashlib
import datetime

def load_json_file(file_path):
    with open(file_path, mode="r") as f:
        data = json.load(f)

    return data

def save_json_file(data, file_path):
    with open(file_path, mode="w+") as f:
        json.dump(data, f)

def generate_random_string(l=512):
    return "".join(random.choices(string.ascii_letters, k=l))

def generate_hash(text):
    if isinstance(text, str): text = text.encode()
    return hashlib.sha512(text).hexdigest()

def get_now_timestamp():
    return datetime.datetime.now().timestamp()