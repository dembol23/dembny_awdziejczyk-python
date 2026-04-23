import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer

from air_quality_stats import get_random_active_station, calculate_station_stats
from data_parser import group_measurement_files_by_key

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Stałe
# ---------------------------------------------------------------------------

BASE_DIR         = Path(__file__).parent.parent
STATIONS_FILE    = BASE_DIR / "data" / "stacje.csv"
MEASUREMENTS_DIR = BASE_DIR / "data" / "measurements"

# ---------------------------------------------------------------------------
# Stałe wskaźników i częstotliwości
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

def find_measurement_file(indicator: str, freq: str) -> Path:
    files = group_measurement_files_by_key(MEASUREMENTS_DIR)
    matches = sorted(
        [k for k in files if k[1] == indicator and k[2] == freq],
        key=lambda k: k[0],
        reverse=True,
    )
    if not matches:
        logger.warning(f"Brak pliku pomiarowego dla wskaźnika={indicator}, freq={freq}")
        raise FileNotFoundError(
            f"Brak pliku pomiarowego dla wskaźnika={indicator}, częstotliwości={freq}."
        )
    return files[matches[0]]

app = typer.Typer(
    name="air_quality_cli",
    help=(
        "Narzędzie do analizy danych jakości powietrza.\n\n"
        "Dane: stacje.csv + measurements/<wskaźnik>_<częstotliwość>.csv"
    ),
    no_args_is_help=True,
)

IndicatorArg = Annotated[
    str,
    typer.Option(
        "--indicator",
        help=(
            f"Mierzona wielkość, np. PM10, PM25, NO2. "
            f"Dozwolone: {', '.join(sorted(VALID_INDICATORS))}"
        ),
        metavar="WSKAŹNIK",
    ),
]

FreqArg = Annotated[
    str,
    typer.Option(
        "--freq",
        help="Czas uśredniania pomiaru: 1g (1 godzina) lub 24g (24 godziny).",
        metavar="CZĘSTOTLIWOŚĆ",
    ),
]

StartArg = Annotated[
    str,
    typer.Option(
        "--start",
        help="Początek przedziału czasowego (format: RRRR-MM-DD).",
        metavar="RRRR-MM-DD",
    ),
]

EndArg = Annotated[
    str,
    typer.Option(
        "--end",
        help="Koniec przedziału czasowego (format: RRRR-MM-DD).",
        metavar="RRRR-MM-DD",
    ),
]

def parse_date(value: str, param_name: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise typer.BadParameter(
            f"Niepoprawna data: '{value}'. Format: RRRR-MM-DD",
            param_hint=f"'--{param_name}'",
        )

def validate_indicator_value(indicator: str) -> str:
    if indicator not in VALID_INDICATORS:
        raise typer.BadParameter(
            f"Nieznany wskaźnik: '{indicator}'. Dozwolone: {', '.join(sorted(VALID_INDICATORS))}",
            param_hint="'--indicator'",
        )
    return indicator

def validate_freq_value(freq: str) -> str:
    if freq not in VALID_FREQS:
        raise typer.BadParameter(
            f"Nieznana częstotliwość: '{freq}'. Dozwolone: {', '.join(sorted(VALID_FREQS))}",
            param_hint="'--freq'",
        )
    return freq

@app.command()
def random_station(
    indicator: IndicatorArg,
    freq: FreqArg,
    start: StartArg,
    end: EndArg,
) -> None:
    """Wypisz nazwę i adres losowej stacji mierzącej podany wskaźnik w zadanym przedziale czasowym."""
    indicator = validate_indicator_value(indicator)
    freq      = validate_freq_value(freq)
    start_dt  = parse_date(start, "start")
    end_dt    = parse_date(end, "end")

    if start_dt > end_dt:
        typer.echo(
            f"Błąd: Data początkowa ({start_dt.date()}) późniejsza od końcowej ({end_dt.date()}).",
            err=True,
        )
        raise typer.Exit(code=2)

    try:
        chosen = get_random_active_station(
            find_measurement_file(indicator, freq),
            STATIONS_FILE, start_dt, end_dt,
        )
    except FileNotFoundError as e:
        logging.error(e)
        raise typer.Exit(code=1)
    except ValueError as e:
        logging.warning(e)
        raise typer.Exit(code=2)

    print("=" * 55)
    print(f"Kod stacji : {chosen.get('Kod stacji', '').strip()}")
    print(f"Nazwa      : {chosen.get('Nazwa stacji', '').strip()}")
    print(f"Adres      : {chosen.get('Adres', '').strip()}")
    print(f"Miejscowość: {chosen.get('Miejscowość', '').strip()}")
    print(f"Województwo: {chosen.get('Województwo', '').strip()}")
    print("=" * 55)


@app.command()
def stats(
    indicator: IndicatorArg,
    freq: FreqArg,
    start: StartArg,
    end: EndArg,
    station: Annotated[
        str,
        # Station is specific to this subcommand so it's defined inline rather
        # than as a shared alias at module level.
        typer.Option("--station", help="Kod stacji, np. DsWrocWybCon.", metavar="KOD_STACJI"),
    ],
) -> None:
    """Oblicz średnią i odchylenie standardowe wskaźnika dla wybranej stacji w zadanym przedziale czasowym."""
    indicator = validate_indicator_value(indicator)
    freq      = validate_freq_value(freq)
    start_dt  = parse_date(start, "start")
    end_dt    = parse_date(end, "end")

    if start_dt > end_dt:
        typer.echo(
            f"Błąd: Data początkowa ({start_dt.date()}) późniejsza od końcowej ({end_dt.date()}).",
            err=True,
        )
        raise typer.Exit(code=2)

    try:
        mean, std_dev, n = calculate_station_stats(
            find_measurement_file(indicator, freq),
            station, start_dt, end_dt,
        )
    except FileNotFoundError as e:
        logging.error(e)
        raise typer.Exit(code=1)
    except ValueError as e:
        logging.warning(e)
        raise typer.Exit(code=2)

    print("=" * 55)
    print(f"Stacja    : {station}  [{indicator}, {freq}]")
    print(f"Okres     : {start_dt.date()} – {end_dt.date()}")
    print(f"Pomiary   : {n}")
    print(f"Średnia   : {mean:.4f} µg/m³")
    print(f"Std. odch.: {std_dev:.4f} µg/m³")
    print("=" * 55)

def main() -> None:
    app()

# pip install typer or
# uv venv
# uv pip install typer
# uv install - curl -LsSf https://astral.sh/uv/install.sh | sh

if __name__ == "__main__":
    main()