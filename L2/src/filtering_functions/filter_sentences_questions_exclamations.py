import sys

def filter_sentences_questions_exclamations(text):
    sentence = ""
    result = ""

    while char := text.read(1):
        sentence += char

        if char in ".!?":
            sentence = sentence.strip()
            if char in "!?":
                result += f"{sentence}\n"
            sentence = ""

    return result


if __name__ == "__main__":
    result = filter_sentences_questions_exclamations(sys.stdin)
    if result:
        print(result)
