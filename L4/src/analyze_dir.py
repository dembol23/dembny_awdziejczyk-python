import os, subprocess, sys, json, argparse
from collections import Counter

def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Analizuje statystycznie wszystkie pliki tekstowe w podanym katalogu, "
            "uruchamiając analyze_file.py przez subprocess dla każdego pliku."
        )
    )
    parser.add_argument(
        "directory",
        help="Ścieżka do katalogu, którego pliki mają zostać przeanalizowane.",
    )
    return parser.parse_args()

def get_files(directory_path):
    """Rekurencyjnie zwraca listę ścieżek plików z podanego katalogu."""
    result = []
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            result.append(file_path)
    return result

def run_analyzer(files):
    """
    Uruchamia analyze_file.py dla każdego pliku z listy.
    Zwraca listę słowników z wynikami analizy.
    """
    results = []
    all_chars_counter = Counter()
    all_words_counter = Counter()

    analyzer_path = os.path.join(os.path.dirname(__file__), "analyze_file.py")

    for file in files:
        try:
            process = subprocess.run(
                [sys.executable, analyzer_path],
                input=file,
                text=True,
                capture_output=True,
                check=True
            )

            data = json.loads(process.stdout)

            if data["top_char"]: all_chars_counter[data["top_char"]] += 1
            if data["top_word"]: all_words_counter[data["top_word"]] += 1

            results.append(data)

        except subprocess.CalledProcessError as e:
            print(f"Błąd analizy {file}: {e.stderr}", file=sys.stderr)
        except Exception as e:
            print(f"Nieoczekiwany błąd dla {file}: {e}", file=sys.stderr)

    print(f"Total files: {len(results)}")
    print(f"Total chars: {sum(r['chars'] for r in results)}")
    print(f"Total words: {sum(r['words'] for r in results)}")
    print(f"Total lines: {sum(r['lines'] for r in results)}")
    print(f"Top char: {all_chars_counter.most_common(1)[0][0] if all_chars_counter else 'brak'}")
    print(f"Top word: {all_words_counter.most_common(1)[0][0] if all_words_counter else 'brak'}")

    return results

if __name__ == "__main__":
    args = parse_args()
    directory = args.directory
 
    if not os.path.exists(directory):
        print(f"Błąd: '{directory}' nie istnieje.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(directory):
        print(f"Błąd: '{directory}' nie jest katalogiem.", file=sys.stderr)
        sys.exit(1)
 
    files = get_files(directory)
 
    if not files:
        print("Nie znaleziono żadnych plików w podanym katalogu.", file=sys.stderr)
        sys.exit(0)
 
    print(f"Znalezione pliki: {len(files)}")
    run_analyzer(files)