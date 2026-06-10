from itertools import groupby, accumulate, repeat

def acronym(words: list[str]) -> str:
    return "".join(map(lambda word: word[0].upper() if len(word) > 0 else "", words))

def median(l: list[float]) -> float:
    if len(l) == 0: raise ValueError("Empty list")
    l = sorted(l)
    mid = len(l) // 2
    return (l[mid - 1] + l[mid]) / 2 if len(l) % 2 == 0 else l[mid]

def square_root(x: float, epsilon: float) -> float:
    '''
        steps - leniwy generator kolejnych kroków
        next - wybiera jeden ostateczny wynik po zatrzymaniu się pętli
    '''
    if x < 0: raise ValueError("Can't root a negative number")
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
    return {k: list(group) for k, group in groupby(sorted(l, key=_word_canonical), key=_word_canonical)}

if __name__ == "__main__":
    print(square_root(10, epsilon=0.001))
    print(make_alpha_dict("on i ona"))
    print(group_anagrams(["kot", "tok", "pies", "kep", "pek", "tok"]))