from typing import SupportsBytes, Any
# from .brick import Brick
from .utils import settings, FM
from struct import pack as struct_pack, unpack as struct_unpack
from .exceptions import *


# ------------------- CREATION GENERATION ---------------------




def _convert_brick_types(brick_types: set[str] | list[str]) -> bytearray:
    """
    Internal function to convert a list of strings into a bytearray for brick types in creation files.

    Arguments:
        brick_types (set[str] | list[str]): List of strings to convert

    Returns:
        bytearray: Bytearray containing the converted strings
    """

    # Returns brick types to write
    buffer: bytearray = bytearray()
    for brick_type in brick_types:
        buffer.extend(unsigned_int(len(brick_type), 1))
        buffer.extend(utf8(brick_type))
    return buffer


def _convert_brick_names_to_id(names: list) -> dict[str | int, int]:
    """
    Internal function to convert names from a list of bricks into a dictionary of names and ids.

    Arguments:
        names (list): List of bricks to convert

    Returns:
        dict[str | int, int]: Dictionary of names and ids
    """

    return {brick.name: i for i, brick in enumerate(names)}



def _get_property_data(bricks: list, default_properties: dict[str, Any]) -> (
        dict[int, str], dict[str, int], dict[int, dict[int, Any]], dict[int, dict[int, int]]):

    """
    Internal function to transform property data into userful information for creation file generation.

    Arguments:
        bricks: List of bricks making the creation
        default_properties: Default properties of bricks. (e.g. expects bricks14 variable)

    Returns:
        dict[int, str]: property id to type,
        dict[str, int]: type to property id,
        dict[int, dict[int, Any]]: property id to (value id to value conversion table),
        dict[int, dict[int, int]]: property id to (id(value) to value id conversion table)

    TODO EXCEPTIONS
    """

    # I pray id(value) works
    # it works

    # Init variables
    property_id_types: dict[int, str] = {}  # Property and their id
    property_types_id: dict[str, int] = {}  # Property id and their property
    property_id_values_id: dict[int, dict[int, Any]] = {}  # Property id and their values: id -> value
    property_id_values_value: dict[int, dict[Any, int]] = {}  # Property id and their values: value -> id

    for brick in bricks:

        # Cache brick type defaults
        brick_type_defaults: dict[str, Any] = default_properties[brick.get_type()]

        # Contents inside better be O(1); worst case it can run up to 1,050,000 (50,000 * 21) times.
        for property_, value in brick.properties.items():

            # Clarification:
            # - property_id_values_id[property_id] -> gets list of values dict[int, Any]
            # - default_properties[brick.get_type()][property_] -> default value for this brick and this property.

            # Skipping if set to default
            if brick_type_defaults[property_] == value: continue

            # Adding to list of known properties
            # is None if missing else id (int)
            property_id = property_types_id.get(property_)

            # If it is new
            if property_id is None:

                property_id = len(property_types_id)  # Give it an id

                property_id_types[property_id] = property_  # Initialize first property-to-id container
                property_types_id[property_] = property_id  # Initialize second id-to-property container
                # value_id[property_id] = 0

                property_id_values_id[property_id] = {}  # Initialize first id-to-value container
                property_id_values_value[property_id] = {}  # Initialize second value-to-id container

            # Storing values
            # print(property_id_values_value)
            # print(property_id_values_value[property_id])
            value_id: int | None = property_id_values_value[property_id].get(id(value))

            if value_id is None:
                value_id = len(property_id_values_id[property_id])  # Give it an id
                property_id_values_id[property_id][value_id] = value  # Store id-to-value
                property_id_values_value[property_id][id(value)] = value_id  # Store value-to-id

            # else: property is known so we can ignore it

    return property_id_types, property_types_id, property_id_values_id, property_id_values_value


