import json

def load_config(file_path="data/config.json"):
    f = open(file_path, encoding="utf-8")
    config = json.load(f)
    f.close()
    return config