import sys

def filter_first_twenty(text):
    sentence = ""
    sentence_count = 0
    result = ""

    while (char := text.read(1)) and sentence_count < 20:
        sentence += char

        if char in ".!?":
            sentence = sentence.strip()
            result += f"{sentence}\n"
            sentence = ""
            sentence_count += 1

    return result


if __name__ == "__main__":
    result = filter_first_twenty(sys.stdin)
    if result:
        print(result)
