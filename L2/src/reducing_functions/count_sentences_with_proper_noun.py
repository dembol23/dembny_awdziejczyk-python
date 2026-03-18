import sys
from utils import read_sentences


def has_proper_noun(sentence):
    is_first_word = True
    in_word = False

    for char in sentence:
        if char.isspace() or char in ',;":-':
            in_word = False
        elif char in '.!?':
            in_word = False
        elif char.isalpha():
            if not in_word:
                if not is_first_word and char.isupper():
                    return True
                is_first_word = False
                in_word = True

    return False

def count_sentences_with_proper_noun(text):
    total_sentences = 0
    counter = 0

    try:
        for sentence in read_sentences(text):
            total_sentences += 1
            if has_proper_noun(sentence):
                counter += 1

        if total_sentences == 0:
            return 0
        return (counter / total_sentences) * 100
    except Exception as e:
        print(e)
        return 0

if __name__ == "__main__":
    result = count_sentences_with_proper_noun(sys.stdin)
    print(result)