import sys, os, pathlib, json
from collections import Counter

def get_filepath():
    path = pathlib.Path(sys.stdin.readline().strip())
    if not path.exists():
        print(f"Error: {path} is not a path!", file=sys.stderr)
        sys.exit(1)
    if not path.is_file():
        print(f"Error: {path} is not a file!", file=sys.stderr)
        sys.exit(1)
    return path

def analyze_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    chars = len(content)
    words = len(content.split())
    lines = len(content.splitlines())
    top_char = Counter(ch for ch in content if not ch.isspace()).most_common(1)[0][0]
    top_word = Counter(content.split()).most_common(1)[0][0]

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
    analyze_file(get_filepath())