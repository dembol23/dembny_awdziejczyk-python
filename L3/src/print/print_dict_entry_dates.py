from collections import Counter
from count.count_by_method import count_by_method
from count.count_status_classes import count_status_classes
from transform.dict_to_entry import dict_to_entry


def print_dict_entry_dates(log_dict):
    for uid, entries in log_dict.items():
        if not entries:
            continue

        tuples = [dict_to_entry(e) for e in entries]
        total = len(entries)

        ips = set(e.get("orig_h") for e in entries if e.get("orig_h"))
        hosts = set(e.get("host") for e in entries if e.get("host"))
        adresy_hosty = f"IP: {', '.join(ips)} / Hosty: {', '.join(hosts)}"

        timestamps = [e.get("ts") for e in entries if e.get("ts")]
        first_date = min(timestamps) if timestamps else "Brak"
        last_date = max(timestamps) if timestamps else "Brak"

        method_counts = count_by_method(tuples)
        status_classes = count_status_classes(tuples)
        count_2xx = status_classes.get("2xx", 0)

        print(f"=== Sesja {uid} ===")
        print(f"- Adresy IP / hosty: {adresy_hosty}")
        print(f"- Liczba żądań: {total}")
        print(f"- Data pierwszego żądania: {first_date}")
        print(f"- Data ostatniego żądania: {last_date}")

        print("- Procentowy udział metod HTTP:")
        for method, count in method_counts.items():
            pct = (count / total) * 100
            print(f"    * {method}: {pct:.1f}%")

        print(f"- Stosunek liczby kodów 2xx do wszystkich: {count_2xx}/{total}")
        print()