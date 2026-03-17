import sys
from utils import read_sentences

def filter_first_twenty(text):
    count = 0
    try:
        for sentence in read_sentences(text):
            if count >= 20:
                break
            yield sentence
            count += 1
    except Exception as e:
        print(e)



if __name__ == "__main__":
    for sentence in filter_first_twenty(sys.stdin):
        print(sentence)