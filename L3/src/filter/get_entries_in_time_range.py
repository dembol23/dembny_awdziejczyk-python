def get_entries_in_time_range(log, start, end):
    return [entry for entry in log if start <= entry[0] < end]