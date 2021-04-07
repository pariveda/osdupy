import json


def print_json(obj):
    print(format_json(obj))


def format_json(obj):
    return json.dumps(obj, indent=2, sort_keys=True)


def batches(lst, n):
    """Yield successive n-sized batches from list."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
