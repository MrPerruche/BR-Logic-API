from typing import SupportsBytes, Any
# from .brick import Brick
from .utils import settings, FM
from struct import pack as struct_pack


# ------------------- CREATION GENERATION ---------------------




def _convert_brick_types(brick_types: set[str] | list[str]) -> bytearray:
    # Returns brick types to write
    buffer: bytearray = bytearray()
    for brick_type in brick_types:
        buffer.extend(unsigned_int(len(brick_type), 1))
        buffer.extend(utf8(brick_type))
    return buffer


def _convert_brick_names_to_id(names: list) -> dict[str | int, int]:

    return {brick.name: i for i, brick in enumerate(names)}



def _get_property_data(bricks: list, default_properties: dict[str, Any]) -> (
        dict[int, str], dict[str, int], dict[int, dict[int, Any]], dict[int, dict[int, int]]):

    """
    Internal function to transform property data into userful information for .brv file generation.

    :param bricks: List of bricks making the creation
    :param default_properties: Default properties of bricks. (e.g. expects bricks14 variable)
    :return:
        1. Conversion table: property id to type,
        2. Conversion table: type to property id,
        3. Conversion table: property id to (value id to value conversion table),
        4. Conversion table: property id to (id(value) to value id conversion table)
    """

    # I pray id(value) works

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

            if prop_type == 'bin':
                converted = ite_val

            elif prop_type == 'bool':
                converted = b'\x01' if ite_val else b'\x00'

            elif prop_type == 'brick_id':
                if ite_val is None:
                    converted = b'\x00'
                else:
                    try:
                        converted = unsigned_int(1, 2)
                        converted += unsigned_int(brick_id_table[ite_val]+1, 2)
                    except IndexError:
                        raise IndexError(f"Brick {ite_val!r} is missing from the brick id table: it does not exist.")

            elif prop_type == 'float':
                converted = sp_float(ite_val)

            elif prop_type == 'list[3*float]':
                try:
                    # Loops are slow in python. Micro optimisation goes brrr
                    converted = sp_float(ite_val[0])
                    converted += sp_float(ite_val[1])
                    converted += sp_float(ite_val[2])
                except IndexError:
                    raise ValueError("Provided list is shorter than 3 floats long.")

            elif prop_type == 'list[3*uint8]':
                try:
                    # Loops are slow in python. Micro optimisation goes brrr
                    converted = unsigned_int(ite_val[0], 1)
                    converted += unsigned_int(ite_val[1], 1)
                    converted += unsigned_int(ite_val[2], 1)
                except IndexError:
                    raise ValueError("Provided list is shorter than 3 unsigned 8-bit integers long.")

            elif prop_type == 'list[4*uint8]':
                try:
                    # Loops are slow in python. Micro optimisation goes brrr
                    converted = unsigned_int(ite_val[0], 1)
                    converted += unsigned_int(ite_val[1], 1)
                    converted += unsigned_int(ite_val[2], 1)
                    converted += unsigned_int(ite_val[3], 1)
                except IndexError:
                    raise ValueError("Provided list is shorter than 4 unsigned 8-bit integers long.")

            elif prop_type == 'list[6*uint2]':
                # Loops are slow in python. Micro optimisation goes brrr
                converted = unsigned_int(ite_val[0] + (ite_val[1] << 2) + (ite_val[2] << 4) + (ite_val[3] << 6) +
                                           (ite_val[4] << 8) +  (ite_val[5] << 10), 2)

            elif prop_type == 'list[brick_id]':
                try:
                    converted = unsigned_int(len(ite_val), 2)
                    for brick_id in ite_val:
                        converted += unsigned_int(brick_id_table[brick_id]+1, 2)
                except IndexError:
                    raise IndexError(f"Brick {ite_val!r} is missing from the brick id table: it does not exist.")

            elif prop_type == 'str8':
                try:
                    converted = unsigned_int(len(ite_val), 1)
                    converted += ite_val.encode('ascii')
                except UnicodeEncodeError:
                    raise ValueError("Provided string is not 8-bit ASCII.")

            elif prop_type == 'strany':
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
                    converted = signed_int(len(ite_val), 2) + converted
                else:
                    converted = signed_int(-len(ite_val), 2) + converted

            elif prop_type == 'uint8':
                converted = unsigned_int(ite_val, 1)

            if uniform_length:
                if last_elem_length != len(converted) and last_elem_length != -1:
                    uniform_length = False
                last_elem_length = len(converted)
            elements_length.append(len(converted))


        except Exception as e:

            # Notify
            FM.error("Conversion to binary failed",
                     f"It seems value {val!r} is not accepted by a {prop_type} type property.\n"
                     f"{type(e).__name__}: {e}")

            raise (type(e))(f"Conversion to binary failed ({e}). Error mitigation failed.")

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


def get_signed_int(bin_value: SupportsBytes) -> int:

    """
    Convert bytes to a signed integer.

    :param bin_value: Bytes
    :return: Signed integer
    """

    return int.from_bytes(bin_value, byteorder='little', signed=True)


def get_unsigned_int(bin_value: SupportsBytes) -> int:

    """
    Convert bytes to an unsigned integer.

    :param bin_value: Bytes
    :return: Unsigned integer
    """
    return int.from_bytes(bin_value, byteorder='little', signed=False)


def is_utf_encodable(string: str) -> bool:

    """
    Check if the string can be encoded in UTF-8 and UTF-16.

    :param string: String to be tested
    :return: True if the string can be encoded in UTF-8 and UTF-16, otherwise False
    """

    return all(ord(char) <= 0x10FFFF for char in string)


def signed_int(integer: int, byte_len: int) -> bytes:

    """
    Convert a signed integer to bytes.

    :param integer: Signed integer
    :param byte_len: Number of bytes in the integer
    :return: Bytes
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

    :param integer: Unsigned integer
    :param byte_len: Number of bytes in the integer
    :return: Bytes
    """

    if integer >= 2**(byte_len*8):
        raise OverflowError(f'Input is greater than {byte_len*8} bit limit of unsigned integer.')

    if integer < 0:
        raise OverflowError(f'Negative input. {integer} is less than 0.')

    return (integer & ((1 << (8 * byte_len)) - 1)).to_bytes(byte_len, byteorder='little', signed=False)


def sp_float(float_: float) -> bytes:

    return struct_pack('<f', float_).ljust(4, b'\x00')[:4]




def utf8(string: str) -> bytes:

    """
    Convert a string to UTF-8 bytes.

    :param string: String
    :return: Bytes
    """

    return string.encode('ascii')


def utf16(string: str) -> bytes:

    """
    Convert a string to UTF-16 bytes.

    :param string: String
    :return: Bytes
    """

    return string.encode('utf-16')



#OTHER

def extract_bytes(ba: bytearray, n: int):

    if n > len(ba): n = len(ba)

    result = ba[:n]
    del ba[:n]

    return result