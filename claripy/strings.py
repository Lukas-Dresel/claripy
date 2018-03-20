import re
from .backend_object import BackendObject
from .bv import BVV

class StringV(BackendObject):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'StringV(%s)' % (self.value)

def StrConcat(*args):
    """
    Create a concrete version of the concatenated string
    :param args: List of string that has to be concatenated

    :return : a concrete version of the concatenated string
    """
    new_value = ''.join([arg.value for arg in args])
    return StringV(new_value)
    
def Substr(start_idx, end_idx, initial_string):
    """
    Create a concrete version of the substring
    :param start_idx : starting index of the substring
    :param end_idx : last index of the substring
    :param initial_string 

    :return : a concrete version of the substring
    """
    if start_idx == end_idx:
        new_value = initial_string.value[start_idx]
    else:
        new_value = initial_string.value[start_idx:end_idx]
    return StringV(new_value)


def StrReplace(initial_string, pattern_to_be_replaced, replacement_pattern):
    """
    Create a concrete version of the replaced string
    (replace ONLY th efirst occurrence of the pattern)
    :param initial_string : string in which the pattern needs to be replaced
    :param pattern_to_be_replaced : substring that has to be replaced inside initial_string 
    :param replacement_poattern : pattern that has to be inserted in initial_string t replace
                                  pattern_to_be_replaced
    
    :return : a concrete representation of the replaced string
    """
    new_value = initial_string.value.replace(pattern_to_be_replaced.value, 
                                             replacement_pattern.value,
                                             1)
    return StringV(new_value)


def StrLen(input_string, bitlength):
    """
    Create a concrete Bit-Vector of 32(?) bit size and as value the length of the string in bytes

    :param input_string: the string we want to calculate the lenght 
    :param bitlength: bitlength of the bitvector representing the length of the string
    
    :return : Bit vector holding the size of the string in bytes
    """
    return BVV(len(input_string.value), bitlength)


def StrContains(input_string, substring):
    """
    Return True if the substring is contained in the concrete value of the input_string
    otherwise false.

    :param input_string: the string we want to check
    :param substring: the string we want to check if it's contained inside the input_string
    
    :return : True is substring is contained in input_string else false 
    """
    return substring.value in input_string.value


def StrPrefixOf(prefix, input_string):
    """
    Return True if the concrete value of the input_string starts with prefix
    otherwise false.

    :param prefix: prefix we want to check 
    :param input_string: the string we want to check
    
    :return : True if the input_string starts with prefix else false 
    """
    return True if re.match(r'^' + prefix.value, input_string.value) is not None else False

def StrSuffixOf(suffix, input_string):
    """
    Return True if the concrete value of the input_string ends with suffix
    otherwise false.

    :param suffix: suffix we want to check 
    :param input_string: the string we want to check
    
    :return : True if the input_string ends with suffix else false 
    """
    return True if re.match(r'.*' + suffix.value + '$', input_string.value) is not None else False

def StrIndexOf(input_string, substring, bitlength):
    """
    Return True if the concrete value of the input_string ends with suffix
    otherwise false.

    :param input_string: the string we want to check
    :param substring: the substring we want to finde the index
    :param bitlength: bitlength of the bitvector representing the index of the substring
    
    :return BVV: index of the substring in bit-vector representation or -1 in bitvector representation
    """
    try:
        return BVV(input_string.value.index(substring.value), 32)
    except ValueError:
        return BVV(-1, 32)