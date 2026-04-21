import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path
from air_quality_stats import get_random_active_station, calculate_station_stats
from data_parser import group_measurement_files_by_key

# ---------------------------------------------------------------------------
# Stałe
# ---------------------------------------------------------------------------

BASE_DIR         = Path(__file__).parent.parent
STATIONS_FILE    = BASE_DIR / "data" / "stacje.csv"
MEASUREMENTS_DIR = BASE_DIR / "data" / "measurements"

# ---------------------------------------------------------------------------
# Walidatory (używane przez argparse jako typ argumentu)
# ---------------------------------------------------------------------------

VALID_INDICATORS = {
    "PM25", "PM10", "NO", "NO2", "NOx", "SO2", "CO", "O3", "C6H6",
    "Pb(PM10)", "Cd(PM10)", "As(PM10)", "Ni(PM10)", "BaP(PM10)",
}

VALID_FREQS = {"1g", "24g"}

def setup_logging() -> None:
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S")
 
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(lambda r: r.levelno < logging.ERROR)
    stdout_handler.setFormatter(fmt)
 
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(fmt)
 
    root = logging.getLogger()
    if root.handlers:
        return
    root.setLevel(logging.DEBUG)
    root.addHandler(stdout_handler)
    root.addHandler(stderr_handler)

# ---------------------------------------------------------------------------
# Walidatory
# ---------------------------------------------------------------------------

def validate_date(value: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Niepoprawna data: '{value}'. Format: RRRR-MM-DD")
 
def validate_indicator(value: str) -> str:
    if value not in VALID_INDICATORS:
        raise argparse.ArgumentTypeError(
            f"Nieznany wskaźnik: '{value}'. Dozwolone: {', '.join(sorted(VALID_INDICATORS))}"
        )
    return value
 
def validate_freq(value: str) -> str:
    if value not in VALID_FREQS:
        raise argparse.ArgumentTypeError(
            f"Nieznana częstotliwość: '{value}'. Dozwolone: {', '.join(sorted(VALID_FREQS))}"
        )
    return value

# ---------------------------------------------------------------------------
# Helper – szuka pliku pomiarowego przez group_measurement_files_by_key
# ---------------------------------------------------------------------------
 
def find_measurement_file(indicator: str, freq: str) -> Path:
    files = group_measurement_files_by_key(MEASUREMENTS_DIR)
    key   = next((k for k in files if k[1] == indicator and k[2] == freq), None)
    if key is None:
        logging.warning(f"Brak pliku pomiarowego dla wskaźnika={indicator}, freq={freq}")
        raise FileNotFoundError(f"Nie znaleziono pliku: {indicator}_{freq}.csv")
    return files[key]

# ---------------------------------------------------------------------------
# Podkomendy
# ---------------------------------------------------------------------------

def cmd_random_station(args: argparse.Namespace) -> None:
    chosen = get_random_active_station(
        find_measurement_file(args.indicator, args.freq),
        STATIONS_FILE, args.start, args.end
    )
    print("=" * 55)
    print(f"Kod stacji : {chosen.get('Kod stacji', '').strip()}")
    print(f"Nazwa      : {chosen.get('Nazwa stacji', '').strip()}")
    print(f"Adres      : {chosen.get('Adres', '').strip()}")
    print(f"Miejscowość: {chosen.get('Miejscowość', '').strip()}")
    print(f"Województwo: {chosen.get('Województwo', '').strip()}")
    print("=" * 55)
 
def cmd_stats(args: argparse.Namespace) -> None:
    mean, std_dev, n = calculate_station_stats(
        find_measurement_file(args.indicator, args.freq),
        args.station, args.start, args.end
    )
    print("=" * 55)
    print(f"Stacja    : {args.station}  [{args.indicator}, {args.freq}]")
    print(f"Okres     : {args.start.date()} – {args.end.date()}")
    print(f"Pomiary   : {n}")
    print(f"Średnia   : {mean:.4f} µg/m³")
    print(f"Std. odch.: {std_dev:.4f} µg/m³")
    print("=" * 55)


# ---------------------------------------------------------------------------
# Parser
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
    setup_logging()
    parser = build_parser()
    args   = parser.parse_args()
 
    if args.start > args.end:
        parser.error(f"Data początkowa ({args.start.date()}) późniejsza od końcowej ({args.end.date()}).")
 
    try:
        {"random-station": cmd_random_station, "stats": cmd_stats}[args.command](args)
    except FileNotFoundError as e:
        logging.error(e)
        sys.exit(1)
    except ValueError as e:
        logging.warning(e)
 
 
if __name__ == "__main__":
    main()