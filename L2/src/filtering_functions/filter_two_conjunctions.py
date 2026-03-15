import sys

def get_number_of_conjunctions(text):
    count = 0
    count += (text.count(" i ") > 0)
    count += (text.count(" oraz ") > 0)
    count += (text.count(" ale ") > 0)
    count += (text.count(" że ") > 0)
    count += (text.count(" lub ") > 0)
    return count

def filter_two_conjunctions(text):
    sentence = ""
    result = ""

    while char := text.read(1):
        sentence += char

        if char in ".!?":
            sentence = sentence.strip()
            if get_number_of_conjunctions(sentence) >= 2:
                result += f"{sentence}\n"
            sentence = ""

    return result


if __name__ == "__main__":
    result = filter_two_conjunctions(sys.stdin)
    if result:
        print(result)
