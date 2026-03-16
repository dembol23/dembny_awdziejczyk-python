import sys

def filter_sentences_up_to_four_words(text):
    sentence = ""
    word_count = 0
    in_word = False

    while char := text.read(1):
        sentence += char

        if char.isalpha():
            if not in_word:
                word_count += 1
                in_word = True
        else:
            in_word = False

        if char in ".!?":
            sentence = sentence.strip()
            if word_count <= 4:
                print(sentence)
            sentence = ""
            word_count = 0
            in_word = False



if __name__ == "__main__":
    filter_sentences_up_to_four_words(sys.stdin)
