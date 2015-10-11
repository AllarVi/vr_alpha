__author__ = 'Mart'

START_CHAR_ASCII_CODE = 32
END_CHAR_ASCII_CODE = 126

#TODO: ATM it returns ranges where there are wildcards also included
# (etc: wildcard = _ and it returns a_b___ though pos1 is not a wildcard

def get_range(index, wildcard):
    """Returns range according to int index and wildcard. Ranges are """
    wildcard_string = str(wildcard)
    wildcard_ascii_index = ord(wildcard)
    number_of_chars = END_CHAR_ASCII_CODE - START_CHAR_ASCII_CODE + 1
    if START_CHAR_ASCII_CODE <= wildcard_ascii_index <= END_CHAR_ASCII_CODE:
        number_of_chars -= 1

    # ? and ?? and ???
    if index is 0:
        range1 = wildcard_string
        range2 = wildcard_string + wildcard_string
        range3 = wildcard_string + wildcard_string + wildcard_string
        return [range1, range2, range3]
    # a???, b???, c??? and d??? and so on.
    elif index <= number_of_chars:
        return [get_char(int(START_CHAR_ASCII_CODE + (index - 1)), wildcard_ascii_index) +
                wildcard_string + wildcard_string + wildcard_string]
    # aa???, ab???, ac???, ad???, ...
    elif index <= (number_of_chars**2 + number_of_chars):
        operator = index - number_of_chars - 1
        return [get_char(START_CHAR_ASCII_CODE + int(operator / number_of_chars), wildcard_ascii_index)
               + get_char(START_CHAR_ASCII_CODE + operator % number_of_chars ,wildcard_ascii_index) +
                wildcard_string + wildcard_string + wildcard_string]
    # aaa???, aab???, aac???, ...
    elif index <= (number_of_chars**3 + (number_of_chars**2 + number_of_chars)):
        operator = index - (number_of_chars**2 + number_of_chars) - 1
        return [get_char(START_CHAR_ASCII_CODE + int(operator / number_of_chars**2), wildcard_ascii_index) +
                get_char(START_CHAR_ASCII_CODE + int(operator / number_of_chars) % number_of_chars, wildcard_ascii_index) +
                get_char(START_CHAR_ASCII_CODE + operator % (number_of_chars), wildcard_ascii_index) +
                wildcard_string + wildcard_string + wildcard_string]
    # aaa????, aab????, aac????, aad????, ...
    elif index <= number_of_chars**3 + (number_of_chars**3 + (number_of_chars**2 + number_of_chars)):
        indexer = 1
    # aaa?????, aab?????, aac?????, aad?????, ...
    elif index <= number_of_chars**3 + (number_of_chars**3 + (number_of_chars**3 + (number_of_chars**2 + number_of_chars))):
        indexer = 2
    # aaa??????, aab??????, aac??????, aad??????, ...
    elif index <= number_of_chars**3 + number_of_chars**3 + (number_of_chars**3 + (number_of_chars**3 + (number_of_chars**2 + number_of_chars))):
        indexer = 3
    else:
        return []

    operator = index - (indexer * number_of_chars**3 + number_of_chars**2 + number_of_chars) - 1
    return [get_char(START_CHAR_ASCII_CODE + int(operator / number_of_chars**2) % number_of_chars, wildcard_ascii_index) +
            get_char(START_CHAR_ASCII_CODE + int(operator / number_of_chars) % number_of_chars, wildcard_ascii_index) +
            get_char(START_CHAR_ASCII_CODE + operator % (number_of_chars), wildcard_ascii_index) +
            wildcard_string * (3 + indexer)]


def get_ranges(startindex, lastindex, wildcard):
    """Returns multiple ranges in an array"""
    i = startindex
    ranges = []
    while i <= lastindex:
        ranges += get_range(i,wildcard)
        i += 1
    return ranges


def get_char(char_ascii_code, wildcard_ascii_code):
    """Returns character after checking that said char is not a wildcard."""
    # Wildcard comes after char or wildcard before range begins
    if char_ascii_code < wildcard_ascii_code or wildcard_ascii_code < START_CHAR_ASCII_CODE:
        return chr(char_ascii_code)
    # Char between wildcard and end. Cannot be equal because of +1, would be out of range.
    elif char_ascii_code < END_CHAR_ASCII_CODE:
        return chr(char_ascii_code + 1)
    else:
        # workaround for char_ascii_code == END_CHAR_ASCII_CODE + 1,
        # at least makes sure that no wildcard is inserted.
        # Actual code should never enter here.
        print("Error: OUT_OF_RANGE vra_range_generator.get_char()")
        if wildcard_ascii_code is not ord("Z"):
            return "Z"
        else:
            return "z"
