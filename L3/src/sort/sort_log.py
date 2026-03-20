def sort_log(log, index):
    try:
        if not isinstance(index, int) or index < 0 or index > 9:
            raise IndexError("Invalid index")
        return sorted(log, key=lambda row:row[index])

    except IndexError as e:
        print(e)
        return log

if __name__ == "__main__":
    sort_log([], 0)