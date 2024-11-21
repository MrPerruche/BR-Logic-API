# from collections.abc import MutableMapping, MutableSequence
from typing import Final, Optional, Any, Literal
from datetime import datetime, timezone
import os.path
import re
from builtins import print as printb
import functools
from json import loads as json_load
from itertools import repeat
from zlib import crc32 as zlib_crc32
from .exceptions import *
from copy import deepcopy

we_have_logging = False

# Externals...
try:
    import numpy as np
except ImportError as e:
    raise ImportError("Failed to import Numpy! As of BRCI-D, Numpy is a hard requirement. Please install it with `pip install numpy` and try again.")

try:
    import logging
    we_have_logging = True
except ImportError:
    print("`logging` module not found. Logging is a soft-dependency. Please install it, as it can greatly help the debugging process.")



# -------------------- DATA --------------------

# Version
BRCI_VERSION: str = "4.17.0"
# Paths
BRCI_CWD: str = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
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

PROJECT_FOLDER: str = os.path.join(BRCI_CWD, 'Projects')
BACKUP_FOLDER: str = os.path.join(BRCI_CWD, 'Backups')

NO_THUMBNAIL: str = os.path.join(BRCI_CWD, 'resources', 'no_thumbnail.png')
BRCI_THUMBNAIL: str = os.path.join(BRCI_CWD, 'resources', 'brci.png')
BLANK_THUMBNAIL: str = os.path.join(BRCI_CWD, 'resources', 'blank.png')
MISSING_THUMBNAIL: str = os.path.join(BRCI_CWD, 'resources', 'missing_thumbnail.png')

# Settings
settings: dict[str, Any] = {
    'show_logs': True,
    'wip_features': False
}

if we_have_logging:
    # The import exists.
    logfile_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'brci.log')

    if os.path.exists(logfile_path):
        # Remove log file if it exists. By default, logging uses append.
        os.remove(logfile_path)

    logger = logging.getLogger("BRCI")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(logfile_path, mode="a", encoding="utf-8", errors="ignore") # For some godforsaken reason, if mode is not append, it doesn't log.
                                                                                                  # after this `if` statement. Period. No clue why.
                                                                                                  # DO NOT TOUCH. Black magic at work.
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("Logging set up!")

