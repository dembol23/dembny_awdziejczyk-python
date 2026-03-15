import sys

def count_sentences_with_proper_noun(text):
    total_sentences = 0
    counter = 0
    is_first_word = True
    word_beginning = True
    already_found = False

    try:
        while char := text.read(1):
            if char.isspace() or char in ',;":-':
                word_beginning = True
            elif char in '.!?':
                total_sentences += 1
                is_first_word = True
                word_beginning = True
                if already_found:
                    counter += 1
                already_found = False
            elif char.isalpha():
                if word_beginning:
                    if not is_first_word and char.isupper() and not already_found:
                        already_found = True
                    is_first_word = False
                    word_beginning = False

        if total_sentences == 0:
            return 0
        return (counter / total_sentences) * 100
    except Exception as e:
        print(e)
        return 0

if __name__ == "__main__":
    result = count_sentences_with_proper_noun(sys.stdin)
    print(result)