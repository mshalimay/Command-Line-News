# Moises Shalimay Andrade
# Auxiliary module with functions that tests if strings are numbers and convert them


def num_is_integer(number):

    if isinstance(number,int):
        return True

    if isinstance(number,float):
        return number.is_integer()

    return False

def str_is_integer(astring:str):
    """returns a boolean indicating if a string is an integer. 
    Eg.: str_is_integer('3')==True, str_is_integer('3/3')=True, str_is_integer('3.0')==True, str_is_integer('2.5')==False
    Args:
        asstring (str): a string potentially containing an integer
    Returns:
        boolean: True if the string is an integer; false otherwise
    """
    # if isnt a number, isnt an integer
    if not is_number(astring):
        return False

    # if is a number, but is a fraction, test if it is in the format ('a/a')
    elif is_fraction(astring):
        numerator_denominator = astring.split('/')
        if numerator_denominator[0] == numerator_denominator[1]:
            return True
        else:
            return False      
    # it is a number and not a fraction, can be a float in the format (a.x, x>0) -> isnt an integer
    # if it is a number in the format 'x.0' or 'x' -> it is an integer
    else:
        number = float(astring)
        if num_is_integer(number):
            return True
        else:
            return False

def is_numberdigit(astring:str):
    """check if a string is a number in the format "x or abc.def" and return True or False; dont consider fractions

    Obs1.: The function ignores whitespaces in strings, but spaces happen BETWEEN characters, the function will return False. Eg.: '3 .5' = False.
    Obs2.: This function is an auxiliary to construct the "is_fraction" function without getting into circularity ("is_fraction" test if digits are floats), 
    both are then consolidated in the full 'is_number' function
    """
    # remove whitespaces and potential spaces between numbers for further evaluation
    astring = astring.strip()
    astring = astring.replace(" ","")
    
    # if cannot convert to a float, then it is not a "pure" number (i.e., contain strings besides numberss)
    try:
        float(astring)
        return True
    except:
        return False

def is_fraction(astring:str):
    """ Checks if a string is a fraction in the format "a/b" and returns True or False
    Obs.: float/integer is also considered as a fraction (e.g., 3.5/4 or pi/3 are fractions)""" 
    # if does not find the "/", not a fraction
    if astring.find("/")==-1:
        return False
    else:
        # remove whitespaces and potential spaces between numbers for further evaluation
        astring = astring.strip()
        astring = astring.replace(" ","")
        # if there are two charachters separated by "/" and all them are numbers -> Fraction
        numerator_denominator = astring.split('/')
        if len(numerator_denominator) == 2 and all(is_numberdigit(charach) for charach in numerator_denominator):
            return True
        else:
            return False

def fraction_to_float(astring:str):
    """ Converts a string that is a fraction to a float"""
    fraction = None
    if is_fraction(astring):
        numerator_denominator = astring.split('/')
    return float(numerator_denominator[0])/float(numerator_denominator[1])

def is_number(astring:str):
    """check if a string is a number and return True or False. Consider fractions

    Obs1.: The function ignores whitespaces in strings, but spaces happen BETWEEN characters, the function will return False. Eg.: '3 .5' = False.
    Obs2.: Consider fractions in the format 'a/b'
    """
    # check if string is a fraction (a/b)
    if is_fraction(astring):
        return True
    
    # check if string is a number in the format "x" or "abc.def"
    elif is_numberdigit(astring):
        return True

    else:
        return False

def str_to_number(astring: str):
    """Converts a string input to a number
    Returns: a float or None
    """
    number = None
    if is_number(astring):
        # if it is a number, convert to float (deal with fractions separately)
        if is_fraction(astring):
            number = fraction_to_float(astring)
        else:
            number = float(astring)
    return number
      