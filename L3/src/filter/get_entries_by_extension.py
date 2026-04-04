def get_entries_by_extension(log, ext):
    return [entry for entry in log if entry[8].split("?")[0].endswith("." + ext)]