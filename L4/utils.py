import os, csv

def get_converted_dir():
    target = os.getenv("CONVERTED_DIR", "converted")
    os.makedirs(target, exist_ok=True)

    return target

def get_name(file):
    return os.path.splitext(os.path.basename(file))[0]

def get_files(dir_name):
    result = []
    for root, dirs, files in os.walk(dir_name):
        for filename in files:
            result.append(os.path.join(root, filename))
    return result

def log_conversion(timestamp, org_path, target_format, target_path, tool_used):
    name = os.path.join(get_converted_dir(), "history.csv")
    with open(name, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, org_path, target_format, target_path, tool_used])