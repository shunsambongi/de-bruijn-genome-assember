def prefix(text):
    if isinstance(text, tuple):
        return tuple((prefix(x) for x in text))
    return text[:-1]