class Limits:

    """
    Class for holding integer and floating-point limits.

    Variables:
        U2_MAX (int): Maximum unsigned 2-bit integer (3)
        U8_MAX (int): Maximum unsigned 8-bit integer (255)
        U16_MAX (int): Maximum unsigned 16-bit integer (65535)
        U32_MAX (int): Maximum unsigned 32-bit integer (4294967295)
        U64_MAX (int): Maximum unsigned 64-bit integer (18446744073709551615)

        I2_MAX (int): Maximum signed 2-bit integer (1)
        I8_MAX (int): Maximum signed 8-bit integer (127)
        I16_MAX (int): Maximum signed 16-bit integer (32767)
        I32_MAX (int): Maximum signed 32-bit integer (2147483647)
        I64_MAX (int): Maximum signed 64-bit integer (9223372036854775807)

        U2_MIN (int): Minimum unsigned 2-bit integer (0)
        U8_MIN (int): Minimum unsigned 8-bit integer (0)
        U16_MIN (int): Minimum unsigned 16-bit integer (0)
        U32_MIN (int): Minimum unsigned 32-bit integer (0)
        U64_MIN (int): Minimum unsigned 64-bit integer (0)

        I2_MIN (int): Minimum signed 2-bit integer (-2)
        I8_MIN (int): Minimum signed 8-bit integer (-128)
        I16_MIN (int): Minimum signed 16-bit integer (-32768)
        I32_MIN (int): Minimum signed 32-bit integer (-2147483648)
        I64_MIN (int): Minimum signed 64-bit integer (-9223372036854775808)
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

    Variables:
        BLACK (Final[str]): ANSI escape code for black text
        RED (Final[str]): ANSI escape code for red text
        GREEN (Final[str]): ANSI escape code for green text
        YELLOW (Final[str]): ANSI escape code for yellow text
        BLUE (Final[str]): ANSI escape code for blue text
        MAGENTA (Final[str]): ANSI escape code for magenta text
        CYAN (Final[str]): ANSI escape code for cyan text
        WHITE (Final[str]): ANSI escape code for white text
        LIGHT_BLACK (Final[str]): ANSI escape code for light black (gray) text
        LIGHT_RED (Final[str]): ANSI escape code for light red text
        LIGHT_GREEN (Final[str]): ANSI escape code for light green text
        LIGHT_YELLOW (Final[str]): ANSI escape code for light yellow text
        LIGHT_BLUE (Final[str]): ANSI escape code for light blue text
        LIGHT_MAGENTA (Final[str]): ANSI escape code for light magenta text
        LIGHT_CYAN (Final[str]): ANSI escape code for light cyan text
        LIGHT_WHITE (Final[str]): ANSI escape code for light white (bright white) text
        BOLD (Final[str]): ANSI escape code for bold text
        UNDERLINE (Final[str]): ANSI escape code for underlined text
        ITALIC (Final[str]): ANSI escape code for italic text
        REVERSE (Final[str]): ANSI escape code for reversed text
        STRIKETHROUGH (Final[str]): ANSI escape code for strikethrough text
        CLEAR_ALL (Final[str]): ANSI escape code for clearing all formatting
        CLEAR_COLOR (Final[str]): ANSI escape code for clearing color formatting
        CLEAR_BOLD (Final[str]): ANSI escape code for clearing bold formatting
        CLEAR_UNDERLINE (Final[str]): ANSI escape code for clearing underlined formatting
        CLEAR_ITALIC (Final[str]): ANSI escape code for clearing italic formatting
        CLEAR_REVERSE (Final[str]): ANSI escape code for clearing reversed formatting
        CLEAR_STRIKETHROUGH (Final[str]): ANSI escape code for clearing strikethrough formatting
    """

    BLACK: Final[str] = '\033[30m'
    RED: Final[str] = '\033[31m'
    GREEN: Final[str] = '\033[32m'
    YELLOW: Final[str] = '\033[33m'
    BLUE: Final[str] = '\033[34m'
    MAGENTA: Final[str] = '\033[35m'
    CYAN: Final[str] = '\033[36m'
    WHITE: Final[str] = '\033[37m'
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
    CLEAR_COLOR: Final[str] = '\033[39m'
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

        Arguments:
            message (str): Header of the error.
            details (Optional[str], optional): Details of the error, not reversed. If omitted (set to None), details will be omitted and the message will not be reversed.
            force_print (bool, optional): Will print regardless of what show_logs is set to. Defaults to False.

        Returns:
            bool: True if the message was printed, else False.
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

        Arguments:
            message (str): Header of the success.
            details (Optional[str], optional): Details of the success, not reversed. If omitted (set to None), details will be omitted and the message will not be reversed.
            force_print (bool, optional): Will print regardless of what show_logs is set to. Defaults to False.

        Returns:
            bool: True if the message was printed, else False.
        """

        if force_print or settings['show_logs']:

            # If we specified details
            if details is not None:
                print(f'{FM.YELLOW}{FM.REVERSE}[WARN] {message}{FM.CLEAR_REVERSE} \n{details}{FM.CLEAR_ALL} ')
            # If we did not specify details
            else:
                print(f'{FM.YELLOW}{FM.REVERSE}[WARN]{FM.CLEAR_REVERSE} {message}{FM.CLEAR_ALL} ')

            # Either way, the message was printed
            return True

        # else:
        return False

    @staticmethod
    def warning(message: str, details: Optional[str] = None, force_print: bool = False) -> bool:

        """
        Will print a warning message if show_logs is set to True.

        Arguments:
            message (str): Header of the warning.
            details (Optional[str], optional): Details of the warning, not reversed. If omitted (set to None), details will be omitted and the message will not be reversed.
            force_print (bool, optional): Will print regardless of what show_logs is set to. Defaults to False.

        Returns:
            bool: True if the message was printed, else False.
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
        """
        NOT RECOMMENDED.
        Will add lowercase snake_case aliases to the FM class.
        """
        for attribute_name in dir(FM):
            if not attribute_name.startswith('_') and attribute_name.lower() in dir(FM):
                setattr(FM, attribute_name.lower(), getattr(FM, attribute_name))


