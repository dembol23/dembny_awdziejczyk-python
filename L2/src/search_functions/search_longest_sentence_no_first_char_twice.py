import sys
from utils import read_sentences


def no_consecutive_same_first_char(sentence):
    last_first_char = ""
    in_word = False

    for char in sentence:
        if char.isalpha():
            if not in_word:
                char_lower = char.lower()
                if char_lower == last_first_char:
                    return False
                last_first_char = char_lower
                in_word = True
        else:
            in_word = False

    return True


def search_longest_sentence_no_first_char_twice(stream):
    longest = ""

    try:
        for sentence in read_sentences(stream):
            if no_consecutive_same_first_char(sentence) and len(sentence) > len(longest):
                longest = sentence
    except Exception as e:
        print(e)

    return longest

if __name__ == "__main__":
    result = search_longest_sentence_no_first_char_twice(sys.stdin)
    if result:
        print(result)