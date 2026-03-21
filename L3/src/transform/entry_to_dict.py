def entry_to_dict(entry):
    keys = ["ts", "uid", "orig_h", "orig_p", "resp_h", "resp_p", "method", "host", "uri", "status"]
    return dict(zip(keys, entry))

