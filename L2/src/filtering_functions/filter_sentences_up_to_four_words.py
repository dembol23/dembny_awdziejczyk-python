import sys
from utils import read_sentences

def count_words(sentence):
    count = 0
    in_word = False
    for char in sentence:
        if char.isalpha():
            if not in_word:
                count += 1
                in_word = True
        else:
            in_word = False
    return count

def filter_sentences_up_to_four_words(text):
    try:
        for sentence in read_sentences(text):
            if count_words(sentence) <= 4:
                yield sentence
    except Exception as e:
        print(e)



if __name__ == "__main__":
    for sentence in filter_sentences_up_to_four_words(sys.stdin):
        print(sentence)