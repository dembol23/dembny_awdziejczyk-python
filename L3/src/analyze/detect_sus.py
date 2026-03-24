from collections import Counter

def detect_sus(log, threshold):
    counts = Counter(row[2] for row in log)
    return [ip for ip, count in counts.items() if count >= threshold]