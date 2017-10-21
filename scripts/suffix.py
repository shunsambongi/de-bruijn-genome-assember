def suffix(text):
    if isinstance(text, tuple):
        return tuple((suffix(x) for x in text))
    return text[1:]
