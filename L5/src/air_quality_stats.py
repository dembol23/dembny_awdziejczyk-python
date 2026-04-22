import random
import statistics
from pathlib import Path
from datetime import datetime
from data_parser import parse_station_metadata, parse_measurements_data
import logging
logger = logging.getLogger(__name__)

def get_random_active_station(measurement_path: Path, stations_path: Path, start: datetime, end: datetime) -> dict:
    records = parse_measurements_data(measurement_path, start_date=start, end_date=end)
    active_codes = {rec["station"] for rec in records}
    
    if not active_codes:
        logger.warning("Brak danych pomiarowych w podanym przedziale czasowym.")
        raise ValueError("Brak danych pomiarowych w podanym przedziale czasowym.")

    stations = parse_station_metadata(stations_path)
    matching_stations = [s for s in stations if s.get("Kod stacji", "").strip() in active_codes]

    if not matching_stations:
        logger.warning("Znaleziono pomiary, ale brak pasujących metadanych stacji.")
        raise ValueError("Nie znaleziono metadanych dla żadnej aktywnej stacji.")

    return random.choice(matching_stations)

def calculate_station_stats(measurement_path: Path, target_station: str, start: datetime, end: datetime) -> tuple[float, float, int]:
    records = parse_measurements_data(
        measurement_path,
        target_station=target_station,
        start_date=start,
        end_date=end,
    )
    values = [rec["value"] for rec in records]

    if not values:
        logger.warning("Brak danych pomiarowych w podanym przedziale czasowym.")
        raise ValueError(f"Stacja '{target_station}' nie posiada żadnych pomiarów w podanym przedziale.")

    if len(values) < 2:
        logger.warning(f"Za mało pomiarów dla stacji '{target_station}' – odchylenie standardowe niemożliwe do obliczenia (n={len(values)}).")
        raise ValueError(f"Za mało pomiarów (n={len(values)}) – do obliczenia odchylenia standardowego potrzeba co najmniej 2.")

    mean = statistics.mean(values)
    std_dev = statistics.stdev(values)
    n = len(values)

    return mean, std_dev, n