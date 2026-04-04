from collections import Counter

def count_status_classes(log):
    valid = {2,3,4,5}
    return dict(Counter(f"{row[9]//100}xx" for row in log if row[9]//100 in valid))
