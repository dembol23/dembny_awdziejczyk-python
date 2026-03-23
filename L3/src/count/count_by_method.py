from collections import Counter

def count_by_method(log):
    return dict(Counter(row[6] for row in log))
