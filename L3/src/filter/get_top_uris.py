from collections import Counter

def get_top_uris(log, n=10):
    return Counter(entry[8] for entry in log).most_common(n)
