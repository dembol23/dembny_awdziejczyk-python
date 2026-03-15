import sys

def search_longest_sentence(text):
    sentence = ""
    longest_sentence = ""
    longest_sentence_len = 0

    while char := text.read(1):
        sentence += char

        if char in ".!?":
            sentence = sentence.strip()
            if len(sentence) > longest_sentence_len:
                longest_sentence_len = len(sentence)
                longest_sentence = sentence
            sentence = ""

    return longest_sentence

if __name__ == "__main__":
    result = search_longest_sentence(sys.stdin)
    if result:
        print(result)