import sys
from utils import read_sentences

def search_longest_sentence(text):
    longest = ""

    try:
        for sentence in read_sentences(text):
            if len(sentence) > len(longest):
                longest = sentence
    except Exception as e:
        print(e)

    return longest

if __name__ == "__main__":
    result = search_longest_sentence(sys.stdin)
    if result:
        print(result)