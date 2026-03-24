from collections import Counter

def analyze_log(log):
    ips = Counter(entry[2] for entry in log)
    uris = Counter(entry[8] for entry in log)
    methods = Counter(entry[6] for entry in log)
    statuses = Counter(entry[9] for entry in log)

    errors_4xx = sum(v for k, v in statuses.items() if k // 100 == 4)
    errors_5xx = sum(v for k, v in statuses.items() if k // 100 == 5)

    return {
        "top_ips": ips.most_common(10),
        "top_uris": uris.most_common(10),
        "method_distribution": dict(methods),
        "status_distribution": dict(statuses),
        "errors_4xx": errors_4xx,
        "errors_5xx": errors_5xx,
        "unique_ips": len(ips),
        "unique_uris": len(uris),
        "total_requests": len(log)
    }