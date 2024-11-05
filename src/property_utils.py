from typing import Final, Literal, Optional
from .utils import FM, settings
import colorsys


# -------------------- LENGTH UNIT CONVERSION -------------------------


class Units:

    """
    Units class for BRCI-D.

    :var UE_UNIT: Length unit used in Unreal Engine. (0.01m)
    :var THIRD, STUD: Length of a third of a brick (0.1m)
    :var BRICK: Length of a brick (0.3m)

    :var KILOMETER, KM: (1_000m)
    :var HECTOMETER, HM: (100m)
    :var DECAMETER, DAM: (10m)
    :var METER, M: (1m)
    :var DECIMETER, DM: (0.1m)
    :var CENTIMETER, CM: (0.01m)
    :var MILLIMETER, MM: (0.001m)
    :var MICROMETER, UM: (0.000_001m)

    :var LEAGUE, LEA: (4_828.032m)
    :var NAUTICAL_MILE, NMI: (1_852m)
    :var MILE, MI: (1_609.344m)
    :var FURLONG, FUR: (201.168m)
    :var CABLE: (185.2m)
    :var CHAIN, CH: (20.116_8m)
    :var ROD, POLE, PERCH: (5.029_2m)
    :var FATHOM, FTH: (1.852m)
    :var YARD, YD: (0.914_4m)
    :var FOOT, FEET, FT: (0.304_8m)
    :var LINK: (0.201_168m)
    :var HAND, HH: (0.101_6m)
    :var INCH, IN: (0.025_4m)
    :var BARLEYCORN: (0.008_466_666_6...m)
    :var FRENCH_PICA, CICERO: (0.004_511_658_1m)
    :var AMERICAN_PICA: (0.004_217_416m)
    :var COMPUTER_PICA, PICA: (0.004_233_333_3...m)
    :var LINE, L: (0.002_166_666_6...m)
    :var THOU, MIL, TH: (0.000_025_4m)
    :var TWIP: (0.000_017_638_9m)

    :var PARSEC, PC: (30_856_775_814_913_673m)
    :var LIGHT_YEAR, LY: (9_460_730_472_580_800m)
    :var LIGHT_DAY, LD: (259_020_683_712_000m)
    :var LIGHT_HOUR, LH: (10_792_528_488_000m)
    :var ASTRONOMICAL_UNIT, AU: (149_597_870_700m)
    :var LIGHT_MINUTE, LM: (179_875_474_800m)
    :var LIGHT_SECOND, LS: (299_792_458m)
    :var LIGHT_MILLISECOND, LMS: (299_792.458m)
    :var LIGHT_MICROSECOND, LUS: (299.792_458m)
    :var LIGHT_NANOSECOND, LNS: (0.299_792_458m)
    :var LIGHT_PICOSECOND, LPS: (0.000_299_792_458m)
    """

    # Brick rigs & Unreal Engine
    UE_UNIT: Final[float] = 0.01
    THIRD: Final[float] = 0.1
    STUD = THIRD
    BRICK: Final[float] = 0.3

    # Metric & SI-Related
    KILOMETER: Final[float] = 1_000.0
    KM = KILOMETER  # Alias
    HECTOMETER: Final[float] = 100.0
    HM = HECTOMETER  # Alias
    DECAMETER: Final[float] = 10.0
    DAM = DECAMETER  # Alias
    METER: Final[float] = 1.0
    M = METER  # Alias
    DECIMETER: Final[float] = 0.1
    DM = DECIMETER  # Alias
    CENTIMETER: Final[float] = 0.01
    CM = CENTIMETER  # Alias
    MILLIMETER: Final[float] = 0.001
    MM = MILLIMETER  # Alias
    MICROMETER: Final[float] = 0.000001
    UM = MICROMETER  # Alias

    # Imperial
    LEAGUE: Final[float] = 4828.032
    LEA = LEAGUE  # Alias
    NAUTICAL_MILE: Final[float] = 1_852
    NMI = NAUTICAL_MILE  # Alias
    MILE: Final[float] = 1_609.344
    MI = MILE  # Alias
    FURLONG: Final[float] = 201.168
    FUR = FURLONG  # Alias
    CABLE: Final[float] = 185.2
    CHAIN: Final[float] = 20.1168
    CH = CHAIN  # Alias
    ROD: Final[float] = 5.0292
    PERCH = POLE = ROD  # Alias
    FATHOM = 1.852
    FTH = FATHOM
    YARD: Final[float] = 0.9144
    YD = YARD  # Alias
    FOOT: Final[float] = 0.3048
    FT = FEET = FOOT  # Alias
    LINK: Final[float] = 0.201168
    HAND: Final[float] = 0.1016
    HH = HAND  # Alias
    INCH: Final[float] = 0.0254
    IN = INCH  # Alias
    BARLEYCORN: Final[float] = INCH / 3
    FRENCH_PICA: Final[float] = 0.0045116581
    CICERO = FRENCH_PICA  # Alias
    AMERICAN_PICA: Final[float] = INCH * 400 / 2409
    COMPUTER_PICA: Final[float] = INCH / 6
    PICA = COMPUTER_PICA  # Alias
    LINE: Final[float] = INCH / 12
    L = LINE  # Alias
    THOU: Final[float] = INCH / 1_000
    MIL = TH = THOU  # Alias
    TWIP: Final[float] = 0.0000176389

    # Astronomical (length)
    PARSEC: Final[float] = 3.085_677_581_4e16
    PC = PARSEC  # Alias
    LIGHT_YEAR: Final[float] = 9_460_730_472_580_800.0
    LY = LIGHT_YEAR  # Alias
    LIGHT_DAY: Final[float] = 25_902_068_371_200.0
    LD = LIGHT_DAY  # Alias
    LIGHT_HOUR: Final[float] = LIGHT_DAY / 24
    LH = LIGHT_HOUR  # Alias
    ASTRONOMICAL_UNIT: Final[float] = 149_597_870_700.0
    AU = ASTRONOMICAL_UNIT  # Alias
    LIGHT_MINUTE: Final[float] = LIGHT_HOUR / 60
    LM = LIGHT_MINUTE  # Alias
    LIGHT_SECOND: Final[float] = LIGHT_MINUTE / 60
    LS = LIGHT_SECOND  # Alias
    LIGHT_MILLISECOND: Final[float] = LIGHT_SECOND / 1000
    LMS = LIGHT_MILLISECOND  # Alias
    LIGHT_MICROSECOND: Final[float] = LIGHT_MILLISECOND / 1000
    LUS = LIGHT_MICROSECOND  # Alias
    LIGHT_NANOSECOND: Final[float] = LIGHT_MICROSECOND / 1000
    LNS = LIGHT_NANOSECOND  # Alias
    LIGHT_PICOSECOND: Final[float] = LIGHT_NANOSECOND / 1000
    LPS = LIGHT_PICOSECOND  # Alias


