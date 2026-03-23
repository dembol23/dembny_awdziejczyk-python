import datetime

def get_entries_by_code(log, code):
    return [entry for entry in log if entry[9] == code]
