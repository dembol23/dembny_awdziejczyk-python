import os
import argparse

GREEN_BOLD = "\033[1;32m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"

def main():
    parser = argparse.ArgumentParser(description="Wyświetla wszystkie zmienne środowiskowe i ich wartości")
    parser.add_argument('filters', nargs='*', 
                        help="Filtry nazw zmiennych (case-insensitive), np. path user")
    args = parser.parse_args()

    filters = [f.lower() for f in args.filters]
    found = False

    for key, value in sorted(os.environ.items()):
        if not filters or any(f in key.lower() for f in filters):
            print(f"{GREEN_BOLD}{key}{RESET} = {value}")
            found = True

    if not found:
        print(f"{YELLOW}Brak zmiennych środowiskowych pasujących do podanych filtrów: {', '.join(args.filters)}{RESET}")

if __name__ == "__main__":
    main()