# --------------------    COLOR ADDITIONS    -------------------- #

def printr(*args: object, end: str = '\n', sep: str = ' ', col: str = '', clear: str = FM.CLEAR_ALL, **kwargs) -> str:

    """
    Print-Reset-Return. Resets color after printing message.

    Arguments:
        *args (tuple): Arguments to print.
        end (str, optional): End of the print. Defaults to "\n".
        sep (str, optional): Separator between arguments. Defaults to " ".
        col (Optional[str], optional): Color to use. Defaults to None.
        clear (str, optional): Color to clear. Defaults to FM.CLEAR_ALL.
    """

    printb(f"{col}{sep.join([str(arg) for arg in args])}", end=f"{end}{clear}", **kwargs)

    return_str = sep.join([str(arg) for arg in args])
    return repr(return_str.strip())[(0 if col else 1):-(1 if clear else 0)] # sanitization: do not keep color codes in the return string


# --------------------    FONT    -------------------- #

fonts: dict[ str, dict[str, list[list[ list[int] ]] ] ] = {}
font_colors: dict[str, dict[str, list[int]]] = {}

def load_font(json_font_path: str, font_name: str) -> None:

    """
    Will load a font from a json file. The json file must have the following structure:
    {
        "colors": {
            " ": [<color for empty>],
            "<character to replace>": [<r>, <g>, <b>],
            ...
        },
        "none": [
            "<pixels as characters for each line. They will be replaced with the color assigned to it in colors dict>",
            ...
        ],
        "<glyph>": [
            "<pixels as characters for each line. They will be replaced with the color assigned to it in colors dict>",
            ...
        ],
        ...
    }

    Arguments:
        json_font_path (str): Path to the json file.
        font_name (str): Name of the font.

    Exceptions:
        JSONDecodeError: json file is invalid
        FontError: If the json files' structure is invalid

    """

    global fonts, font_colors

    with open(json_font_path, 'r') as f:
        _current_font = json_load(f.read())

    if 'colors' not in _current_font.keys():
        raise FontError(f"Color mappings for json font not found when loading {font_name}.")

    if 'none' not in _current_font.keys():
        raise FontError(f"No glyph for unknown characters found when loading {font_name}.")

    font_colors.update({font_name: _current_font.pop('colors')})
    fonts.update({font_name: {k: [[ font_colors[font_name][char] for char in s] for s in a] for k, a in _current_font.items()}})


load_font(os.path.join(BRCI_CWD, 'resources', 'font.json'), 'default')


def generate_text_bitmap(text: str, size_x: int = 256, size_y: int = 256, scale: int = 3, background: Optional[list[int]] = None, font: str = 'default') -> list[list[ list[int] ]]:

    """
    Will convert text to a grid of RGBA values.
    """

    used_font: dict[str, list[list[ list[int] ]]] = fonts[font]
    used_colors = {char: col.copy() for char, col in font_colors[font].items()}  # faster than deepcopy
    if background is None:
        background_col = font_colors[font][' ']
    else:
        background_col = background
        used_colors[' '] = background
    position: int = 2 * scale
    text_height: int = len(used_font['none']) * scale
    lines: list[list[ list[int] ]] = [[background_col] * position for _ in range(text_height)]
    right_padding: int = position  # = 2 * padding. micro optimisation goes brrr
    is_auto_new_line: bool = False
    for char in text:
        if is_auto_new_line and char == ' ':
            continue
        else:
            is_auto_new_line = False
        printed_char: list[list[ list[int] ]] = [[pixel for pixel in line for _ in range(scale)] for line in used_font[char] for _ in range(scale)] if char in used_font else used_font['none']
        if char == '\n' or position + len(printed_char[0]) > size_x - right_padding:
            for i in range(text_height):
                lines[-text_height + i].extend([background_col] * (size_x - len(lines[-text_height + i])))
            position = 2 * scale
            lines.extend([[background_col] * position for _ in range(text_height)])
            if char == ' ':
                is_auto_new_line = True
                continue
            if char == '\n':
                continue
        for i, line in enumerate(printed_char):
            lines[-text_height + i].extend(line)
        position += len(printed_char[0])
    for i in range(text_height):
        lines[-text_height + i].extend([background_col] * (size_x - len(lines[-text_height + i])))

    if len(lines) > size_y:
        return lines[:size_y]
    # else:
    lines.extend([[background_col] * size_x] * (size_y - len(lines)))
    return lines

