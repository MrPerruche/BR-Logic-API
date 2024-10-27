# from collections.abc import MutableMapping, MutableSequence
from typing import Final, Optional, Any
from datetime import datetime, timezone
import os.path
import re
from builtins import print as printb


# Externals...
try:
    import numpy as np
except ImportError as e:
    raise ImportError("Failed to import Numpy! As of BRCI-D, Numpy is a hard requirement. Please install it with `pip install numpy` and try again.")

# -------------------- DATA --------------------

# Version
BRCI_VERSION: str = "D11"  # D(...) is basically 4.(...)

# Paths
_CWD: str = os.path.dirname(os.path.realpath(__file__))
_LOCALAPPDATA: str = os.getenv("LOCALAPPDATA")

if os.name == 'nt':
    _USER: str = os.getenv('%USERNAME%')
    BRICK_RIGS_FOLDER: list[str] = [os.path.join(_LOCALAPPDATA, 'BrickRigs', 'SavedRemastered', 'Vehicles')]
else:
    _USER: str = os.getenv('$USER')
    # TODO: Get something safer than this
    BRICK_RIGS_FOLDER: list[str] = [
        os.path.expanduser(f"~/.steam/steamapps/compatdata/552100/pfx/drive_c/users/steamuser/AppData/Local/BrickRigs/SavedRemastered/Vehicles"),
        os.path.expanduser(f"~/.wine/drive_c/users/{_USER}/AppData/Local/BrickRigs/SavedRemastered/Vehicles"),
        os.path.expanduser(f"~/.local/share/Steam/steamapps/compatdata/552100/pfx/drive_c/users/steamuser/AppData/Local/BrickRigs/SavedRemastered/Vehicles")
    ]

PROJECT_FOLDER: str = os.path.join(_CWD, 'Projects')
BACKUP_FOLDER: str = os.path.join(_CWD, 'Backups')

NO_THUMBNAIL: str = os.path.join(_CWD, 'resources', 'no_thumbnail.png')
BRCI_THUMBNAIL: str = os.path.join(_CWD, 'resources', 'brci.png')

# Settings
settings: dict[str, Any] = {
    'show_logs': True,
    'attempt_error_mitigation': True
}


class Limits:

    """
    Class for holding integer and floating-point limits.

    :var U8_MAX: Maximum unsigned 8-bit integer (255)
    :var U16_MAX: Maximum unsigned 16-bit integer (65535)
    :var U32_MAX: Maximum unsigned 32-bit integer (4294967295)
    :var U64_MAX: Maximum unsigned 64-bit integer (18446744073709551615)

    :var I8_MAX: Maximum signed 8-bit integer (127)
    :var I16_MAX: Maximum signed 16-bit integer (32767)
    :var I32_MAX: Maximum signed 32-bit integer (2147483647)
    :var I64_MAX: Maximum signed 64-bit integer (9223372036854775807)

    :var U8_MIN: Minimum unsigned 8-bit integer (0)
    :var U16_MIN: Minimum unsigned 16-bit integer (0)
    :var U32_MIN: Minimum unsigned 32-bit integer (0)
    :var U64_MIN: Minimum unsigned 64-bit integer (0)

    :var I8_MIN: Minimum signed 8-bit integer (-128)
    :var I16_MIN: Minimum signed 16-bit integer (-32768)
    :var I32_MIN: Minimum signed 32-bit integer (-2147483648)
    :var I64_MIN: Minimum signed 64-bit integer (-9223372036854775808)
    """

    # Integer limits
    U2_MAX: Final[int] = 3
    U8_MAX: Final[int] = np.iinfo(np.uint8).max
    U16_MAX: Final[int] = np.iinfo(np.uint16).max
    U32_MAX: Final[int] = np.iinfo(np.uint32).max
    U64_MAX: Final[int] = np.iinfo(np.uint64).max

    I2_MAX = 1
    I8_MAX: Final[int] = np.iinfo(np.int8).max
    I16_MAX: Final[int] = np.iinfo(np.int16).max
    I32_MAX: Final[int] = np.iinfo(np.int32).max
    I64_MAX: Final[int] = np.iinfo(np.int64).max

    U2_MIN: Final[int] = 0
    U8_MIN: Final[int] = 0
    U16_MIN: Final[int] = 0
    U32_MIN: Final[int] = 0
    U64_MIN: Final[int] = 0

    I2_MIN: Final[int] = -2
    I8_MIN: Final[int] = np.iinfo(np.int8).min
    I16_MIN: Final[int] = np.iinfo(np.int16).min
    I32_MIN: Final[int] = np.iinfo(np.int32).min
    I64_MIN: Final[int] = np.iinfo(np.int64).min

    # Floating-point limits
    F32_MAX: Final[int] = np.finfo(np.float32).max
    F64_MAX: Final[int] = np.finfo(np.float64).max

    F32_MIN: Final[int] = np.finfo(np.float32).min
    F64_MIN: Final[int] = np.finfo(np.float64).min


