import sys

def count_paragraphs(text):
    paragraph_count = 0
    in_paragraph = False

    try:
        for line in text:
            line = line.strip()

            if line != "":
                if not in_paragraph:
                    in_paragraph = True
                    paragraph_count += 1
            else:
                in_paragraph = False
        return paragraph_count
    except Exception as e:
        print(e)
        return 0

def main():
    print(count_paragraphs(sys.stdin))

if __name__ == "__main__":
    main()