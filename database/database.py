import json
file = open("database/database.json", "r", encoding="utf-8")
INFO = json.load(file)
file.close()

def get_info():
    return INFO

def fill_database():
    with open("database/database.json", "w", encoding="utf-8") as f:
        json.dump(get_info(), f)