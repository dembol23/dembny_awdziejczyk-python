import sys

def count_paragraphs(text):
    paragraph_count = 0
    in_paragraph = False
    consecutive_newlines = 0

    try:
        while char := text.read(1):
            if char == '\n':
                consecutive_newlines += 1
                if consecutive_newlines >= 2:
                    in_paragraph = False

            elif not  char.isspace():
                consecutive_newlines = 0
                if not in_paragraph:
                    in_paragraph = True
                    paragraph_count += 1
            else:
                consecutive_newlines = 0
        return paragraph_count
    except Exception as e:
        print(e)
        return 0

if __name__ == "__main__":
    result = count_paragraphs(sys.stdin)
    print(result)