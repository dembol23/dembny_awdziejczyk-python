def read_sentences(stream):
    sentence = ""
    prev_newline = False

    while char := stream.read(1):
        if char == '\n':
            if prev_newline:
                sentence = sentence.strip()
                if sentence:
                    yield sentence
                sentence = ""
                prev_newline = False
            else:
                prev_newline = True
                if sentence and not sentence.endswith(' '):
                    sentence += ' '
        else:
            prev_newline = False
            sentence += char
            if char in '.!?':
                sentence = sentence.strip()
                if sentence:
                    yield sentence
                sentence = ""

    sentence = sentence.strip()
    if sentence:
        yield sentence