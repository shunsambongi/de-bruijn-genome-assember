def string_from_path(path):
    text = path[0]
    for kmer in path[1:]:
        if isinstance(kmer, tuple):
            pair = tuple((string_from_path([text[i], x]) for i, x in enumerate(kmer)))
            text = pair
        else:
            text += kmer[-1]
    return text
