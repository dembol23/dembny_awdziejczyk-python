import sys
from datetime import datetime

def ts_to_datetime(ts):
    return datetime.fromtimestamp(float(ts))

def list_to_tuple(line):
    ts = ts_to_datetime(line[0])
    uid = line[1]
    id_orig_host = line[2]
    id_orig_p = int(line[3])
    id_resp_h = line[4]
    id_resp_p = int(line[5])
    method = line[7]
    host = line[8]
    uri = line[9]
    status = line[14]

    return ts, uid, id_orig_host, id_orig_p, id_resp_h, id_resp_p, method, host, uri, status

def read_log(log):
    sep = "\t"
    return [list_to_tuple(line.strip().split(sep)) for line in log if line != ""]

if __name__ == '__main__':
    print(read_log(sys.stdin))
