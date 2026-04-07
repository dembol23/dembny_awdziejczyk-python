import sys, datetime, subprocess, mimetypes
from utils import *

def mediaconvert(file):
    mime_type = mimetypes.guess_type(file)[0]

    if mime_type and mime_type.startswith("image"):
        format = "png"
    else:
        format = "mp4"

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    result_name = f"{timestamp}-{get_name(file)}.{format}"
    target_path = os.path.join(get_converted_dir(), result_name)

    if mime_type and mime_type.startswith('image'):
        tool = "magick"
        cmd = ["convert", file, target_path]
    else:
        tool = "ffmpeg"
        cmd = ["ffmpeg", "-i", file, target_path]

    subprocess.run(cmd, check=True)
    log_conversion(timestamp, file, format, target_path, tool)

if __name__ == "__main__":
    for file in get_files(sys.argv[1]):
        mediaconvert(file)