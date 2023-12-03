def convert(x, base):
    if type(x) is not int:
        raise TypeError("x is not an integer")
    if type(base) is not int:
        raise TypeError("base is not an integer")
    if x < 0:
        raise ValueError("x must be positive")
    if base < 2:
        raise ValueError("base cannot be less than 2")
    coefficients = []
    while x > 0:
        remainder = x % base
        x = x // base
        coefficients.append(remainder)
        
    return coefficients[::-1]

def hexstring(x):
    coefficients = convert(x, 16)
    hex_string = ''.join(str(c) if c < 10 else chr(c + 55) for c in coefficients)
    hex_string = '0x' + hex_string
    return hex_string

def decodedate(x):
    month = ((x & 0xF0000000) >> 28 ) + 1
    day = ((x & 0x0F800000) >> 23) + 1
    year = (x & 0x007FFFFF)
    date_string = f'{day}.{month}.{year}'
    return date_string

def encodedate(day, month, year):
    if day < 1 or day > 31:
        raise ValueError("Invalid day")
    if month < 1 or month > 12:
        raise ValueError("Invalid month")
    if year < 0 or year >= (2**23):
        raise ValueError("Invalid year")
    month_bits = ((month - 1) & 0xF) << 28
    day_bits = ((day - 1) & 0x1F) << 23
    year_bits = (year & 0x7FFFFF)
    date = month_bits | day_bits | year_bits
    return date

print(encodedate(5,5,2017))