def convert_len(value: float | int | list[float | int], old_unit: float | int, new_unit: float | int) -> float | list[float]:

    """
    Convert a value or list of values from one unit to another.

    :param value:
    :param old_unit:
    :param new_unit:
    :return:
    """


    # Need to import it each time to update it


    # Check if old_unit is a float or int
    if not isinstance(old_unit, (float, int)):

        # Signal there's something wrong
        FM.error("Old unit must be a float or int.", "Old unit must be a float or int, being how many "
                 f"meters one of the unit is. \nOld unit is set to: {old_unit!r} (type: {type(old_unit).__name__}).")

        # See if we can fix the issue (if the user wants to)
        if settings['attempt_error_mitigation']:
            try:
                old_unit = float(old_unit)
                FM.success(f"Old unit was interpreted as: {old_unit!r} (type: {type(old_unit).__name__})")
            except ValueError:
                raise ValueError(f"Old unit must be a float or int. Error mitigation failed.")

        else:
            raise ValueError("Old unit must be a float or int.")

    # Do the same for new_unit
    if not isinstance(new_unit, (float, int)):

        # Signal there's something wrong
        FM.error("New unit must be a float or int.", "New unit must be a float or int, being how many "
                 f"meters one of the unit is. \nNew unit is set to: {new_unit!r} (type: {type(new_unit).__name__}).")

        # See if we can fix the issue (if the user wants to)
        if settings['attempt_error_mitigation']:
            try:
                new_unit = float(new_unit)
                FM.success(f"New unit was interpreted as: {new_unit!r} (type: {type(new_unit).__name__})")
            except ValueError:
                raise ValueError(f"New unit must be a float or int. Error mitigation failed.")

        else:
            raise ValueError("New unit must be a float or int.")


    # If it's a value we convert it to the new unit
    if isinstance(value, (float, int)):
        return value / new_unit * old_unit

    # Else if it's a list we convert each value to the new unit
    elif isinstance(value, list):
        return [v / new_unit * old_unit for v in value]

    # else:
    raise ValueError("Value must be a float, int or list of floats and ints." +
                     (" Error mitigation failed." if settings['attempt_error_mitigation'] else ""))