class FM:

    """
    Class containing various formatting features.
    """

    BLACK: Final[str] = '\033[30m'
    RED: Final[str] = '\033[91m'
    GREEN: Final[str] = '\033[92m'
    YELLOW: Final[str] = '\033[93m'
    BLUE: Final[str] = '\033[94m'
    MAGENTA: Final[str] = '\033[95m'
    CYAN: Final[str] = '\033[96m'
    WHITE: Final[str] = '\033[97m'
    LIGHT_BLACK: Final[str] = '\033[90m'
    LIGHT_RED: Final[str] = '\033[91m'
    LIGHT_GREEN: Final[str] = '\033[92m'
    LIGHT_YELLOW: Final[str] = '\033[93m'
    LIGHT_BLUE: Final[str] = '\033[94m'
    LIGHT_MAGENTA: Final[str] = '\033[95m'
    LIGHT_CYAN: Final[str] = '\033[96m'
    LIGHT_WHITE: Final[str] = '\033[97m'

    BOLD: Final[str] = '\033[1m'
    UNDERLINE: Final[str] = '\033[4m'
    ITALIC: Final[str] = '\033[3m'
    REVERSE: Final[str] = '\033[7m'
    STRIKETHROUGH: Final[str] = '\033[9m'

    CLEAR_ALL: Final[str] = '\033[0m'
    CLEAR_BOLD: Final[str] = '\033[22m'
    CLEAR_UNDERLINE: Final[str] = '\033[24m'
    CLEAR_ITALIC: Final[str] = '\033[23m'
    CLEAR_REVERSE: Final[str] = '\033[27m'
    CLEAR_STRIKETHROUGH: Final[str] = '\033[29m'

    # Function that outputs an error message
    @staticmethod
    def error(message: str, details: Optional[str] = None, force_print: bool = False) -> bool:

        """
        Will print an error message if show_logs is set to True.

        :param message: Header of the error, reversed.
        :param details: Details of the error, not reversed. If omitted (set to None), details will be omitted and the message will not be reversed.
        :param force_print: Will print regardless of what show_logs is set to.

        :return: True if the message was printed, else False.
        :rtype: bool
        """

        # Printing
        if force_print or settings['show_logs']:

            # If we specified details
            if details is not None:
                print(f'{FM.RED}{FM.REVERSE}[ERROR] {message}{FM.CLEAR_REVERSE} \n{details}')
            # If we did not specify details
            else:
                print(f'{FM.RED}{FM.REVERSE}[ERROR]{FM.CLEAR_REVERSE} {message}')

            # Either way, the message was printed
            return True

        # else:
        return False

    @staticmethod
    def success(message: str, details: Optional[str] = None, force_print: bool = False) -> bool:

        """
        Will print a success message if show_logs is set to True.

        :param message: Header of the success, reversed.
        :param details: Details of the success, not reversed. If omitted (set to None), details will be omitted and the message will not be reversed.
        :param force_print: Will print regardless of what show_logs is set to.

        :return: True if the message was printed, else False.
        :rtype: bool
        """

        if force_print or settings['show_logs']:

            # If we specified details
            if details is not None:
                print(f'{FM.LIGHT_GREEN}{FM.REVERSE}[SUCCESS] {message}{FM.CLEAR_REVERSE} \n{details}{FM.CLEAR_ALL} ')
            # If we did not specify details
            else:
                print(f'{FM.LIGHT_GREEN}{FM.REVERSE}[SUCCESS]{FM.CLEAR_REVERSE} {message}{FM.CLEAR_ALL} ')

            # Either way, the message was printed
            return True

        # else:
        return False


    @staticmethod
    def add_color_aliases() -> None:
        for attribute_name in dir(FM):
            if not attribute_name.startswith('_'):
                setattr(FM, attribute_name.lower(), getattr(FM, attribute_name))

# --------------------    COLOR ADDITIONS    -------------------- #

def printr(*args, end: str = "\n", sep: str = " ", clear: str = FM.CLEAR_ALL, **kwargs) -> str:

    """Print-Reset-Return. Resets color. Also, will return the text passed to it."""

    printb(*args, end=f"{end}{clear}", sep=sep, **kwargs)

    return_str = sep.join([str(arg) for arg in args])
    return repr(return_str.strip())[1:-1] # sanitization: do not keep color codes in the return string

# ------------------- TIME-RELATED FUNCTIONS -------------------- #


def get_time_100ns() -> int:

    """
    Get the current time in 100 nanoseconds. Notably used in metadata and for BRCI backups.

    :return: 100s of nanoseconds since 0001-01-01 00:00:00
    :rtype: int
    """

    # Get current UTC time
    now = datetime.now(timezone.utc)
    # Calculate the time since year 1
    time_delta = now - datetime(1, 1, 1, tzinfo=timezone.utc)
    # Convert to 100 nanoseconds
    return int(time_delta.total_seconds() * 10**7)


# -------------------- OS RELATED FUNCTIONS --------------------


def is_valid_folder_name(name: str, is_nt: bool) -> bool:

    """
    Check if the folder name is valid.

    :param name: Potentially invalid name
    :param is_nt: True if we are working with NT, otherwise False (POSIX)

    :return: True if the name is valid, otherwise False
    :rtype: bool
    """

    if is_nt:
        # Check for NT system validity
        # nt_match = r'[<>:"/\\|?*]'  # TODO figure out a better solution for path issues
        nt_match = r'[<>:"/|?*]'
        """
        if re.search(nt_match, name): print("fuck you regex")
        if len(name) == 0: print("fuck you len")
        if set(name) == set(): print("fuck you sets")
        if name[-1] in {'.', ' '}: print("fuck you last character")
        if name in (
                "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
                "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"): print("fuck you banned strs")
        """
        if re.search(nt_match, name[2:] if len(name) > 1 and name[1] == ':' else name) or len(name) == 0 or set(name
                ) == set() or name[-1] in {'.', ' '} or name in ("CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3",
                "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7",
                "LPT8", "LPT9"):
            return False
    else:
        # Check for POSIX system validity
        posix_match = r'[<>:"/\\|?*\x00-\x1F]'
        if re.search(posix_match, name) or len(name) == 0 or set(name) == set():
            return False

    # else: valid
    return True


