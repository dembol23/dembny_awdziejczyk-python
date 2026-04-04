def get_entries_by_code(log, code):
    if not isinstance(code, int) or code < 100 or code > 599:
        raise ValueError(f"Nieprawidłowy kod HTTP: {code}")
    return [entry for entry in log if entry[9] == code]
