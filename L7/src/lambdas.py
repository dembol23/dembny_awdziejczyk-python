from functools import reduce

# 1a. Funkcja, która przyjmuje na wejściu listę ciągów znaków akronim zbudowany z tych ciągów znaków.
def acronym(l: list[str]) -> str:
    result = ""
    return reduce(lambda acc, string: acc + string[0].upper(), l, result)

# 1b.  Funkcja, która przyjmuje na wejściu przyjmuje listę liczb i zwraca ich medianę.
# Funkcja nie może korzystać z modułu statistics ani żadnego innego modułu do obliczeń statystycznych.

def median(l: list[float]) -> float:
    length = len(l)
    list.sort(l)
    return (l[length//2 - 1] + l[length//2]) / 2 if length % 2 == 0 else l[length//2]

# 1c. Funkcja obliczająca pierwiastek kwadratowy metodą Netwona. Funkcja
# przyjmuje na wejściu pierwiastkowaną liczbę 𝑥 oraz epsilon i zwraca taki 𝑦, że
# y >= 0 i |y^2 - x| < epsilon
# metoda Newtona - https://www.algorytm.edu.pl/algorytmy-maturalne/newton-raphson.html

def pierwiastek(x: float, epsilon: float) -> float:
    def step(y: float) -> float:
        return (y + x / y) / 2

    def iterate(y: float) -> float:
        return y if abs(y * y - x) < epsilon else iterate(step(y))

    return iterate(x / 2)

# 1d. Funkcja, która przyjmuje na wejściu ciąg znaków, a zwraca na wyjściu słownik,
# w którym kluczami są znaki występujące alfabetyczne występujące ciągu, a wartościami listy słów zawierających te znaki.

def make_alpha_dict(s: str) -> dict[str, list[str]]:
    words = s.split()
    letters = {letter for word in words for letter in word if letter.isalpha()}
    return {letter: [word for word in words if letter in word] for letter in letters}

# 1e.  Funkcja spłaszczająca listy. Funkcja powinna przyjmować listę, której elementami mogą być elementy skalarne lub sekwencje.
# Spłaszczenie polega na zmianie zagnieżdżonej struktury na jednowymiarową listę zawierającą wszystkie elementy wewnętrznych sekwencji.
# Spłaszczenie powinno działać na wszystkich poziomach zagnieżdżeń, tzn. wynikowa lista powinna zawierać tylko elementy skalarne.
# Na potrzeby zadania należy przyjąć, że elementy skalarne to takie, które nie są listami ani krotkami.

def flatten(l: list | tuple) -> list:
    return sum([flatten(e) if isinstance(e, (list, tuple)) else [e] for e in l], [])

# 1f. Funkcja grupująca anagramy. Funkcja powinna przyjmować listę słów i zwracać słownik,
# w którym kluczem jest kanoniczna postać słowa (np. słowo z literami posortowanymi alfabetycznie),
# a wartością lista słów będących anagramami.
def _word_canonical(word: str) -> str:
    return "".join(sorted(word))

def group_anagrams(l: list[str]) -> dict[str, list[str]]:
    pairs = [(_word_canonical(word), word) for word in l]
    keys = {key for key, _ in pairs}
    return {key: [word for k, word in pairs if k == key] for key in keys}
