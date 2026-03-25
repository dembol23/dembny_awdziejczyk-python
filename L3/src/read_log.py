import sys
from datetime import datetime

def safe_int(val, default=0):
    try:
        return int(val)
    except (ValueError, TypeError):
        return default

def ts_to_datetime(ts):
    return datetime.fromtimestamp(float(ts))

def list_to_tuple(line):
    ts = ts_to_datetime(line[0])
    uid = line[1]
    id_orig_host = line[2]
    id_orig_p = safe_int(line[3])
    id_resp_h = line[4]
    id_resp_p = safe_int(line[5])
    method = line[7]
    host = line[8]
    uri = line[9]
    status = safe_int(line[14])

    return ts, uid, id_orig_host, id_orig_p, id_resp_h, id_resp_p, method, host, uri, status

def read_log():
    sep = "\t"
    return [list_to_tuple(line.strip().split(sep)) for line in sys.stdin if line.strip() != ""]