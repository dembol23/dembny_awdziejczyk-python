from itertools import groupby, accumulate, repeat

def acronym(words: list[str]) -> str:
    return "".join(map(lambda word: word[0].upper(), words))

def median(l: list[float]) -> float:
    s = sorted(l)
    mid = len(s) // 2
    return (s[mid - 1] + s[mid]) / 2 if len(s) % 2 == 0 else s[mid]

def pierwiastek(x: float, epsilon: float) -> float:
    '''
        steps - leniwy generator kolejnych kroków
        next - wybiera jeden ostateczny wynik po zatrzymaniu się pętli
    '''
    step = lambda y: (y + x / y) / 2
    steps = accumulate(repeat(None), lambda y, _: step(y), initial=x / 2)
    return next(y for y in steps if abs(y * y - x) < epsilon)

def make_alpha_dict(s: str) -> dict[str, list[str]]:
    words = s.split()
    letters = {letter for word in words for letter in word if letter.isalpha()}
    return {letter: [word for word in words if letter in word] for letter in letters}

def flatten(l: list | tuple) -> list:
    return [item for elem in l for item in (flatten(elem) if isinstance(elem, (list, tuple)) else [elem])]

def _word_canonical(word: str) -> str:
    return "".join(sorted(word))

def group_anagrams(l: list[str]) -> dict[str, list[str]]:
    '''
        pairs - sortuje według postaci kanonicznej
        groupby - grupuje występujące po sobie słowa według postaci kanonicznych
    '''
    return {k: list(group) for k, group in groupby(sorted(l, key=_word_canonical), key=_word_canonical)}

if __name__ == "__main__":
    print(group_anagrams(["kot", "tok", "pies", "kep", "pek"]))