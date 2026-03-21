from collections import defaultdict
from .entry_to_dict import entry_to_dict

def log_to_dict(log):
    result = defaultdict(list)
    for entry in log:
        result[entry[1]].append(entry_to_dict(entry))
    return dict(result)
        
