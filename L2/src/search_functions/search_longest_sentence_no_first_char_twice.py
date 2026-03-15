import sys

def search_longest_sentence_no_first_char_twice(text):
    sentence = ""
    is_new_word = True
    no_first_char_twice = True
    last_first_char = ""
    longest_sentence = ""
    longest_sentence_len = 0

    while char := text.read(1):
        sentence += char

        if is_new_word and char.isalpha():
            char_lower = char.lower()

            if char_lower == last_first_char:
                no_first_char_twice = False
            last_first_char = char_lower
            is_new_word = False

        if char.isspace():
            is_new_word = True

        if char in ".!?":
            sentence = sentence.strip()
            if no_first_char_twice and len(sentence) > longest_sentence_len:
                longest_sentence_len = len(sentence)
                longest_sentence = sentence
            sentence = ""
            last_first_char = ""
            is_new_word = True
            no_first_char_twice = True


    return longest_sentence

if __name__ == "__main__":
    result = search_longest_sentence_no_first_char_twice(sys.stdin)
    if result:
        print(result)