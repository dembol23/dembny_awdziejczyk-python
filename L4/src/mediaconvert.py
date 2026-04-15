import sys, os, datetime, subprocess, mimetypes, argparse
from utils import *

SUPPORTED_IMAGE_FORMATS = {"png", "jpg", "jpeg", "webp", "gif", "bmp", "tiff", "avif"}
SUPPORTED_VIDEO_FORMATS = {"mp4", "mkv", "webm", "avi", "mov", "flv", "ogg", "mp3", "wav", "aac", "flac"}

def mediaconvert(file, fmt, converted_dir):
    mime_type = mimetypes.guess_type(file)[0]

    if mime_type is None:
        print(f"Pominięto '{file}': nieznany typ pliku", file=sys.stderr)
        return

    is_image = mime_type.startswith("image")
    is_media = mime_type.startswith("video") or mime_type.startswith("audio")

    if not is_image and not is_media:
        print(f"Pominięto '{file}': nieobsługiwany typ '{mime_type}'", file=sys.stderr)
        return

    if is_image:
        tool = "magick"
        effective_fmt = fmt if fmt in SUPPORTED_IMAGE_FORMATS else "png"
    else:
        tool = "ffmpeg"
        effective_fmt = fmt if fmt in SUPPORTED_VIDEO_FORMATS else "mp4"
    
    now = datetime.datetime.now()
    timestamp_file = now.strftime("%Y%m%d%H%M%S")
    timestamp_iso  = now.isoformat(timespec="seconds")
    result_name = f"{timestamp_file}-{get_name(file)}.{effective_fmt}"
    target_path = os.path.join(converted_dir, result_name)

    cmd = ["magick", file, target_path] if is_image else ["ffmpeg", "-i", file, target_path]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"Sukces: {target_path}")
        log_conversion(timestamp_iso, file, effective_fmt, target_path, tool, converted_dir)
    except subprocess.CalledProcessError as e:
        print(f"Błąd konwersji '{file}' (kod: {e.returncode})", file=sys.stderr)
        if e.stderr:
            print(e.stderr.decode(errors="replace"), file=sys.stderr)
    except FileNotFoundError:
        print(f"Błąd: '{tool}' nie jest zainstalowany lub nie znaleziono w PATH", file=sys.stderr)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Konwertuje pliki multimedialne (wideo/audio → ffmpeg, obrazy → magick)."
    )
    parser.add_argument(
        "path",
        help="Ścieżka do katalogu z plikami (lub pojedynczego pliku – dodatkowa funkcjonalność).",
    )
    parser.add_argument(
        "--format", "-f",
        dest="fmt",
        default=None,
        help=(
            "Format wyjściowy, np. mp4, webm, png, jpg. "
            "Domyślnie: mp4 dla wideo/audio, png dla obrazów."
        ),
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    path = args.path
    fmt = args.fmt
 
    if os.path.isdir(path):
        files = get_files(path)
    elif os.path.isfile(path):
        print(f"Uwaga: '{path}' to plik, nie katalog. Przetwarzam jako pojedynczy plik.")
        files = [path]
    else:
        print(f"Błąd: '{path}' nie istnieje", file=sys.stderr)
        sys.exit(1)
 
    if not files:
        print("Nie znaleziono żadnych plików do przetworzenia.", file=sys.stderr)
        sys.exit(0)
 
    print(f"Znalezione pliki ({len(files)}): {files}")
 
    converted_dir = get_converted_dir()
 
    for file in files:
        mime_type = mimetypes.guess_type(file)[0]
        if fmt is None:
            effective_fmt = "png" if (mime_type and mime_type.startswith("image")) else "mp4"
        else:
            effective_fmt = fmt
        mediaconvert(file, effective_fmt, converted_dir)