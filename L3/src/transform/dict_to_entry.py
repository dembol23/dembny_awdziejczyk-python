def dict_to_entry(d):
    keys = ["ts", "uid", "orig_h", "orig_p", "resp_h", "resp_p", "method", "host", "uri", "status"]
    return tuple(d.get(k) for k in keys)