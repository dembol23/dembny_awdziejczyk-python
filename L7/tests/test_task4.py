from src.generator import make_generator

def fibb(n: int = 1):
    a = 0
    b = 1
    for _ in range(n-1):
        a,b = b, a+b
    return a

def test_make_generator_with_fibb():
    gen = make_generator(fibb)
    
    assert next(gen) == 0  # fibb(1)
    assert next(gen) == 1  # fibb(2)
    assert next(gen) == 1  # fibb(3)
    assert next(gen) == 2  # fibb(4)
    assert next(gen) == 3  # fibb(5)

def test_make_generator_with_lambda():
    gen = make_generator(lambda x: x**2)
    
    assert next(gen) == 1   # 1^2
    assert next(gen) == 4   # 2^2
    assert next(gen) == 9   # 3^2
    assert next(gen) == 16  # 4^2