# Function to calculate position of a brick from any unit
def pos(value: float | int | list[float | int], unit: float | int = Units.METER) -> float | list[float]:

    """
    Function to convert position (or distance*) of a brick from any unit to the unit Brick Rigs use.

    :param value: Value to convert.
    :param unit: Old unit.

    :return: Converted value.
    :rtype: float | list[float]
    """

    return convert_len(value, unit, Units.UE_UNIT)


# Function to calculate size of a brick from any unit
def size(brick_size: float | int | list[float | int], unit: float | int = Units.METER) -> float | list[float]:

    """
    Function to convert size (or length*) of a brick from any unit to the unit Brick Rigs use.

    :param brick_size: Value to convert.
    :param unit: Old unit.

    :return: Converted value.
    :rtype: float | list[float]
    """

    return convert_len(brick_size, unit, Units.THIRD)


# -------------------- COLORS --------------------

_SUPPORTED_COLOR_SPACES: Final[set[str]] = {'rgb', 'hsl', 'hsv', 'cmyk'}

def convert_color(color: list[float | int] | tuple[float | int, ...],
                  color_space: Literal['rgb', 'hsl', 'hsv', 'cmyk'], new_color_space: Literal['rgb', 'hsl', 'hsv', 'cmyk'],
                  alpha: bool, old_max: float | int = 255.0, new_max: float | int = 255.0) -> list[int]:


    # Need to import it each time to update it


    """
    Convert color from a color space to another

    :param color: List of each channel of the RGB(A) color.
    :param color_space: Color space of the color. Either 'rgb', 'hsl', 'hsv', or 'cmyk'.
    :param new_color_space: Color space of the new color. Either 'rgb', 'hsl', 'hsv', or 'cmyk'.
    :param alpha: Whether the color has an additional alpha channel
    :param old_max: Maximum value of the given color. old_max = 123 -> e.g. white -> [123, 123, 123] / [123, 123, 123, 123]
    :param new_max: Maximum value of the new color. new_max = 123 -> e.g. white -> [123, 123, 123] / [123, 123, 123, 123]

    :return: Color converted to the new color space
    """


    # ----- ERROR CHECKING

    # Check if color is right
    # Is a list
    if not isinstance(color, (list, tuple)):

        # Signal there's something wrong
        FM.error("Color must be a list.",
                 f"Color must be a list of floats or ints. \nColor is set to: {color!r} (type: {type(color).__name__}).")

        # See if we can fix the issue (if the user wants to)
        if settings['attempt_error_mitigation']:
            try:
                color = tuple(color)
                FM.success(f"Color was interpreted as: {color!r} (type: {type(color).__name__})")
            except ValueError:
                raise ValueError(f"Color must be a list. Error mitigation failed.")

        else:
            raise ValueError("Color must be a list.")

    # If color is of the right length
    if len(color) != len(color_space) + alpha:

        # Signal there's something wrong
        FM.error(f"Colors in {color_space + ('(a)' if alpha else '')} must be a list of length {len(color_space) + alpha}.",
                 f"Color must be a list of floats or ints. \nColor is set to: {color!r} (type: {type(color).__name__}).")

        # See if we can fix the issue (if the user wants to)
        if settings['attempt_error_mitigation']:
            try:
                # Adjust color to be of the right length
                color = color[:len(color_space) + alpha]
                color = color + [0.0] * ((len(color_space) + alpha) - len(color))

                FM.success(f"Color was interpreted as: {color!r} (type: {type(color).__name__})")
            except ValueError:
                raise ValueError(f"Color must be a list of length 3 or 4. Error mitigation failed.")

        else:
            raise ValueError("Color must be a list of length 3 or 4.")

    # Is all floats or integers
    if not all(isinstance(v, (float, int)) for v in color):

        # Signal there's something wrong
        FM.error("Color must be a list of floats or ints.",
                 f"Color must be a list of floats or ints. \nColor is set to: {color!r} (type: {type(color).__name__}).")

        # See if we can fix the issue (if the user wants to)
        if settings['attempt_error_mitigation']:
            try:
                color = [float(v) for v in color]
                FM.success(f"Color was interpreted as: {color!r} (type: {type(color).__name__})")
            except ValueError:
                raise ValueError(f"Color must be a list of floats or ints. Error mitigation failed.")

        else:
            raise ValueError("Color must be a list of floats or ints.")


    # Check if color spaces are right
    if color_space not in _SUPPORTED_COLOR_SPACES:

        # Signal there's something wrong
        FM.error(f"Non supported color space: {color_space!r}.",
                 f"Color space must be one of {', '.join([repr(space) for space in _SUPPORTED_COLOR_SPACES])}.\n"
                 f"Color space is set to: {color_space!r} (type: {type(color_space).__name__}).")

        # See if we can fix the issue (if the user wants to)
        if settings['attempt_error_mitigation']:
            try:
                color_space = color_space[:-1]
                if color_space in _SUPPORTED_COLOR_SPACES:
                    FM.success(f"Color space was interpreted as: {color_space!r} (type: {type(color_space).__name__})")
                else: raise ValueError
            except ValueError:
                raise ValueError(f'Non supported color space: {color_space!r}. Error mitigation failed.')

        else:
            raise ValueError(f'Non supported color space: {color_space!r}.')

    if new_color_space not in _SUPPORTED_COLOR_SPACES:

        # Signal there's something wrong
        FM.error(f"Non supported color space: {new_color_space!r}.",
                 f"Color space must be one of {', '.join([repr(space) for space in _SUPPORTED_COLOR_SPACES])}.\n"
                 f"Color space is set to: {new_color_space!r} (type: {type(new_color_space).__name__}).")

        # See if we can fix the issue (if the user wants to)
        if settings['attempt_error_mitigation']:
            try:
                new_color_space = new_color_space[:-1]
                if new_color_space in _SUPPORTED_COLOR_SPACES:
                    FM.success(f"Color space was interpreted as: {new_color_space!r} (type: {type(new_color_space).__name__})")
                else: raise ValueError
            except ValueError:
                raise ValueError(f'Non supported color space: {new_color_space!r}. Error mitigation failed.')

        else:
            raise ValueError(f'Non supported color space: {new_color_space!r}.')

    # Check if alpha and max parameters have teh right type (bool, float | int, float | int)
    if not isinstance(alpha, bool):

        # Signal there's something wrong
        FM.error("Alpha must be a boolean.",
                 f"Alpha is set to: {alpha!r} (type: {type(alpha).__name__}).")

        # See if we can fix the issue (if the user wants to)
        if settings['attempt_error_mitigation']:
            try:
                alpha = bool(alpha)
                FM.success(f"Alpha was interpreted as: {alpha!r} (type: {type(alpha).__name__})")
            except ValueError:
                raise ValueError(f"Alpha must be a boolean. Error mitigation failed.")

        else:
            raise ValueError("Alpha must be a boolean.")

    if not isinstance(old_max, (float, int)):

        # Signal there's something wrong
        FM.error("Old max must be a float or int.",
                 f"Old max is set to: {old_max!r} (type: {type(old_max).__name__}).")

        # See if we can fix the issue (if the user wants to)
        if settings['attempt_error_mitigation']:
            try:
                old_max = float(old_max)
                FM.success(f"Old max was interpreted as: {old_max!r} (type: {type(old_max).__name__})")
            except ValueError:
                raise ValueError(f"Old max must be a float or int. Error mitigation failed.")

        else:
            raise ValueError("Old max must be a float or int.")

    if not isinstance(new_max, (float, int)):

        # Signal there's something wrong
        FM.error("New max must be a float or int.",
                 f"New max is set to: {new_max!r} (type: {type(new_max).__name__}).")

        # See if we can fix the issue (if the user wants to)
        if settings['attempt_error_mitigation']:
            try:
                new_max = float(new_max)
                FM.success(f"New max was interpreted as: {new_max!r} (type: {type(new_max).__name__})")
            except ValueError:
                raise ValueError(f"New max must be a float or int. Error mitigation failed.")

        else:
            raise ValueError("New max must be a float or int.")


    # ----- CONVERTING COLOR

    # Separating alpha
    a: float | int | None = int(color[-1] / old_max * new_max) if alpha else None
    treated_color: list[float] = [float(col / old_max) for col in (color[:-1] if alpha else color)]

    # CONVERTING TO RGB(A)
    rgb_color: list[float] | tuple[float, ...] = tuple()

    # RGB color space -> nothing to do
    if color_space == 'rgb':

        rgb_color = treated_color

    # HSV color space
    elif color_space == 'hsv':

        # Convert to RGB
        rgb_color = colorsys.hsv_to_rgb(*treated_color)

    # HSL color space
    elif color_space == 'hsl':

        rgb_color = colorsys.hls_to_rgb(treated_color[0], treated_color[2], treated_color[1])

    # CMYK color space (no package!)
    elif color_space == 'cmyk':

        rgb_color = [0, 0, 0]
        c, m, y, k = treated_color
        rgb_color[0] = (1 - c) * (1 - k)
        rgb_color[1] = (1 - m) * (1 - k)
        rgb_color[2] = (1 - y) * (1 - k)


    # CONVERTING TO NEW COLOR SPACE
    output: list[int] = []

    # RGB color space -> nothing to do
    if new_color_space == 'rgb':

        pass

    # HSV color space
    elif new_color_space == 'hsv':

        output = [int(col * new_max) for col in colorsys.rgb_to_hsv(*rgb_color)]

    # HSL color space
    elif new_color_space == 'hsl':

        output = [int(col * new_max) for col in colorsys.rgb_to_hls(*rgb_color)]
        output[1], output[2] = output[2], output[1]

    # CMYK color space
    elif new_color_space == 'cmyk':

        # Setup variables & calculate key
        r, g, b = rgb_color
        k = 1 - max(r, g, b)
        output = [0, 0, 0, k]

        if k != 1:  # If it's 1 then it's 0, 0, 0, 0, which is initialized by default

            # Colors
            output[0] = (1 - r - k) / (1 - k)
            output[1] = (1 - g - k) / (1 - k)
            output[2] = (1 - b - k) / (1 - k)

        # Put back in right range
        output = [int(col * new_max) for col in output]


    # Adding alpha
    if a is not None:
        output.append(a)

    return output



