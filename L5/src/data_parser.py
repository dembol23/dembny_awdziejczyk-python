from pathlib import Path
import csv, re
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

# Zadanie 1 - parsowanie metadanych stacji
def parse_station_metadata(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Plik nie istnieje: {path}")
    logger.info(f"Otwieranie pliku: {path.name}")
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        result = list(reader)
    logger.info(f"Zamknięto plik: {path.name} – wczytano {len(result)} rekordów")
    return result


# Zadanie 1 - parsowanie pliku pomiarowego
def parse_measurements_data(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Plik nie istnieje: {path}")
    
    logger.info(f"Otwieranie pliku: {path.name}")
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)          # <-- reader, nie DictReader
        rows = list(reader)
    logger.info(f"Zamknięto plik: {path.name} – wczytano {len(rows)} wierszy")

    station_codes = rows[1][1:]         # wiersz 2: kody stacji
    indicators    = rows[2][1:]         # wiersz 3: wskaźniki (PM10, ...)
    frequencies   = rows[3][1:]         # wiersz 4: czas uśredniania
    units         = rows[4][1:]         # wiersz 5: jednostki

    records = []
    for row in rows[6:]:                # dane od wiersza 7 (index 6)
        if not row or not row[0]:
            continue
        logger.debug(f"Wczytano wiersz: {sum(len(c) for c in row)} bajtów")
        timestamp = datetime.strptime(row[0], "%m/%d/%y %H:%M")

        for i, raw_val in enumerate(row[1:]):
            if not raw_val:
                continue
            try:
                value = float(raw_val.replace(',', '.'))
            except ValueError:
                continue

            records.append({
                "timestamp": timestamp,
                "station":   station_codes[i],
                "indicator": indicators[i],
                "frequency": frequencies[i],
                "unit":      units[i],
                "value":     value,
            })

    return records


# Zadanie 2 - grupowanie plików pomiarowych po kluczu (rok, wskaźnik, częstotliwość)
def group_measurement_files_by_key(path: Path) -> dict[tuple, Path]:
    if not path.exists():
        raise FileNotFoundError(f"Ścieżka nie istnieje: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"Oczekiwano katalogu, nie pliku: {path}")

    pattern = re.compile(r'^(\d{4})_([^_]+)_([^_]+)\.csv$')
    result = {}
    for file in path.glob("*.csv"):
        match = pattern.match(file.name)
        if match:
            result[(match.group(1), match.group(2), match.group(3))] = file
    return result

def get_addresses(path: Path, city: str) -> list[tuple]:
    res = parse_station_metadata(path)
    addr_pattern = re.compile(r'^(.*?)\s+(\d+\w*)$')
    result = []
    for station in res:
        if station.get("Województwo", "").lower() == city.lower():
            addr  = station.get("Adres", "").strip()
            match = addr_pattern.match(addr)
            if match:
                ulica, numer = match.group(1), match.group(2)
            else:
                ulica, numer = addr, None
            result.append((
                station.get("Województwo", ""),
                station.get("Miejscowość", ""),
                ulica,
                numer 
            ))
    if not result:
        logger.warning(f"Nie znaleziono stacji w miejscowości: {city!r}")
    return result