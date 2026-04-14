import sys, datetime, subprocess, mimetypes
from utils import *

def mediaconvert(file):
    mime_type = mimetypes.guess_type(file)[0]

    fmt = "png" if mime_type and mime_type.startswith("image") else "mp4"

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    result_name = f"{timestamp}-{get_name(file)}.{fmt}"
    target_path = os.path.join(get_converted_dir(), result_name)

    if mime_type and mime_type.startswith('image'):
        tool = "magick"
        cmd = ["convert", file, target_path]
    else:
        tool = "ffmpeg"
        cmd = ["ffmpeg", "-i", file, target_path]

    try:
        subprocess.run(cmd, check=True)
        print(f"Sukces: {target_path}")
        log_conversion(timestamp, file, fmt, target_path, tool)
    except subprocess.CalledProcessError as e:
        print(f"Błąd konwersji '{file}' (kod: {e.returncode})", file=sys.stderr)
    except FileNotFoundError:
        print(f"Błąd: '{tool}' nie jest zainstalowany", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Użycie: python mediaconvert.py <ścieżka>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    if os.path.isfile(path):
        files = [path]
    elif os.path.isdir(path):
        files = get_files(path)
    else:
        print(f"Błąd: '{path}' nie istnieje", file=sys.stderr)
        sys.exit(1)

    print(f"Znalezione pliki: {files}")
    for file in files:
        mediaconvert(file)