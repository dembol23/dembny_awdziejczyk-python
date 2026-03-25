from read_log import read_log
from print import print_dict_entry_dates
from transform import entry_to_dict, log_to_dict
from filter import (get_entries_by_code, get_entries_by_addr,
                    get_failed_reads, get_entries_by_extension,
                    get_top_ips, get_top_uris, get_unique_methods,
                    get_entries_in_time_range)
from count import count_by_method, count_status_classes
from sort import sort_log
from analyze import (analyze_log, get_session_paths,
                    get_extension_stats, detect_sus)
from datetime import datetime

def separator(title):
    print(f"\n{'='*10} {title} {'='*10}")

def main():
    logi = read_log()
    log_dict = log_to_dict(logi)

    separator("Zad 1 - read_log")
    print(f"Wczytano {len(logi)} logów")
    print(f"Przykładowy wpis: {logi[0]}")

    separator("Zad 2 - sort_log")
    print("Po timestamp:", sort_log(logi, 0)[0][0])
    print("Po statusie:", sort_log(logi, 9)[0][9])
    print("Błędny indeks:", sort_log(logi, 99))

    separator("Zad 3 - get_entries_by_code")
    print("404:", len(get_entries_by_code(logi, 404)))
    print("200:", len(get_entries_by_code(logi, 200)))

    separator("Zad 4 - get_entries_by_addr")
    print("Po IP:", len(get_entries_by_addr(logi, '192.168.202.79')))
    print("Po hoście:", len(get_entries_by_addr(logi, '192.168.229.251')))

    separator("Zad 5 - get_failed_reads")
    a, b = get_failed_reads(logi)
    print(f"4xx: {len(a)}, 5xx: {len(b)}")
    print(f"merge=True: {len(get_failed_reads(logi, merge=True))}")

    separator("Zad 6 - get_entries_by_extension")
    print("nsf:", len(get_entries_by_extension(logi, 'nsf')))
    print("jpg:", len(get_entries_by_extension(logi, 'jpg')))

    separator("Zad 7 - get_top_ips")
    print(get_top_ips(logi, n=3))

    separator("Zad 8 - get_unique_methods")
    print(get_unique_methods(logi))

    separator("Zad 9 - get_entries_in_time_range")
    start = datetime(2012, 3, 16, 12, 30, 0)
    end   = datetime(2012, 3, 16, 12, 31, 0)
    print(f"W zakresie: {len(get_entries_in_time_range(logi, start, end))}")

    separator("Zad 10 - count_by_method")
    print(count_by_method(logi))

    separator("Zad 11 - get_top_uris")
    print(get_top_uris(logi, n=3))

    separator("Zad 12 - count_status_classes")
    print(count_status_classes(logi))

    separator("Zad 13 - entry_to_dict")
    print(entry_to_dict(logi[0]))

    separator("Zad 14 - log_to_dict")
    print(f"Sesji: {len(log_dict)}")
    sample = list(log_dict.items())[0]
    print(f"Przykład uid: {sample[0]}, wpisy: {len(sample[1])}")

    separator("Zad 15 - print_dict_entry_dates")
    first_uid = list(log_dict.keys())[0]
    print_dict_entry_dates({first_uid: log_dict[first_uid]})

    separator("Zad 16 - najaktywniejsza sesja")
    top_uid = max(log_dict, key=lambda uid: len(log_dict[uid]))
    print(f"UID: {top_uid}, żądań: {len(log_dict[top_uid])}")

    separator("Zad 17 - get_session_paths")
    paths = get_session_paths(logi)
    sample = list(paths.items())[0]
    print(f"UID: {sample[0]}, ścieżki: {sample[1]}")

    separator("Zad 18 - detect_sus")
    print(detect_sus(logi, threshold=5))

    separator("Zad 19 - get_extension_stats")
    print(get_extension_stats(logi))

    separator("Zad 20 - analyze_log")
    result = analyze_log(logi)
    for k, v in result.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()