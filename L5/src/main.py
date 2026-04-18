from pathlib import Path
from data_parser import *


def main():
    obecny_katalog    = Path(__file__).parent
    katalog_pomiarow  = obecny_katalog.parent / "data" / "measurements"
    # res               = group_measurement_files_by_key(katalog_pomiarow)
    res               = get_addresses(katalog_pomiarow.parent / "stacje.csv", "nowa ruda")
    print(res)

    # ── Nagłówek tabeli ───────────────────────────────────────────────────────
    # ROK  = 6
    # PAR  = 10
    # CZAS = 5
    # PLIK = max((len(p.name) for p in res.values()), default=20)

    # sep_top = f"╔{'═'*(ROK+2)}╦{'═'*(PAR+2)}╦{'═'*(CZAS+2)}╦{'═'*(PLIK+2)}╗"
    # sep_mid = f"╠{'═'*(ROK+2)}╬{'═'*(PAR+2)}╬{'═'*(CZAS+2)}╬{'═'*(PLIK+2)}╣"
    # sep_bot = f"╚{'═'*(ROK+2)}╩{'═'*(PAR+2)}╩{'═'*(CZAS+2)}╩{'═'*(PLIK+2)}╝"
    # header  = f"║ {'ROK':<{ROK}} ║ {'PARAMETR':<{PAR}} ║ {'CZAS':<{CZAS}} ║ {'PLIK':<{PLIK}} ║"

    # print(f"\n{sep_top}")
    # print(header)
    # print(sep_mid)

    # for i, (key, path) in enumerate(res.items()):
    #     rok, parametr, czas = key
    #     # FiraCode: => to ligatura strzałki
    #     print(f"║ {rok:<{ROK}} ║ {parametr:<{PAR}} ║ {czas:<{CZAS}} ║ {path.name:<{PLIK}} ║")
    #     if i < len(res) - 1:
    #         print(sep_mid)

    # print(sep_bot)
    # print(f"\n  => Znaleziono {len(res)} plików pomiarowych.\n")


if __name__ == "__main__":
    main()