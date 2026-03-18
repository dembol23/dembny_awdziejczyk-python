import sys
from utils import read_sentences

def clean_spaces(text):
    text = text.strip()
    while "  " in text:
        text = text.replace("  ", " ")
    return text

def get_number_of_conjunctions(text):
    return (
        (" i " in text) +
        (" oraz " in text) +
        (" ale " in text) +
        (" że " in text) +
        (" lub " in text)
    )

def filter_two_conjunctions(text):
    try:
        for sentence in read_sentences(text):
            cleaned = clean_spaces(sentence.replace(",", ""))
            if get_number_of_conjunctions(cleaned) >= 2:
                yield sentence
    except Exception as e:
        print(e)


if __name__ == "__main__":
    for sentence in filter_two_conjunctions(sys.stdin):
        print(sentence)

