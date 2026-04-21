import argparse
import csv
import math
import os
import random
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Stałe – ścieżki plików
# ---------------------------------------------------------------------------

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SCRIPT_DIR)
STATIONS_FILE = os.path.join(BASE_DIR, "data/stacje.csv")
MEASUREMENTS_DIR = os.path.join(BASE_DIR, "data/measurements")
DATE_FMT_USER = "%Y-%m-%d"
DATE_FMT_FILE = "%d/%m/%y %H:%M"

# ---------------------------------------------------------------------------
# Walidatory (używane przez argparse jako typ argumentu)
# ---------------------------------------------------------------------------

VALID_INDICATORS = {
    "PM2.5", "PM10", "NO", "NO2", "NOx", "SO2", "CO", "O3", "C6H6",
    "Pb(PM10)", "Cd(PM10)", "As(PM10)", "Ni(PM10)", "BaP(PM10)",
}

VALID_FREQS = {"1g", "24g"}


def validate_indicator(value: str) -> str:
    """
    Sprawdza, czy podany wskaźnik należy do listy dozwolonych wartości.
    Argparse wywołuje tę funkcję automatycznie dla argumentu --indicator.
    Jeśli wartość jest niepoprawna, rzuca argparse.ArgumentTypeError,
    co wyświetla czytelny błąd i przerywa program.
    """
    if value not in VALID_INDICATORS:
        raise argparse.ArgumentTypeError(
            f"Nieznany wskaźnik: '{value}'. "
            f"Dozwolone wartości: {', '.join(sorted(VALID_INDICATORS))}"
        )
    return value


def validate_freq(value: str) -> str:
    """
    Sprawdza, czy podana częstotliwość uśredniania należy do dozwolonych wartości.
    """
    if value not in VALID_FREQS:
        raise argparse.ArgumentTypeError(
            f"Nieznana częstotliwość: '{value}'. "
            f"Dozwolone wartości: {', '.join(sorted(VALID_FREQS))}"
        )
    return value


def validate_date(value: str) -> datetime:
    """
    Parsuje datę w formacie YYYY-MM-DD do obiektu datetime.
    Jeśli format jest niepoprawny, rzuca argparse.ArgumentTypeError.
    """
    try:
        return datetime.strptime(value, DATE_FMT_USER)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Niepoprawna data: '{value}'. Oczekiwany format: RRRR-MM-DD"
        )


# ---------------------------------------------------------------------------
# Funkcje pomocnicze – ładowanie danych
# ---------------------------------------------------------------------------

def load_stations(path: str) -> list[dict]:
    """
    Wczytuje plik stacje.csv i zwraca listę słowników,
    gdzie każdy słownik odpowiada jednej stacji.

    Parametr path: ścieżka do pliku stacje.csv.
    """
    stations = []
    # Otwieramy plik z kodowaniem UTF-8 z BOM (często stosowanym w polskich plikach CSV).
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            stations.append(row)
    return stations


def build_measurement_path(indicator: str, freq: str) -> str:
    """
    Buduje ścieżkę do pliku z pomiarami na podstawie wskaźnika i częstotliwości.
    Szablon nazwy pliku to: <wskaźnik>_<częstotliwość>.csv
    Przykład: As(PM10)_24g.csv
    """
    filename = f"2023_{indicator}_{freq}.csv"
    return os.path.join(MEASUREMENTS_DIR, filename)


