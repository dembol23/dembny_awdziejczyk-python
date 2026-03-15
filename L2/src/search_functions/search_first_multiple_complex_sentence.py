import sys

def search_first_multiple_complex_sentence(text):
    sentence = ""
    comma_count = 0

    while char := text.read(1):
        sentence += char

        if char == ",":
            comma_count += 1

        if char in ".!?":
            sentence = sentence.strip()
            if comma_count > 1:
                return sentence
            sentence = ""
            comma_count = 0
    return ""

if __name__ == "__main__":
    result = search_first_multiple_complex_sentence(sys.stdin)
    if result:
        print(result)