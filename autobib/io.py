def parse(string):
    is_key = False
    result = {}
    start_entry = 0
    start_key = 0
    stop_key = 0
    braces = 0
    for i, c in enumerate(string):
        if braces == 0:
            if c == "@":
                start_entry = i
                continue
            if c == "{":
                start_key = i + 1
                is_key = True
                braces += 1
                continue
        if is_key and c == ",":
            stop_key = i
            is_key = False
            continue
        if c == "{":
            braces += 1
        if c == "}":
            braces -= 1
            if braces == 0:
                key = string[start_key:stop_key]
                result[key] = string[start_entry : i + 1]
    return result
