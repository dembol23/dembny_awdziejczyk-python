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
            # "archive.tar.gz".split(".", 1)[1]    'tar.gz'  ← od lewej, za dużo
            # "archive.tar.gz".rsplit(".", 1)[1]   'gz'      ← od prawej, tylko rozszerzenie
            extensions.append(filename.rsplit(".", 1)[1].lower())
    return dict(Counter(extensions))