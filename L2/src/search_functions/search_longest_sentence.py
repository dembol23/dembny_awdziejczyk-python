import sys

def search_longest_sentence():
    sentence = ""
    longest_sentence = ""
    longest_sentence_len = 0

    while char := sys.stdin.read(1):
        sentence += char

        if char in ".!?":
            sentence = sentence.strip()
            if len(sentence) > longest_sentence_len:
                longest_sentence_len = len(sentence)
                longest_sentence = sentence
            sentence = ""

    print(longest_sentence)

if __name__ == "__main__":
    search_longest_sentence()