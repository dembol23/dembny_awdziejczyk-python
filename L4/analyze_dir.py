import os, subprocess, sys, json
from collections import Counter

def get_files(directory_path):
    result = []
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            result.append(file_path)
    return result

def run_analyzer(files):
    results = []
    all_chars_counter = Counter()
    all_words_counter = Counter()

    analyzer_path = os.path.join(os.path.dirname(__file__), "analyze_file.py")

    for file in files:
        try:
            process = subprocess.run(
                ["python", analyzer_path],
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
    if len(sys.argv) != 2:
        print("Użycie: python analyze_dir.py <ścieżka_do_katalogu>", file=sys.stderr)
        sys.exit(1)

    run_analyzer(get_files(sys.argv[1]))