def rgb(color: list[float | int], old_max: float = 255.0) -> list[int]:

    """
    Convert from RGB(A) (depending on the length of the list) to HSV(A) (which Brick Rigs uses for colors)

    :param color: List of each channel of the RGB(A) color.
    :param old_max: Maximum value of the RGB(A) color. old_max = 123 -> e.g. white -> [123, 123, 123] / [123, 123, 123, 123]

    :return: List of each channel of the HSV(A) color.
    """

    alpha: bool = False
    if len(color) == 4:
        alpha = True

    return convert_color(color, 'rgb', 'hsv', alpha, old_max)


def hsv(color: list[float | int], old_max: float = 255.0) -> list[int]:


    # Need to import it each time to update it


    if not isinstance(color, list):

        # Signal there's something wrong
        FM.error("Color must be a list.",
                 f"Color is: {color!r} (type: {type(color).__name__}).")

        # See if we can fix the issue (if the user wants to)
        if settings['attempt_error_mitigation']:
            try:
                color = list(color)
                FM.success(f"Color was interpreted as: {color!r} (type: {type(color).__name__})")
            except ValueError:
                raise ValueError(f"Color must be a list. Error mitigation failed.")

        else:
            raise ValueError("Color must be a list.")


    if not 3 < len(color) <= 4:

        # Signal there's something wrong
        FM.error("Color must be a list of 3 or 4 floats or integers.",
                 f"Color is: {color!r} (type: {type(color).__name__}).")

        # Error mitigation is impossible
        raise ValueError("Color must be a list of 3 or 4 elements." +
                         (" Error mitigation failed." if settings['attempt_error_mitigation'] else ""))


    if not all(isinstance(col, (float, int)) for col in color):

        # Signal there's something wrong
        FM.error("Color must be a list of 3 or 4 floats or integers.",
                 f"Color is: {color!r} (type: {type(color).__name__}).")

        # See if we can fix the issue (if the user wants to)
        if settings['attempt_error_mitigation']:
            try:
                color = [float(col) for col in color]
                FM.success(f"Color was interpreted as: {color!r} (type: {type(color).__name__})")
            except ValueError:
                raise ValueError(f"Color must be a list of 3 or 4 floats or integers. Error mitigation failed.")

        else:
            raise ValueError("Color must be a list of 3 or 4 floats or integers.")


    return [int(col / old_max * 255) for col in color]


