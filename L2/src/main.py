import sys

def echo(sentence):
    return sentence

def clean_spaces(text):
    cleaned_text = text.strip()
    while "  " in cleaned_text:
        cleaned_text = cleaned_text.replace("  ", " ")
    return cleaned_text

def main(func):
    line_count = 0
    empty_lines_in_a_row = 0
    buffer = ""
    preamble_checked = False

    for line in sys.stdin:
        text = clean_spaces(line)
        if text == "-----":
            break
        if not preamble_checked:
            buffer += text + "\n"
            if text == "":
                empty_lines_in_a_row += 1
            else:
                empty_lines_in_a_row = 0
            line_count += 1
            if empty_lines_in_a_row >= 2:
                preamble_checked = True
                buffer = ""
            if line_count >= 10 and empty_lines_in_a_row < 2:
                print(func(buffer), end = "")
                preamble_checked = True
        else:
            print(func(clean_spaces(line)))



if __name__ == "__main__":
    main(echo)