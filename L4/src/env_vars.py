import os
import sys

def main():
    args = [i.lower() for i in sys.argv[1:]]
    GREEN_BOLD = "\033[1;32m"
    RESET = "\033[0m"
    for key, value in sorted(os.environ.items()):
        if not args or any(arg in key.lower() for arg in args):
            print(f"{GREEN_BOLD}{key}{RESET} = {value}")

if __name__ == "__main__":
    main()