def hsl(color: list[float | int], old_max: float = 255.0) -> list[int]:

    """
    Convert from HSL(A) (depending on the length of the list) to HSV(A) (which Brick Rigs uses for colors)

    :param color: List of each channel of the HSL(A) color.
    :param old_max: Maximum value of the HSL(A) color. old_max = 123 -> e.g. white -> [0, 0, 123] / [0, 0, 123, 123]

    :return: List of each channel of the HSV(A) color.
    """

    alpha: bool = False
    if len(color) == 4:
        alpha = True

    return convert_color(color, 'hsl', 'hsv', alpha, old_max)


def cmyk(color: list[float | int], old_max: float = 255.0) -> list[int]:

    """
    Convert from CMYK(A) (depending on the length of the list) to HSV(A) (which Brick Rigs uses for colors)

    :param color: List of each channel of the CMYK(A) color.
    :param old_max: Maximum value of the CMYK(A) color. old_max = 123 -> e.g. black -> [0, 0, 0, 123] / [0, 0, 0, 123, 123]

    :return: List of each channel of the HSV(A) color.
    """

    alpha: bool = False
    if len(color) == 5:
        alpha = True

    return convert_color(color, 'cmyk', 'hsv', alpha, old_max)




# -------------------- BRICK INPUTS --------------------

def brick_input14(prop_name: str, input_type: str, value: float | int = 1.0, source_bricks: Optional[list[str]] = None) -> dict[str, float | int | list[str]]:

    """
    Converts a list of arguments into a list of properties corresponding to brick inputs to provide similarity with BRCI-C.
    Same as `brci.BrickInput14()`

    :param prop_name: Name of the property, e.g. `'EnabledInputChannel'`
    :param input_type: Type of the input
    :param value: Value of the input
    :param source_bricks: List of source bricks
    :return: List of properties
    """

    return {
        f'{prop_name}.InputAxis': input_type,
        f'{prop_name}.SourceBricks': [] if source_bricks is None else source_bricks,
        f'{prop_name}.Value': value
    }


# Since BrickInput() originates from a class:
#noinspection PyPep8Naming
def BrickInput14(prop_name: str, input_type: str, value: float | int = 1.0, source_bricks: Optional[list[str]] = None) -> dict[str, float | int | list[str]]:

    return brick_input14(prop_name, input_type, value, source_bricks)