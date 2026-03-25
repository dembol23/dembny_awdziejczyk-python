from collections import Counter

def get_top_ips(log, n=10):
    return Counter(entry[2] for entry in log).most_common(n)
