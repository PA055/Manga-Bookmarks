import re


def clean_float(f):
    if not str(f)[:].replace('.', '').isnumeric():
        return f
    return int(f) if float(f) == int(f) else float(f)


def get_chapter_number(text):
    for i in range(len(text)):
        if text[i:].replace('.', '').isnumeric():
            return float(text[i:])
    return 0

def get_numbers(text):
    return float(re.search('\d+\.?\d*', text).group())


def clean_up(f):
    if '-page-' in str(f) and '.html' in str(f):
        idx = f.find('-page-')
        return f[:idx] + f[-5:]
    return f


def get_host(url):
    return '/'.join(url.split('/')[:3])