def _get_prop_bin(prop_type: str, id_: int,
                  prop_id_t__val_id_t_val: dict[int, dict[int, Any]],
                  brick_id_table: dict[str | int, int]) -> (bytearray, bytearray):

    """
    Internal function to convert a property type's properties to binary data ready for the creation file.

    Arguments:
        prop_type (str): Property type's type
        id_ (int): Property type's id
        prop_id_t__val_id_t_val (dict[int, dict[int, Any]]): Property id to (value memory address to value) conversion table
        brick_id_table (dict[str | int, int]): Bricks' name to id conversion table

    Returns:
        bytearray: Property binary data
        bytearray: Additional info regarding properties' byte length

    Exceptions:
        ValueError: Invalid value
        NameError: Unknown brick name (brick with this name missing from brci.Creation().bricks)
        brci.BrickError: Brick is invalid, raising unexpected error.
    """

    # Initialize result variable
    result: bytearray = bytearray()
    converted: bytes = b''

    # Clarification:
    # - prop_id_t_val_t_val_id[id_]: Value memory address to value id (of this property)

    last_elem_length: int = -1
    elements_length: list[int] = []
    uniform_length: bool = True

    for val_id, val in prop_id_t__val_id_t_val[id_].items():

        # Treat input
        # Cannot be mitigated, having debug info is important, so we do not do our warning thing.
        ite_val = val() if callable(val) else val

        # Convert to binary (bytearray)
        try:

            match prop_type:
                case 'bin':
                    converted = ite_val

                case 'bool':
                    converted = b'\x01' if ite_val else b'\x00'

                case 'brick_id':
                    if ite_val is None:
                        converted = b'\x00\x00'
                    else:
                        try:
                            converted = unsigned_int(1, 2)
                            converted += unsigned_int(brick_id_table[ite_val]+1, 2)
                        except IndexError:
                            raise NameError(f"Brick {ite_val!r} is missing from the brick id table: it does not exist.")

                case 'float':
                    converted = sp_float(ite_val)

                case 'list[3*float]':
                    try:
                        # Loops are slow in python. Micro optimisation goes brrr
                        converted = sp_float(ite_val[0])
                        converted += sp_float(ite_val[1])
                        converted += sp_float(ite_val[2])
                    except IndexError:
                        raise ValueError("Provided list is shorter than 3 floats long.")

                case 'list[3*uint8]':
                    try:
                        # Loops are slow in python. Micro optimisation goes brrr
                        converted = unsigned_int(ite_val[0], 1)
                        converted += unsigned_int(ite_val[1], 1)
                        converted += unsigned_int(ite_val[2], 1)
                    except IndexError:
                        raise ValueError("Provided list is shorter than 3 unsigned 8-bit integers long.")

                case 'list[4*uint8]':
                    try:
                        # Loops are slow in python. Micro optimisation goes brrr
                        converted = unsigned_int(ite_val[0], 1)
                        converted += unsigned_int(ite_val[1], 1)
                        converted += unsigned_int(ite_val[2], 1)
                        converted += unsigned_int(ite_val[3], 1)
                    except IndexError:
                        raise ValueError("Provided list is shorter than 4 unsigned 8-bit integers long.")

                case 'list[6*uint2]':
                    # Loops are slow in python. Micro optimisation goes brrr
                    converted = unsigned_int(ite_val[0] + (ite_val[1] << 2) + (ite_val[2] << 4) + (ite_val[3] << 6) +
                                               (ite_val[4] << 8) +  (ite_val[5] << 10), 2)

                case 'list[brick_id]':
                    try:
                        converted = unsigned_int(len(ite_val), 2)
                        for brick_id in ite_val:
                            converted += unsigned_int(brick_id_table[brick_id]+1, 2)
                    except IndexError:
                        raise NameError(f"Brick {ite_val!r} is missing from the brick id table: it does not exist.")

                case 'str8':
                    try:
                        converted = unsigned_int(len(ite_val), 1)
                        converted += ite_val.encode('ascii')
                    except UnicodeEncodeError:
                        raise ValueError("Provided string is not 8-bit ASCII.")

                case 'strany':
                    is_ascii: bool = True
                    try:
                        converted = ite_val.encode('ascii')
                    except UnicodeEncodeError:
                        is_ascii: bool = False
                        try:
                            converted = ite_val.encode('utf-16')[2:]
                        except UnicodeEncodeError as e:
                            raise ValueError("Provided string can be encoded in neither ASCII nor UTF-16.") from e
                    if is_ascii:
                        converted = signed_int(len(ite_val), 1) + converted
                    else:
                        converted = signed_int(-len(ite_val), 2) + converted

                case 'uint8':
                    converted = unsigned_int(ite_val, 1)

            if uniform_length:
                if last_elem_length != len(converted) and last_elem_length != -1:
                    uniform_length = False
                last_elem_length = len(converted)
            elements_length.append(len(converted))


        except Exception as e:

            raise BrickError(f"Invalid value {val!r} (id: {val_id}) used for property of type {prop_type} raising {e!r}", culprit=None)

        result.extend(converted)


    addon = bytearray()
    if len(elements_length) > 1:
        if uniform_length:
            addon: bytearray = bytearray(unsigned_int(last_elem_length, 2))
        else:
            addon: bytearray = bytearray(b'\x00\x00')
            for elem_len in elements_length:
                addon: bytearray = bytearray(unsigned_int(elem_len, 2))


    return result, addon




# ------------------- GENERAL --------------------


def get_signed_int(bin_value: bytes | bytearray) -> int:

    """
    Convert bytes or bytearray to an integer.

    Arguments:
        bin_value (bytes | bytearray): Bytes to convert (little-endian)

    Returns:
        int: Integer
    """

    return int.from_bytes(bin_value, byteorder='little', signed=True)


def get_unsigned_int(bin_value: bytes | bytearray) -> int:

    """
    Convert bytes to an unsigned integer.

    Arguments:
        bin_value (bytes | bytearray): Bytes to convert (little-endian)

    Returns:
        int: Integer (unsigned)
    """
    return int.from_bytes(bin_value, byteorder='little', signed=False)


