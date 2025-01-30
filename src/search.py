import re

def search_in_data(data, pattern):
    try:
        compiled_pattern = re.compile(pattern)
        return [match.start() for match in compiled_pattern.finditer(data)]
    except re.error:
        return []
