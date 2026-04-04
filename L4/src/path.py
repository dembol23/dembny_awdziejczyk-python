import os
import sys

def is_executable(path):
    # Sprawdza czy plik jest wykonywalny na uruchamianym systemie
    if os.name == 'nt':
        return path.lower().endswith(('.exe', '.bat', '.cmd'))
    return os.access(path, os.X_OK)

def main():
    """
        path.py             = wyświetla katalogi ze zmiennej środowiskowej PATH
        path.py --execs     = wyświetla katalogi ze zmiennej środowiskowej PATH oraz znajdujące się 
                              w nich pliki wykonywalne
    """
    
    GREEN = "\033[1;32m"
    RED="\033[1;31m"
    RESET = "\033[0m"

    path_dirs = os.environ.get("PATH", "").split(os.pathsep)
    show_execs = "--execs" in sys.argv

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
    if len(sys.argv) > 1 and not show_execs:
        print("-"*50)
        print(f"{RED}--execs żeby wyświetlić pliki wykonywalne{RESET}")
        print("-"*50)

if __name__ == "__main__":
    main()