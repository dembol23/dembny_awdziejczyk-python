import sys

def search_first_multiple_complex_sentence():
    sentence = ""
    comma_count = 0

    while char := sys.stdin.read(1):
        sentence += char

        if char == ",":
            comma_count += 1

        if char in ".!?":
            sentence = sentence.strip()
            if comma_count > 1:
                print(sentence)
                break
            sentence = ""
            comma_count = 0


if __name__ == "__main__":
    search_first_multiple_complex_sentence()