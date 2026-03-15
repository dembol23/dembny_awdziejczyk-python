import sys

def count_non_white_chars(text):
    char_count = 0

    try:
        while char := text.read(1):
            if not char.isspace():
                char_count += 1
        return char_count
    except Exception as e:
        print(e)
        return 0

if __name__ == "__main__":
    result = count_non_white_chars(sys.stdin)
    print(result)