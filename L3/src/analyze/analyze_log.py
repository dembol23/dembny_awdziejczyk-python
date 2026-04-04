from filter import get_top_ips, get_top_uris, get_failed_reads
from count import count_by_method, count_status_classes

def analyze_log(log):
    errors_4xx, errors_5xx = get_failed_reads(log)
    
    return {
        "top_ips": get_top_ips(log, n=10),
        "top_uris": get_top_uris(log, n=10),
        "method_distribution": count_by_method(log),
        "status_distribution": count_status_classes(log),
        "errors_4xx": len(errors_4xx),
        "errors_5xx": len(errors_5xx),
        "unique_ips": len(set(entry[2] for entry in log)),
        "unique_uris": len(set(entry[8] for entry in log)),
        "total_requests": len(log)
    }