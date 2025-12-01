
def convert_string_to_ascii_binary_hex(input_string):
    ascii_codes = [ord(char) for char in input_string]
    binary_codes = [bin(ord(char))[2:].zfill(8) for char in input_string]
    hex_codes = [hex(ord(char))[2:].upper().zfill(2) for char in input_string]
    return ascii_codes, binary_codes, hex_codes


def convert_ascii_to_string(ascii_codes):
    try:
        return "".join(chr(int(code)) for code in ascii_codes)
    except ValueError:
        return None


def convert_binary_to_string(binary_codes):
    try:
        return "".join(chr(int(code, 2)) for code in binary_codes)
    except ValueError:
        return None


def convert_hex_to_string(hex_codes):
    try:
        return "".join(chr(int(code, 16)) for code in hex_codes)
    except ValueError:
        return None
