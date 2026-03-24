def get_session_paths(log):
    sessions = {}
    for entry in log:
        sessions.setdefault(entry[1], []).append(entry[8])
    return sessions