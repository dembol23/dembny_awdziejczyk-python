import re

def validate_ip(ip):
    pattern = (r"^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
            r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
            r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
            r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    return re.match(pattern, ip)

def get_entries_by_addr(log, addr):
    if validate_ip(addr):
        return [entry for entry in log if entry[2] == addr]
    else:
        return [entry for entry in log if entry[7] == addr]