def can_be_encoded_in_utf(string: str) -> bool:

    """
    Check if the string can be encoded in UTF-8 and UTF-16.

    Arguments:
        string (str): String to check

    Returns:
        bool: True if the string can be encoded in UTF-8 and UTF-16
    """

    return all(ord(char) <= 0x10FFFF for char in string)


def signed_int(integer: int, byte_len: int) -> bytes:

    """
    Convert a signed integer to bytes.

    Arguments:
        integer (int): Signed integer
        byte_len (int): Number of bytes in the integer

    Returns:
        bytes: Bytes object representing the integer (little-endian)

    Exceptions:
        OverflowError: If the integer is out of range
    """

    if integer < -2**(byte_len*8-1):
        raise OverflowError(f'Input is less than {byte_len*8} bit limit of signed integer.')

    if integer >= 2**(byte_len*8-1):
        raise OverflowError(f'Input is greater than {byte_len*8} bit limit of signed integer.')

    return integer.to_bytes(byte_len, byteorder='little', signed=True)

# This is a comment.

def unsigned_int(integer: int, byte_len: int) -> bytes:

    """
    Convert an unsigned integer to bytes.

    Arguments:
        integer (int): Unsigned integer
        byte_len (int): Number of bytes in the integer

    Returns:
        bytes: Bytes object representing the integer (little-endian)

    Exceptions:
        OverflowError: If the integer is out of range
    """

    if integer >= 2**(byte_len*8):
        raise OverflowError(f'Input is greater than {byte_len*8} bit limit of unsigned integer.')

    if integer < 0:
        raise OverflowError(f'Negative input. {integer} is less than 0.')

    return (integer & ((1 << (8 * byte_len)) - 1)).to_bytes(byte_len, byteorder='little', signed=False)


def sp_float(float_: float) -> bytes:

    """
    Convert a float to bytes.

    Arguments:
        float_ (float): Float

    Returns:
        bytes: Bytes object representing the float (little-endian, single-precision)

    Exceptions:
        OverflowError: If the float is out of range
    """

    return struct_pack('<f', float_).ljust(4, b'\x00')[:4]


def get_sp_float(ba: bytearray) -> float:

    """
    Convert bytes to a float.

    Arguments:
        ba (bytearray): Bytes to convert (little-endian, single-precision)

    Returns:
        float: Float
    """

    return struct_unpack('<f', bytes(ba[:4]))[0]




def utf8(string: str) -> bytes:

    """
    Convert a string to UTF-8 bytes.

    Arguments:
        string (str): String

    Returns:
        bytes: Bytes

    Exceptions:
        UnicodeEncodeError: If the string cannot be encoded
    """

    return string.encode('ascii')


def get_utf8(bin_value: bytes | bytearray) -> str:

    """
    Convert UTF-8 bytes to a string.

    Arguments:
        bin_value (bytes | bytearray): Bytes to convert (little-endian)

    Returns:
        str: String
    """

    return bin_value.decode('ascii')


def utf16(string: str) -> bytes:

    """
    Convert a string to UTF-16 bytes.

    Arguments:
        string (str): String

    Returns:
        bytes: Bytes

    Exceptions:
        UnicodeEncodeError: If the string cannot be encoded
    """

    return string.encode('utf-16')


def get_utf16(bin_value: bytes | bytearray) -> str:

    """
    Convert UTF-16 bytes to a string.

    Arguments:
        bin_value (bytes | bytearray): Bytes to convert (little-endian)

    Returns:
        str: String
    """

    return bin_value.decode('utf-16')


#OTHER

def extract_bytes(ba: bytearray, n: int) -> bytearray:

    """
    Removes the first n bytes of the bytearray and returns them, or all if n is greater than the length of the bytearray.

    Arguments:
        ba (bytearray): Bytearray to extract from
        n (int): Number of bytes to extract

    Returns:
        bytearray: Extracted bytes
    """

    if n > len(ba): n = len(ba)

    result = ba[:n]
    del ba[:n]

    return result



def extract_str8(ba: bytearray) -> str:

    """
    Extracts UTF-8 encoded string from a Brick Rigs file

    Arguments:
        ba (bytearray): Bytearray to extract from

    Returns:
        str: Extracted string
    """

    return get_utf8(extract_bytes(ba, get_unsigned_int(extract_bytes(ba, 1))))

def extract_str16(ba: bytearray) -> str:

    """
    Extracts UTF-8 or UTF-16 encoded string from a Brick Rigs file

    Arguments:
        ba (bytearray): Bytearray to extract from

    Returns:
        str: Extracted string
    """

    str_len: int = get_unsigned_int(extract_bytes(ba, 2))
    if str_len < 0:
        return get_utf16(extract_bytes(ba, -str_len))
    else:
        return get_utf8(extract_bytes(ba, str_len))

