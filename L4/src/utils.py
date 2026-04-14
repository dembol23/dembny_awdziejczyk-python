import os, csv

def get_converted_dir():
    """Zwraca ścieżkę katalogu docelowego i tworzy go jeśli nie istnieje."""
    target = os.getenv("CONVERTED_DIR", "converted")
    os.makedirs(target, exist_ok=True)
    return target

def get_name(file):
    """Zwraca nazwę pliku bez rozszerzenia."""
    return os.path.splitext(os.path.basename(file))[0]

def get_files(dir_name):
    """
    Rekurencyjnie zwraca listę plików z katalogu dir_name,
    pomijając katalog docelowy (CONVERTED_DIR), by uniknąć
    przetwarzania już skonwertowanych plików.
    """
    converted = os.path.abspath(get_converted_dir())
    result = []
    for root, dirs, files in os.walk(dir_name):
        if os.path.abspath(root).startswith(converted):
            continue
        for filename in files:
            result.append(os.path.join(root, filename))
    return result

def log_conversion(timestamp, org_path, target_format, target_path, tool_used, converted_dir=None):
    """
    Zapisuje wpis do pliku history.csv w katalogu docelowym.
 
    Parametry:
        timestamp     – znacznik czasu w formacie ISO 8601
        org_path      – oryginalna ścieżka pliku
        target_format – format wyjściowy (np. mp4, png)
        target_path   – ścieżka pliku wynikowego
        tool_used     – użyte narzędzie (ffmpeg / magick)
        converted_dir – katalog docelowy; jeśli None, używany jest get_converted_dir()
    """
    if converted_dir is None:
        converted_dir = get_converted_dir()
 
    history_path = os.path.join(converted_dir, "history.csv")
    file_exists = os.path.isfile(history_path)
 
    with open(history_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "original_path", "format", "target_path", "tool"])
        writer.writerow([timestamp, org_path, target_format, target_path, tool_used])