import os
import argparse

GREEN = "\033[1;32m"
RED = "\033[1;31m"
RESET = "\033[0m"

def is_executable(path):
    # Sprawdza czy plik jest wykonywalny na uruchamianym systemie
    if os.name == 'nt':
        return path.lower().endswith(('.exe', '.bat', '.cmd'))
    return os.access(path, os.X_OK)

def main():
    parser = argparse.ArgumentParser(description="Wyświetla katalogi ze zmiennej PATH")
    parser.add_argument('--execs', action='store_true', 
                        help="Pokaż pliki wykonywalne w każdym katalogu")
    args = parser.parse_args()

    path_env = os.environ.get("PATH", "")
    if not path_env:
        print("Zmienna PATH jest pusta lub nieustawiona.")
        return
    path_dirs = path_env.split(os.pathsep)
    show_execs = args.execs

    for directory in path_dirs:
        if os.path.isdir(directory):
            print(f"{GREEN}{directory}{RESET}")
            if show_execs:
                try:
                    for file in os.listdir(directory):
                        full_path = os.path.join(directory, file)
                        if os.path.isfile(full_path) and is_executable(full_path):
                            print(f"  └── {file}")
                except PermissionError:
                    print("  [Brak uprawnień do odczytu]")
        else:
            print(f"{GREEN}{directory}{RESET} {RED}[Katalog nie istnieje]{RESET}")

if __name__ == "__main__":
    main()