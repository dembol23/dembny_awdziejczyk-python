import sys
from utils import read_sentences

def filter_sentences_questions_exclamations(text):
    try:
        for sentence in read_sentences(text):
            if sentence and sentence[-1] in '!?':
                yield sentence
    except Exception as e:
        print(e)

if __name__ == "__main__":
    for sentence in filter_sentences_questions_exclamations(sys.stdin):
        print(sentence)