import sys
from pathlib import Path
from datetime import datetime

# ── Ścieżki ───────────────────────────────────────────────────────────────────
BASE_DIR         = Path(__file__).parent.parent
STATIONS_FILE    = BASE_DIR / "data" / "stacje.csv"
MEASUREMENTS_DIR = BASE_DIR / "data" / "measurements"

# ── Importy z projektu ────────────────────────────────────────────────────────
from data_parser import (
    parse_station_metadata,
    parse_measurements_data,
    group_measurement_files_by_key,
    get_addresses,
)
from air_quality_cli import main as cli_main

# ── Helper do wypisywania sekcji ──────────────────────────────────────────────
def header(title: str) -> None:
    print(f"\n{'─'*55}")
    print(f"  {title}")
    print(f"{'─'*55}")

def ok(msg: str)   : print(f"  [OK]   {msg}")
def fail(msg: str) : print(f"  [FAIL] {msg}", file=sys.stderr)

# ── Testy ─────────────────────────────────────────────────────────────────────

def test_parse_station_metadata():
    header("Zad. 1 – parse_station_metadata")
    stations = parse_station_metadata(STATIONS_FILE)
    assert isinstance(stations, list),            "wynik nie jest listą"
    assert len(stations) > 0,                     "lista jest pusta"
    assert "Kod stacji" in stations[0],           "brak klucza 'Kod stacji'"
    assert "Miejscowość" in stations[0],          "brak klucza 'Miejscowość'"
    ok(f"wczytano {len(stations)} stacji")
    ok(f"przykład: {stations[0]['Kod stacji']} – {stations[0]['Nazwa stacji']}")

def test_parse_measurements_data():
    header("Zad. 1 – parse_measurements_data")
    path = MEASUREMENTS_DIR / "2023_PM10_1g.csv"
    records = parse_measurements_data(path)
    assert isinstance(records, list),                "wynik nie jest listą"
    assert len(records) > 0,                         "brak rekordów"
    first = records[0]
    assert "timestamp" in first,                     "brak klucza 'timestamp'"
    assert "station"   in first,                     "brak klucza 'station'"
    assert "value"     in first,                     "brak klucza 'value'"
    assert isinstance(first["timestamp"], datetime), "timestamp nie jest datetime"
    assert isinstance(first["value"],     float),    "value nie jest float"
    ok(f"wczytano {len(records)} rekordów")
    ok(f"przykład: {first['timestamp']}  {first['station']}  {first['value']} {first['unit']}")

def test_group_measurement_files_by_key():
    header("Zad. 2 – group_measurement_files_by_key")
    groups = group_measurement_files_by_key(MEASUREMENTS_DIR)
    assert isinstance(groups, dict), "wynik nie jest słownikiem"
    assert len(groups) > 0,          "brak plików"
    key, path = next(iter(groups.items()))
    assert len(key) == 3,            "klucz nie jest trójką"
    assert path.exists(),            "ścieżka nie istnieje"
    ok(f"znaleziono {len(groups)} plików pomiarowych")
    for (rok, wsk, czas), p in groups.items():
        ok(f"  ({rok}, {wsk:8}, {czas}) => {p.name}")

def test_get_addresses():
    header("Zad. 3 – get_addresses")
    city  = "Wrocław"
    addrs = get_addresses(STATIONS_FILE, city)
    assert isinstance(addrs, list), "wynik nie jest listą"
    assert len(addrs) > 0,          f"brak stacji w: {city}"
    for woj, miasto, ulica, numer in addrs:
        assert miasto.lower() == city.lower(), f"zły filtr – '{miasto}'"
        ok(f"  {woj} | {miasto} | {ulica} | nr: {numer}")

def test_cli_stats():
    header("Zad. 5 – CLI: stats")
    sys.argv = [
        "air_quality_cli.py",
        "--indicator", "PM10",
        "--freq",      "1g",
        "--start",     "2023-01-01",
        "--end",       "2023-01-07",
        "stats",
        "--station",   "DsWrocWybCon",
    ]
    cli_main()

def test_cli_random_station():
    header("Zad. 5 – CLI: random-station")
    sys.argv = [
        "air_quality_cli.py",
        "--indicator", "PM10",
        "--freq",      "1g",
        "--start",     "2023-01-01",
        "--end",       "2023-01-07",
        "random-station",
    ]
    cli_main()

def test_cli_bad_date():
    header("Zad. 5 – CLI: walidacja złej daty")
    sys.argv = [
        "air_quality_cli.py",
        "--indicator", "PM10",
        "--freq",      "1g",
        "--start",     "01/01/2023",   # zły format – powinien odrzucić
        "--end",       "2023-01-07",
        "random-station",
    ]
    try:
        cli_main()
        fail("powinien był odrzucić złą datę!")
    except SystemExit as e:
        ok(f"poprawnie odrzucono złą datę (SystemExit kod: {e.code})")

def test_cli_bad_indicator():
    header("Zad. 5 – CLI: walidacja złego wskaźnika")
    sys.argv = [
        "air_quality_cli.py",
        "--indicator", "SMOG",         # nieznany wskaźnik
        "--freq",      "1g",
        "--start",     "2023-01-01",
        "--end",       "2023-01-07",
        "random-station",
    ]
    try:
        cli_main()
        fail("powinien był odrzucić nieznany wskaźnik!")
    except SystemExit as e:
        ok(f"poprawnie odrzucono zły wskaźnik (SystemExit kod: {e.code})")

# ── Uruchomienie ──────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  TESTY PROJEKTU – Laboratorium 5")
    print("=" * 55)

    tests = [
        test_parse_station_metadata,
        test_parse_measurements_data,
        test_group_measurement_files_by_key,
        test_get_addresses,
        test_cli_stats,
        test_cli_random_station,
        test_cli_bad_date,
        test_cli_bad_indicator,
    ]

    passed = failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except (AssertionError, Exception) as e:
            fail(f"{test.__name__}: {e}")
            failed += 1

    print(f"\n{'='*55}")
    print(f"  Wynik: {passed} OK  |  {failed} FAILED")
    print(f"{'='*55}\n")

if __name__ == "__main__":
    main()