import random
import math
from pathlib import Path
from datetime import datetime
from data_parser import parse_station_metadata, parse_measurements_data
import logging
logger = logging.getLogger(__name__)

def get_random_active_station(measurement_path: Path, stations_path: Path, start: datetime, end: datetime) -> dict:
    records = parse_measurements_data(measurement_path)
    
    # Zbieramy kody stacji, które mają chociaż jeden pomiar w zadanym czasie
    active_codes = {
        rec["station"] for rec in records 
        if start <= rec["timestamp"] <= end
    }
    
    if not active_codes:
        raise ValueError("Brak danych pomiarowych w podanym przedziale czasowym.")

    stations = parse_station_metadata(stations_path)
    matching_stations = [s for s in stations if s.get("Kod stacji", "") in active_codes]

    if not matching_stations:
        raise ValueError("Nie znaleziono metadanych dla żadnej aktywnej stacji.")

    return random.choice(matching_stations)

def calculate_station_stats(measurement_path: Path, target_station: str, start: datetime, end: datetime) -> tuple[float, float, int]:
    records = parse_measurements_data(measurement_path)
    
    # Wyciągamy same wartości liczbowe dla konkretnej stacji w danym czasie
    values = [
        rec["value"] for rec in records 
        if rec["station"] == target_station and start <= rec["timestamp"] <= end
    ]

    if not values:
        raise ValueError(f"Stacja '{target_station}' nie posiada żadnych pomiarów w podanym przedziale.")

    n = len(values)
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / n
    std_dev = math.sqrt(variance)

    return mean, std_dev, n