import re

def findall_in_file(file_name: str, pattern: str):
    pattern = re.compile(pattern)
    with open(file_name, 'r') as f:
        return [match for line in f for match in re.findall(pattern, line)]

# 4a - Wyodrębnij wszystkie daty w formacie RRRR-MM-DD (Z danych w kolumnach "Data uruchomienia" i "Data zamknięcia").
def get_dates(csv_file_name: str) -> list[str]:
    date_pattern = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
    return findall_in_file(csv_file_name, date_pattern)


# 4b - Wyciągnij listę szerokości i długości geograficznej z rekordów (np. 50.943245, 4.913327) – liczba dziesiętna z 6 cyframi po kropce.
def get_geo(csv_file_name: str) -> list[str]:
    geo_pattern = r'\d+\.\d{6}'
    return findall_in_file(csv_file_name, geo_pattern)

# 4c - Znajdź stacje o nazwach składających się z dwóch części (zawierających myślnik)
def get_hyphenated_stations(csv_file_name: str) -> list[str]:
    station_pattern = r'[^,-]+ - [^,-]+'
    return findall_in_file(csv_file_name, station_pattern)

# 4d - Zamień w nazwach stacji
# i. spacje na symbol podłogi (“ “ → “_”)
# ii. polskie znaki diakrytyczne na ich odpowiedniki będące literami alfabetu łacińskiego (‘ą” → ‘a’, ‘ć’ → ‘c’, itd.)
def normalize_station_names(csv_file_name: str) -> list[str]:
    diacritics = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
        'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
        'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
        'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z',
    }

    column_pattern = re.compile(r'(?:[^,]*,){3}([^,]+)')
    replace_pattern = re.compile(f"[{''.join(diacritics.keys())} ]")

    result = []
    with open(csv_file_name, 'r') as f:
        next(f)
        next(f)
        for line in f:
            match = re.search(column_pattern, line)
            if not match:
                continue
            name = match.group(1)
            name = re.sub(replace_pattern, lambda m: diacritics.get(m.group(), '_'), name)
            result.append(name)
    return result


# 4e - Sprawdź, czy wszystkie stacje z kodem kończącym się na "MOB" mają rodzaj "mobilna" (48 nie ma)
def verify_mob_stations(csv_file_name: str) -> bool:
    mob_pattern = r'\w+MOB,[^,]*,([^,\n]+)'
    matches = findall_in_file(csv_file_name, mob_pattern)
    return all(station_type.strip() == 'mobilna' for station_type in matches)


# 4f - Wyodrębnij lokalizacje złożone z 3 członów rozdzielonych myślnikiem
def get_three_part_locations(csv_file_name: str) -> list[str]:
    three_part_pattern = r'[^,-]+ - [^,-]+ - [^,-]+'
    return findall_in_file(csv_file_name, three_part_pattern)

# 4g. Znajdź lokalizacje zawierające przecinek i nazwę ulicy (ul.) lub alei (al.).
def get_street_locations(csv_file_name: str) -> list[str]:
    street_pattern = r'([^,\n]+,[^,\n]*(?:ul\.|al\.)[^,\n]+)'
    return findall_in_file(csv_file_name, street_pattern)

# print(normalize_station_names('../data/stacje.csv'))