def load_measurements(
        path: str, start: datetime, end: datetime
) -> tuple[list[str], list[dict]]:
    """
    Wczytuje plik pomiarów i filtruje wiersze mieszczące się w przedziale [start, end].

    Zwraca krotkę (kody_stacji, wiersze_pomiarów):
      - kody_stacji: lista kodów stacji (nagłówek z wiersza "Kod stacji")
      - wiersze_pomiarów: lista słowników {kod_stacji: wartość_pomiaru}
        dla każdego kroku czasowego w zadanym przedziale.

    Pierwsze 6 wierszy pliku to metadane – pomijamy je i budujemy własny nagłówek.
    """
    if not os.path.exists(path):
        print(f"Błąd: plik pomiarów nie istnieje: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.reader(fh)
        rows = list(reader)

    station_codes = rows[1][1:]

    filtered_rows = []
    for data_row in rows[6:]:
        if not data_row or not data_row[0].strip():
            continue
        try:
            ts = datetime.strptime(data_row[0].strip(), DATE_FMT_FILE)
        except ValueError:
            continue

        if start <= ts <= end:
            row_dict = {"_timestamp": ts}
            for i, code in enumerate(station_codes):
                raw = data_row[i + 1].strip() if i + 1 < len(data_row) else ""
                row_dict[code] = raw
            filtered_rows.append(row_dict)

    return station_codes, filtered_rows


# ---------------------------------------------------------------------------
# Podkomenda: random-station
# ---------------------------------------------------------------------------

def cmd_random_station(args: argparse.Namespace) -> None:
    """
    Wypisuje nazwę i adres losowej stacji, która w zadanym przedziale czasowym
    mierzy wskaźnik podany przez użytkownika.

    Algorytm:
    1. Wczytaj plik pomiarów i odfiltruj wiersze z zadanego przedziału.
    2. Zbierz kody stacji, które mają co najmniej jeden niepusty pomiar.
    3. Dopasuj te kody do wpisów w stacje.csv.
    4. Wybierz losowo jedną stację i wypisz jej dane.
    """
    path = build_measurement_path(args.indicator, args.freq)
    station_codes, filtered_rows = load_measurements(path, args.start, args.end)

    if not filtered_rows:
        print(
            "Brak danych pomiarowych w podanym przedziale czasowym.",
            file=sys.stderr,
        )
        sys.exit(1)

    active_codes = set()
    for row in filtered_rows:
        for code in station_codes:
            val = row.get(code, "").strip()
            # Wartość niepusta i niebędąca samą spacją oznacza, że stacja mierzyła.
            if val:
                active_codes.add(code)

    if not active_codes:
        print(
            "Żadna stacja nie wykonała pomiarów w podanym przedziale.",
            file=sys.stderr,
        )
        sys.exit(1)

    stations = load_stations(STATIONS_FILE)

    matching_stations = [
        s for s in stations if s.get("Kod stacji", "").strip() in active_codes
    ]

    if not matching_stations:
        print(
            "Nie znaleziono metadanych dla żadnej aktywnej stacji w stacje.csv.",
            file=sys.stderr,
        )
        sys.exit(1)

    chosen = random.choice(matching_stations)

    print("=" * 55)
    print("Losowa stacja pomiarowa")
    print("=" * 55)
    print(f"Kod stacji : {chosen.get('Kod stacji', '').strip()}")
    print(f"Nazwa      : {chosen.get('Nazwa stacji', '').strip()}")
    print(f"Adres      : {chosen.get('Adres', '').strip()}")
    print(f"Miejscowość: {chosen.get('Miejscowość', '').strip()}")
    print(f"Województwo: {chosen.get('Województwo', '').strip()}")
    print("=" * 55)


# ---------------------------------------------------------------------------
# Podkomenda: stats
# ---------------------------------------------------------------------------

def cmd_stats(args: argparse.Namespace) -> None:
    """
    Oblicza średnią arytmetyczną i odchylenie standardowe (populacyjne)
    wartości wskaźnika dla podanej stacji w zadanym przedziale czasowym.

    Algorytm:
    1. Wczytaj i odfiltruj pomiary.
    2. Dla podanej stacji zbierz niepuste wartości numeryczne (pomijamy "0.5"
       jako wartość zastępczą? Nie – zadanie nie precyzuje, więc włączamy
       wszystkie niepuste i dające się sparsować liczby).
    3. Oblicz średnią i odchylenie standardowe.
    """
    path = build_measurement_path(args.indicator, args.freq)
    station_codes, filtered_rows = load_measurements(path, args.start, args.end)

    # Sprawdzamy, czy kod stacji istnieje w pliku pomiarów.
    target = args.station.strip()
    if target not in station_codes:
        print(
            f"Błąd: stacja '{target}' nie istnieje w pliku pomiarów.",
            file=sys.stderr,
        )
        print(
            f"Dostępne kody stacji: {', '.join(station_codes)}",
            file=sys.stderr,
        )
        sys.exit(1)

    if not filtered_rows:
        print(
            "Brak danych pomiarowych w podanym przedziale czasowym.",
            file=sys.stderr,
        )
        sys.exit(1)

    values = []
    for row in filtered_rows:
        raw = row.get(target, "").strip()
        if not raw:
            continue
        try:
            values.append(float(raw))
        except ValueError:
            continue

    if not values:
        print(
            f"Stacja '{target}' nie posiada żadnych pomiarów numerycznych "
            "w podanym przedziale.",
            file=sys.stderr,
        )
        sys.exit(1)

    n = len(values)
    mean = sum(values) / n

    # Odchylenie standardowe populacyjne:
    # sqrt( (1/n) * Σ(xi - mean)² )
    variance = sum((x - mean) ** 2 for x in values) / n
    std_dev = math.sqrt(variance)

    print("=" * 55)
    print(f"Statystyki dla stacji: {target}")
    print(f"Wskaźnik             : {args.indicator}  [{args.freq}]")
    print(f"Przedział            : {args.start.date()} – {args.end.date()}")
    print(f"Liczba pomiarów      : {n}")
    print(f"Średnia              : {mean:.4f} ng/m³")
    print(f"Odchylenie std.      : {std_dev:.4f} ng/m³")
    print("=" * 55)


# ---------------------------------------------------------------------------
# Budowanie parsera argparse
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """
    Tworzy i konfiguruje główny parser oraz podparsery dla podkomend.
    Zwraca gotowy obiekt ArgumentParser.
    """
    parser = argparse.ArgumentParser(
        prog="air_quality_cli",
        description=(
            "Narzędzie do analizy danych jakości powietrza.\n"
            "Dane: stacje.csv + measurements/<wskaźnik>_<częstotliwość>.csv"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Przykłady:\n"
            "  %(prog)s --indicator PM10 --freq 24g "
            "--start 2023-01-01 --end 2023-12-31 random-station\n"
            "  %(prog)s --indicator PM10 --freq 24g "
            "--start 2023-01-01 --end 2023-12-31 stats --station DsWrocWybCon\n"
        ),
    )

    parser.add_argument(
        "--indicator",
        required=True,
        type=validate_indicator,
        metavar="WSKAŹNIK",
        help=(
            f"Mierzona wielkość, np. PM10, PM2.5, NO2. "
            f"Dozwolone: {', '.join(sorted(VALID_INDICATORS))}"
        ),
    )

    parser.add_argument(
        "--freq",
        required=True,
        type=validate_freq,
        metavar="CZĘSTOTLIWOŚĆ",
        help="Czas uśredniania pomiaru: 1g (1 godzina) lub 24g (24 godziny).",
    )

    parser.add_argument(
        "--start",
        required=True,
        type=validate_date,
        metavar="RRRR-MM-DD",
        help="Początek przedziału czasowego (format: RRRR-MM-DD).",
    )

    parser.add_argument(
        "--end",
        required=True,
        type=validate_date,
        metavar="RRRR-MM-DD",
        help="Koniec przedziału czasowego (format: RRRR-MM-DD).",
    )

    # --- Podparsery (subcommands) ---

    # add_subparsers tworzy grupę podkomend.
    # dest="command" zapisuje nazwę wybranej podkomendy do args.command.
    # required=True wymusza podanie podkomendy – bez niej program wypisze help.
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        title="Podkomendy",
        description="Wybierz jedną z dostępnych operacji:",
        metavar="PODKOMENDA",
    )

    # Podkomenda: random-station
    subparsers.add_parser(
        "random-station",
        help=(
            "Wypisz nazwę i adres losowej stacji mierzącej podany wskaźnik "
            "w zadanym przedziale czasowym."
        ),
    )

    # Podkomenda: stats
    stats_parser = subparsers.add_parser(
        "stats",
        help=(
            "Oblicz średnią i odchylenie standardowe wskaźnika "
            "dla wybranej stacji w zadanym przedziale czasowym."
        ),
    )
    # Argument wymagany tylko przez podkomendę stats.
    stats_parser.add_argument(
        "--station",
        required=True,
        metavar="KOD_STACJI",
        help="Kod stacji, np. DsWrocWybCon.",
    )

    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.start > args.end:
        parser.error(
            f"Data początkowa ({args.start.date()}) nie może być "
            f"późniejsza od daty końcowej ({args.end.date()})."
        )

    if args.command == "random-station":
        cmd_random_station(args)
    elif args.command == "stats":
        cmd_stats(args)


if __name__ == "__main__":
    main()