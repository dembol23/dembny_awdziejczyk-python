import sys

def filter_sentences_questions_exclamations(text):
    sentence = ""

    while char := text.read(1):
        sentence += char

        if char in ".!?":
            sentence = sentence.strip()
            if char in "!?":
                print(sentence)
            sentence = ""

if __name__ == "__main__":
    filter_sentences_questions_exclamations(sys.stdin)