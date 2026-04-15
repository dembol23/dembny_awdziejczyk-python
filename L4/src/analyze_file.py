import sys, pathlib, json, argparse
from collections import Counter

def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Analizuje plik tekstowy i wypisuje statystyki w formacie JSON. "
            "Ścieżkę do pliku można podać jako argument lub przesłać na stdin."
        )
    )
    parser.add_argument(
        "file",
        nargs="?",
        help=(
            "Ścieżka do pliku tekstowego do analizy. "
            "Jeśli nie podano, ścieżka czytana jest ze stdin."
        ),
    )
    return parser.parse_args()

def get_filepath(args):
    """
    Zwraca obiekt pathlib.Path na podstawie argumentu CLI lub stdin.
    Kończy program z błędem, gdy ścieżka nie istnieje lub nie jest plikiem.
    """
    if args.file:
        raw = args.file
    else:
        raw = sys.stdin.readline().strip()
        if not raw:
            print("Błąd: nie podano ścieżki do pliku (ani jako argumentu, ani przez stdin).",
                  file=sys.stderr)
            sys.exit(1)
 
    path = pathlib.Path(raw)
 
    if not path.exists():
        print(f"Błąd: '{path}' nie istnieje.", file=sys.stderr)
        sys.exit(1)
    if not path.is_file():
        print(f"Błąd: '{path}' nie jest plikiem.", file=sys.stderr)
        sys.exit(1)
 
    return path

def analyze_file(filepath):
    """Analizuje plik i wypisuje wynik jako JSON na stdout."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"Błąd: '{filepath}' nie jest poprawnym plikiem tekstowym UTF-8.", file=sys.stderr)
        sys.exit(1)

    chars = len(content)
    word_list = content.split()
    words = len(word_list)
    lines = len(content.splitlines())
    top_char = Counter(ch for ch in content if not ch.isspace()).most_common(1)[0][0] if content.strip() else ""
    top_word = Counter(word_list).most_common(1)[0][0] if word_list else ""

    result = {
        "filepath": str(filepath.resolve()),
        "chars": chars,
        "words": words,
        "lines": lines,
        "top_char": top_char,
        "top_word": top_word
    }

    print(json.dumps(result, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    analyze_file(get_filepath(parse_args()))