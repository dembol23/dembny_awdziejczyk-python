import sys

def get_number_of_conjunctions(text):
    return (
        (" i " in text) +
        (" oraz " in text) +
        (" ale " in text) +
        (" że " in text) +
        (" lub " in text)
    )

def filter_two_conjunctions(text):
    sentence = ""
    result = ""

    while char := text.read(1):
        sentence += char

        if char in ".!?":
            sentence = sentence.strip().replace(",", "")
            if get_number_of_conjunctions(sentence) >= 2:
                result += f"{sentence}\n"
            sentence = ""

    return result


if __name__ == "__main__":
    result = filter_two_conjunctions(sys.stdin)
    if result:
        print(result)
