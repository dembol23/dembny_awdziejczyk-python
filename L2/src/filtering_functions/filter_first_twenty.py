import sys

def filter_first_twenty(text):
    sentence = ""
    sentence_count = 0

    while (char := text.read(1)) and sentence_count < 20:
        sentence += char

        if char in ".!?":
            sentence = sentence.strip()
            print(sentence)
            sentence = ""
            sentence_count += 1



if __name__ == "__main__":
    filter_first_twenty(sys.stdin)