from util import load_json_file, save_json_file

CONTACT_DATA_PATH = "/home/programming/mysite/data/contact_data.json"
def record_contact(username, contact_content, contact_type):
    contact_data = load_json_file(CONTACT_DATA_PATH)

    if contact_type in contact_data:
        contact_data[contact_type].append({"user": username, "content": contact_content})
    else:
        contact_data["other"].append({"user": username, "content": contact_content})

    save_json_file(contact_data, CONTACT_DATA_PATH)
