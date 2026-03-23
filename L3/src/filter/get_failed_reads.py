def get_failed_reads(log, merge=False):
    if merge:
        return [entry for entry in log if entry[9]//100 == 4 or entry[9]//100 == 5]
    else:
        return [entry for entry in log if entry[9]//100 == 4], [entry for entry in log if entry[9]//100 == 5]