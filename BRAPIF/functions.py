import struct
from dataclasses import dataclass


def unsigned_int(integer, byte_len):

    if integer >= 2**(byte_len*8):
        raise OverflowError(f'Input is greater than {byte_len*8} bit limit of unsigned integer.')

    if integer < 0:
        raise OverflowError(f'Negative input. {integer} is less than 0.')

    return (integer & ((1 << (8 * byte_len)) - 1)).to_bytes(byte_len, byteorder='little', signed=False)


# Function to write signed negative integers of any byte length. Used for utf-16 encoding
def signed_int(integer, byte_len):
    return integer.to_bytes(byte_len, byteorder='little', signed=True)


# Function to write half, single and double precision float number
def bin_float(float_number, byte_len):

    if byte_len == 2:
        # Convert the float to a  32-bit integer representation
        float_bits = struct.unpack('<I', struct.pack('<f', float_number))[0]

        # Extract the sign, exponent, and mantissa from the float bits
        sign = (float_bits >> 16) & 0x8000
        exponent = (float_bits >> 23) & 0xFF
        mantissa = float_bits & 0x7FFFFF

        # Handle special cases
        if exponent == 255:
            # Infinity or NaN
            if mantissa:
                # NaN, return a half-precision NaN
                return struct.pack('<H', 0x7C00 | (mantissa >> 13))
            else:
                # Infinity, return a half-precision infinity
                return struct.pack('<H', sign | 0x7C00)

        # Subtract the bias from the exponent
        exponent -= 127

        # Check for overflow or underflow
        if exponent < -24:
            # Underflow, return zero
            return struct.pack('<H', sign)
        elif exponent > 15:
            # Overflow, return infinity
            return struct.pack('<H', sign | 0x7C00)

        # Normalize the mantissa and adjust the exponent
        mantissa >>= 13
        exponent += 15

        # Combine the sign, exponent, and mantissa into a half-precision float
        half_float_bits = (sign << 15) | (exponent << 10) | mantissa

        # Pack the half-precision float bits into a  16-bit binary string
        return struct.pack('<H', half_float_bits)

    elif byte_len == 4:  # Single-precision float
        float_bytes = struct.pack('<f', float_number)
    elif byte_len == 8:  # Double-precision float
        float_bytes = struct.pack('<d', float_number)
    else:
        raise ValueError("Invalid byte length for float")

    padded_bytes = float_bytes.ljust(byte_len, b'\x00')[:byte_len]

    return padded_bytes


# Function to write with utf-16 encoding (Neg. length excluded)
def bin_str(string):
    return string.encode('utf-16')


# Function to write with utf-8 encoding (Length excluded)
def small_bin_str(string):
    return string.encode('utf-8')


# Function to copy existing files into new directories
def copy_file(source_path, destination_path):
    with open(source_path, 'rb') as src_file:
        cp_data = src_file.read()

    _blank_preview = open(destination_path, "x")
    _blank_preview.close()

    with open(destination_path, 'wb') as destination_file:
        destination_file.write(cp_data)


def append_multiple(var, keys, value, gbn=False):
    for key in keys:

        var[key] = value.copy()

        if gbn:
            var[key]['gbn'] = key





@dataclass
class BrickInput:

    brick_input_type: str
    brick_input: any

    def return_br(self):
        w_return = b''

        # We write what the input is
        w_return += unsigned_int(len(self.brick_input_type), 1)


        # Now if its something that has more information..
        match self.brick_input_type:
            # If its a constant value (They're called AlwaysOn ingame, why fluppi?)
            case 'AlwaysOn':
                # If something other than 1.0 or nothing is defined..
                if float(self.brick_input) is not None or float(self.brick_input) != 1.0:
                    # We write what value is in
                    w_return += (b'\x12' + small_bin_str('InputChannel.Value')
                                 + b'\x01\x00\x00\x00\x04' + bin_float(self.brick_input, 4))

            case 'Custom':
                # This require data only available in main.py
                # It is impossible to write it here as it this data is from BRAPI class in main.py
                # So we send a message BRAPI class has some work to do
                w_return = b'CUSTOM REQ STR2BID'  # Pay attention, we're not adding, we're replacing!
            # If theres nothing special we don't care then

            case _:
                pass

        return w_return