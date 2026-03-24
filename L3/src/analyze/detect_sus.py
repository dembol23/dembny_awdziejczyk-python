from collections import Counter

def detect_sus(log, threshold):
    counts = dict(Counter(row[2] for row in log))
    sus = [ip for ip, count in counts if count >= threshold]
    return sus