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
    total_files = 0
    total_chars = 0
    total_words = 0
    total_lines = 0
    all_chars_counter = Counter()
    all_words_counter = Counter()

    for file in files:
        try:
            process = subprocess.run(
                ["python", "analyze_file.py"],
                input=file.encode('utf-8'),
                capture_output=True,
                check=True
            )

            data = json.loads(process.stdout)

            total_files += 1
            total_chars += data["chars"]
            total_words += data["words"]
            total_lines += data["lines"]

            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                all_chars_counter.update(ch for ch in content if not ch.isspace())
                all_words_counter.update(content.split())

            results.append(data)

        except Exception as e:
            print(e, file=sys.stderr)

    print(f"Total files: {total_files}")
    print(f"Total chars: {total_chars}")
    print(f"Total words: {total_words}")
    print(f"Total lines: {total_lines}")
    print(f"Top char: {all_chars_counter.most_common(1)[0][0]}")
    print(f"Top word: {all_words_counter.most_common(1)[0][0]}")

    return results

if __name__ == "__main__":
    dir_path = sys.argv[1]
    print(run_analyzer(get_files(dir_path)))