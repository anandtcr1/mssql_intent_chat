import json

def load_schema(path="schema.json") -> dict:
    with open(path, "r") as f:
        return json.load(f)
