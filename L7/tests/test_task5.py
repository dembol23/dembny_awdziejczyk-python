from src.generator import mem_make_generator, mem_make_generator_rec

call_count_mem = 0
call_count_rec = 0

def fib_mem(n):
    global call_count_mem
    call_count_mem += 1
    if n < 2:
        return n
    return fib_mem(n - 1) + fib_mem(n - 2)

def fib_rec(n):
    global call_count_rec
    call_count_rec += 1
    if n < 2:
        return n
    return fib_rec(n - 1) + fib_rec(n - 2)

def test_call_count_comparison():
    global call_count_mem, call_count_rec
    call_count_mem = 0
    call_count_rec = 0

    gen_mem = mem_make_generator(fib_mem)
    gen_rec = mem_make_generator_rec(fib_rec)

    for _ in range(8):
        next(gen_mem)
        next(gen_rec)


    print(f"Wywołania przy zwykłym cache: {call_count_mem}")
    print(f"Wywołania przy podmianie funkcji w module: {call_count_rec}")

    gen_mem_2 = mem_make_generator(fib_mem)
    for _ in range(8):
        next(gen_mem_2)

    print(f"Wywołania po drugim mem_make_generator: {call_count_mem}")

    gen_rec_2 = mem_make_generator_rec(fib_rec)
    for _ in range(8):
        next(gen_rec_2)

    print(f"Wywołania po drugim mem_make_generator (rec): {call_count_rec}")




if __name__ == "__main__":
    test_call_count_comparison()