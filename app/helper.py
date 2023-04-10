def clean_float(f):
    if not str(f)[:].replace('.', '').isnumeric():
        return f
    return int(f) if float(f) == int(f) else float(f)

def get_chapter_number(text):
    for i in range(len(text)):
        if text[i:].replace('.', '').isnumeric():
            return float(text[i:])
    return 0
