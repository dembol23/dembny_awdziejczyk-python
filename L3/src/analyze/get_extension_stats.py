from collections import Counter

def get_extension_stats(log):
    extensions = []
    for entry in log:
        path = entry[8].split("?")[0]
        filename = path.split("/")[-1]
        if "." in filename:
            #   rsplit - works like string.split(), but:
            #   1) splits from the right side
            #   2) conducts as many splits as specified in second argument
            extensions.append(filename.rsplit(".", 1)[1].lower())
    return dict(Counter(extensions))