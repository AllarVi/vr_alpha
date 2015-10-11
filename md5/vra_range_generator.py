__author__ = 'Mart'

START_CHAR_ASCII_CODE = 32
END_CHAR_ASCII_CODE = 125

#TODO: ATM it returns ranges where there are wildcards also included
# (etc: wildcard = _ and it returns a_b___ though pos1 is not a wildcard

def get_range(index, wildcard):
    wildcard_string = str(wildcard)
    wildcard_ascii_index = ord(wildcard)
    number_of_chars = END_CHAR_ASCII_CODE - START_CHAR_ASCII_CODE + 1

    # ? and ??
    if index is 0:
        range1 = wildcard_string
        range2 = wildcard_string + wildcard_string
        return [range1, range2]
    # a??, b??, c?? and d?? and so on.
    elif index <= number_of_chars:
        return [get_char(int(START_CHAR_ASCII_CODE + (index - 1))) + wildcard_string + wildcard_string]
    # aa??, ab??, ac??, ad??, ...
    # Must iterate elemnr*elemnr times to cover all,
    # but we have already covered number_of_chars times, so add this.
    elif index <= (number_of_chars**2 + number_of_chars):
        operator = index - number_of_chars - 1
        return [get_char(START_CHAR_ASCII_CODE + int(operator / number_of_chars))
               + get_char(START_CHAR_ASCII_CODE + operator % number_of_chars) + wildcard_string + wildcard_string]
    # aaa??, aab??, aac??, ...
    elif index <= (number_of_chars**3 + (number_of_chars**2 + number_of_chars)):
        operator = index - (number_of_chars**2 + number_of_chars) - 1
        return [get_char(START_CHAR_ASCII_CODE + int(operator / number_of_chars**2)) +
                get_char(START_CHAR_ASCII_CODE + int(operator / number_of_chars) % number_of_chars) +
                get_char(START_CHAR_ASCII_CODE + operator % (number_of_chars)) +
                wildcard_string + wildcard_string]
    # aaa???, aab???, aac???, aad???, ...
    elif index <= number_of_chars**3 + (number_of_chars**3 + (number_of_chars**2 + number_of_chars)):
        operator = index - (number_of_chars**2 + number_of_chars) - 1
        return [get_char(START_CHAR_ASCII_CODE + int(operator / number_of_chars**2) % number_of_chars) +
                get_char(START_CHAR_ASCII_CODE + int(operator / number_of_chars) % number_of_chars) +
                get_char(START_CHAR_ASCII_CODE + operator % (number_of_chars)) +
                wildcard_string + wildcard_string + wildcard_string]
    return []


def get_ranges(startindex, lastindex, wildcard):
    i = startindex
    ranges = []
    while i <= lastindex:
        ranges += get_range(i,wildcard)
        print("Ranges(" + str(i) + "): "+ str(get_range(i,wildcard)))
        i += 1
    return ranges


def get_char(char_ascii_code, wildcard_ascii_code):
    if char_ascii_code < wildcard_ascii_code:
        return chr(char_ascii_code)
    elif char_ascii_code < END_CHAR_ASCII_CODE:
        return chr(char_ascii_code + 1)
    else:
        # workaround for char_ascii_code == END_CHAR_ASCII_CODE + 1, at least makes sure that no wildcard is inserted.
        if wildcard_ascii_code is ord("a"):
            return "b"
        else:
            return "a"