def crc32(data):
    return zlib_crc32(data) & 0xffffffff


# --------------------    LOGGING    -------------------- #


def logwrap(level: Literal["info", "debug", "warning", "error", "critical"], msg: str) -> str:
    """A special function in place of the regular `logging` calls, as to not raise errors if `logging` is not found.

    Arguments:
        level (Literal["info", "debug", "warning", "error", "critical"]): The log level.
        msg (str): The message to log.

    Returns:
        str: The message logged. Good for using this function in print statements, function calls, variables, etc.
    """

    if we_have_logging:
        match level:
            case "info":
                logger.info(msg)
            case "debug":
                logger.debug(msg)
            case "warning":
                logger.warning(msg)
            case "error":
                logger.error(msg)
            case "critical":
                logger.critical(msg)
            case _:
                # Not a valid log level. Default to info with a warning message.
                logger.info(f"(Note: Invalid log level '{level}'!) || {msg}")
    else:
        print("Logwrap called, but logging disabled...")

    return msg


# ------------------- TIME-RELATED FUNCTIONS -------------------- #


def get_time_100ns() -> int:

    """
    Get the current time in hundreds of nanoseconds. Notably used in metadata and for BRCI backups.

    Returns:
        int: 100s of nanoseconds since 0001-01-01 00:00:00

    Exceptions:
        OSError: Failed to retrieve time
        OverflowError: Time is set past 8639-12-17 23:59:59. In this case BRCI is not your least concern.
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

    Arguments:
        name (str): Name of the folder.
        is_nt (bool): True if we are working with NT, otherwise False (POSIX). Can be checked using `os.name == 'nt'`

    Returns:
        bool: True if the folder name is valid, otherwise False

    Exceptions:
        TypeError: name is not a string or is_nt is not a boolean
    """

    if not type(name) == str:
        raise TypeError("Folder name must be a string")

    if not type(is_nt) == bool:
        raise TypeError("is_nt must be a boolean")


    if is_nt:
        # Check for NT system validity
        # nt_match = r'[<>:"/\\|?*]'  # TODO figure out a better solution for path issues

        nt_match = r'[<>:"/|?*]'
        
        #
        #if re.search(nt_match, name): print("fuck you regex")
        #if len(name) == 0: print("fuck you len")
        #if set(name) == set(): print("fuck you sets")
        #if name[-1] in {'.', ' '}: print("fuck you last character")
        #if name in (
        #        "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        #        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"): print("fuck you banned strs")
        # Making these lines comments because I felt like it, and because it was a massive block of neon green string text for me :bob_troll:
        
        bad_folder_names = ("CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3",
                "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7",
                "LPT8", "LPT9") # Technically EVER SO SLIGHTLY less efficient to make this a full variable, but screw you, fight with me over it. More readable.

        if (re.search(nt_match, name[2:] if len(name) > 1 and name[1] == ':' else name) or
                len(name) == 0 or
                set(name) == set() or
                name[-1] in {'.', ' '} or
                name in bad_folder_names):
            # This name is invalid. Return False.
            logwrap("warning", f"NT directory name check *failed*. Dirname: {name}")
            # If you have an issue with logs being here, let me know. These will help with debugging.
            # If you want to disable logs in random areas like these, they're usually set to debug, just set the logger to a higher level to filter them out.
            return False
        else:
            # Once again, let me know.
            logwrap("info", f"NT directory name check *passed*. Dirname: {name}")

    else:
        # Check for POSIX system validity
        posix_match = r'[<>:"/\\|?*\x00-\x1F]'
        if re.search(posix_match, name) or len(name) == 0 or set(name) == set():
            logwrap("warning", f"POSIX directory name check *failed*. Dirname: {name}")
            return False
        else:
            logwrap("info", f"POSIX directory name check *passed*. Dirname: {name}")

    # else: valid
    return True
