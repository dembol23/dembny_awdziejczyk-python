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
def parse_measurements_data(
    path: Path,
    target_station: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Plik nie istnieje: {path}")

    logger.info(f"Otwieranie pliku: {path.name}")
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    logger.info(f"Zamknięto plik: {path.name} – wczytano {len(rows)} wierszy")

    if len(rows) < 7:
        logger.error(f"Plik {path.name} jest uszkodzony lub zbyt krótki (brak nagłówków).")
        return []

    station_codes = [s.strip() for s in rows[1][1:]]
    indicators    = rows[2][1:]
    frequencies   = rows[3][1:]
    units         = rows[4][1:]

    # Wczesne wyszukanie indeksu stacji – O(k) tylko raz, nie k razy per wiersz
    target_idx: int | None = None
    if target_station is not None:
        try:
            target_idx = station_codes.index(target_station.strip())
        except ValueError:
            logger.warning(f"Stacja '{target_station}' nie istnieje w pliku {path.name}")
            return []

    records = []
    for row in rows[6:]:
        if not row or not row[0]:
            continue

        timestamp = datetime.strptime(row[0], "%m/%d/%y %H:%M")

        # Wczesne odrzucenie całego wiersza po dacie
        if start_date is not None and timestamp < start_date:
            continue
        if end_date is not None and timestamp > end_date:
            continue

        logger.debug(f"Wczytano wiersz: {sum(len(c.encode('utf-8')) for c in row)} bajtów")

        if target_idx is not None:
            # Ścieżka szybka – tylko jedna kolumna
            raw_val = row[target_idx + 1] if target_idx + 1 < len(row) else ""
            if raw_val:
                try:
                    records.append({
                        "timestamp": timestamp,
                        "station":   station_codes[target_idx],
                        "indicator": indicators[target_idx],
                        "frequency": frequencies[target_idx],
                        "unit":      units[target_idx],
                        "value":     float(raw_val.replace(',', '.')),
                    })
                except ValueError:
                    pass
        else:
            # Ścieżka pełna – wszystkie kolumny
            for i, raw_val in enumerate(row[1:]):
                if not raw_val or i >= len(station_codes):
                    continue
                try:
                    records.append({
                        "timestamp": timestamp,
                        "station":   station_codes[i],
                        "indicator": indicators[i],
                        "frequency": frequencies[i],
                        "unit":      units[i],
                        "value":     float(raw_val.replace(',', '.')),
                    })
                except ValueError:
                    continue

    return records


# Zadanie 2 - grupowanie plików pomiarowych po kluczu (rok, wskaźnik, częstotliwość)
def group_measurement_files_by_key(path: Path) -> dict[tuple, Path]:
    if not path.exists():
        raise FileNotFoundError(f"Ścieżka nie istnieje: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"Oczekiwano katalogu, nie pliku: {path}")

    pattern = re.compile(r'^(\d{4})_([^_]+)_([^_]+)\.csv$')
    result = {}
    # path.glob("*.csv") zwraca od razu obiekty Path i nie zagląda do podkatalogów
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
        if station.get("Miejscowość", "").strip().lower() == city.lower():
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