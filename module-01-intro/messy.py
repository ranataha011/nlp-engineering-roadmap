def count_words(filename):
    with open(filename, "r") as f:
        text = f.read()
    words = text.split()
    d = {}
    for w in words:
        if w in d:
            d[w] = d[w] + 1
        else:
            d[w] = 1
    return d


x = count_words("sample.txt")
print(x)
