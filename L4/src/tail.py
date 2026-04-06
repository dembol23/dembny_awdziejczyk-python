import argparse, sys, time
from collections import deque

def main():
    parser = argparse.ArgumentParser(description="Wyświetla ostatnie linie pliku")
    parser.add_argument('--lines', type=int, default=10, help="Liczba linii do wyświetlenia (domyślnie 10)")
    parser.add_argument('--follow', action='store_true', help="Śledź plik i wyświetlaj nowe linie na bieżąco")
    parser.add_argument('file', nargs='?', help="Ścieżka do pliku (jeśli nie podano, czyta ze stdin)")
    args = parser.parse_args()

    if args.follow and not args.file:
        print("Błąd: --follow wymaga podania pliku", file=sys.stderr)
        sys.exit(1)

    if args.file:
        try:
            source = open(args.file, 'r')
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku '{args.file}'", file=sys.stderr)
            sys.exit(1)
    elif not sys.stdin.isatty():
        # sys.stdin.isatty() zwraca False gdy stdin ma podane dane przez pipe, True gdy nie
        source = sys.stdin
    else:
        print("Błąd: podaj plik lub dane na stdin", file=sys.stderr)
        sys.exit(1)
        
    try:
        lines = deque(source, maxlen = args.lines)
        print(''.join(lines), end='', flush=True) 

        if args.follow:
            source.seek(0, 2)
            try:
                while True:
                    line = source.readline()
                    if line:
                        print(line, end='', flush=True)
                    else:
                        time.sleep(0.1)
            except KeyboardInterrupt:
                pass

    finally:
        if source is not sys.stdin:
            source.close()
    
    


if __name__ == "__main__":
    main()