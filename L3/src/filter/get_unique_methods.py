def get_unique_methods(log):
    return list(set(entry[6] for entry in log))