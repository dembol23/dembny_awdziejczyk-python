import sys

def filter_sentences_up_to_four_words(text):
    sentence = ""
    result = ""
    word_count = 1

    while char := text.read(1):
        sentence += char

        if char == " ":
            word_count += 1

        if char in ".!?":
            sentence = sentence.strip()
            if word_count <= 4:
                result += f"{sentence}\n"
            sentence = ""
            word_count = 1

    return result


if __name__ == "__main__":
    result = filter_sentences_up_to_four_words(sys.stdin)
    if result:
        print(result)
