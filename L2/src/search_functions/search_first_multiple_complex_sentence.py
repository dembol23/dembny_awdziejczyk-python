import sys
from utils import read_sentences

def count_commas(sentence):
    count = 0
    for char in sentence:
        if char == ',':
            count += 1
    return count

def search_first_multiple_complex_sentence(text):
    try:
        for sentence in read_sentences(text):
            if count_commas(sentence) > 1:
                return sentence
    except Exception as e:
        print(e)

    return ""

if __name__ == "__main__":
    result = search_first_multiple_complex_sentence(sys.stdin)
    if result:
        print(result)