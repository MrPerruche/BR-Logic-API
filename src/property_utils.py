from typing import Final, Literal, Optional
from .utils import FM, settings
import colorsys


# -------------------- LENGTH UNIT CONVERSION -------------------------


class Units:

    """
    Units class for BRCI-D.

    Variables:
        UE_UNIT (Final[float]): Length unit used in Unreal Engine. (0.01m)
        THIRD, STUD, SUB_UNIT (Final[float]): Length of a third of a brick (0.1m)
        BRICK, UNIT (Final[float]): Length of a brick (0.3m)

        QUETTA (float): Metric prefix adopted in 2022. (×10^30)
        RONNA (float): Metric prefix adopted in 2022. (×10^27)
        YOTTA (float): Metric prefix adopted in 1991. (×10^24)
        ZETTA (float): Metric prefix adopted in 1991. (×10^21)
        EXA (float): Metric prefix adopted in 1975. (×10^18)
        PETA (float): Metric prefix adopted in 1975. (×10^15)
        TERA (float): Metric prefix adopted in 1960. (×10^12)
        GIGA (float): Metric prefix adopted in 1960. (×10^9)
        MEGA (float): Metric prefix adopted in 1873. (×10^6)
        KILO (float): Metric prefix adopted in 1795. (×10^3)
        HECTO (float): Metric prefix adopted in 1795. (×10^2)
        DECA (float): Metric prefix adopted in 1795. (×10^1)
        DECI (float): Metric prefix adopted in 1795. (×10^-1)
        CENTI (float): Metric prefix adopted in 1795. (×10^-2)
        MILLI (float): Metric prefix adopted in 1795. (×10^-3)
        MICRO (float): Metric prefix adopted in 1873. (×10^-6)
        NANO (float): Metric prefix adopted in 1960. (×10^-9)
        PICO (float): Metric prefix adopted in 1960. (×10^-12)
        FEMTO (float): Metric prefix adopted in 1964. (×10^-15)
        ATTO (float): Metric prefix adopted in 1964. (×10^-18)
        ZEPTO (float): Metric prefix adopted in 1991. (×10^-21)
        YOCTO (float): Metric prefix adopted in 1991. (×10^-24)
        RONTO (float): Metric prefix adopted in 2022. (×10^-27)
        QUECTO (float): Metric prefix adopted in 2022. (×10^-30)

        KILOMETER, KM (float): A thousand meters. (1_000m)
        HECTOMETER, HM (float): A hundred meters. (100m)
        DECAMETER, DAM (float): Ten meters. (10m)
        METER, M (float): Defined as the distance light travels in 1/299_792_458 of a second. (1m)
        DECIMETER, DM (float): A tenth of a meter. (0.1m)
        CENTIMETER, CM (float): A centimeter. (0.01m)
        MILLIMETER, MM (float): A millimeter. (0.001m)
        MICROMETER, UM (float): A micrometer. (0.000_001m)

        LEAGUE, LEA (float): (4_828.032m)
        NAUTICAL_MILE, NMI (float): (1_852m)
        MILE, MI (float): (1_609.344m)
        FURLONG, FUR (float): (201.168m)
        CABLE (float): (185.2m)
        CHAIN, CH (float): (20.116_8m)
        ROD, POLE, PERCH (float): (5.029_2m)
        FATHOM, FTH (float): (1.852m)
        YARD, YD (float): (0.914_4m)
        FOOT, FEET, FT (float): (0.304_8m)
        LINK (float): (0.201_168m)
        HAND, HH (float): (0.101_6m)
        INCH, IN (float): (0.025_4m)
        BARLEYCORN (float): (0.008_466_666_6...m)
        FRENCH_PICA, CICERO (float): (0.004_511_658_1m)
        AMERICAN_PICA (float): (0.004_217_416m)
        COMPUTER_PICA, PICA (float): (0.004_233_333_3...m)
        LINE, L (float): (0.002_166_666_6...m)
        THOU, MIL, TH (float): (0.000_025_4m)
        TWIP (float): (0.000_017_638_9m)

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

    # Metric Prefixes
    QUETTA: Final[float] = 1e30
    RONNA: Final[float] = 1e27
    YOTTA: Final[float] = 1e24
    ZETTA: Final[float] = 1e21
    EXA: Final[float] = 1e18
    PETA: Final[float] = 1e15
    TERA: Final[float] = 1e12
    GIGA: Final[float] = 1e9
    MEGA: Final[float] = 1e6
    KILO: Final[float] = 1e3
    HECTO: Final[float] = 100
    DECA: Final[float] = 10
    DECI: Final[float] = 0.1
    CENTI: Final[float] = 0.01
    MILLI: Final[float] = 1e-3
    MICRO: Final[float] = 1e-6
    NANO: Final[float] = 1e-9
    PICO: Final[float] = 1e-12
    FEMTO: Final[float] = 1e-15
    ATTO: Final[float] = 1e-18
    ZEPTO: Final[float] = 1e-21
    YOCTO: Final[float] = 1e-24
    RONTO: Final[float] = 1e-27
    QUECTO: Final[float] = 1e-30


    # Brick rigs & Unreal Engine
    UE_UNIT: Final[float] = 0.01
    THIRD: Final[float] = 0.1
    SUB_UNIT = STUD = THIRD
    BRICK: Final[float] = 0.3
    UNIT = BRICK

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
    Convert a value or list of values from one unit to another. Both unit arguments must be use the same unit.

    Arguments:
        value: Value or list of values to convert.
        old_unit: Old unit.
        new_unit: New unit.

    Returns:
        float | int | list[float | int]: Converted value(s)

    Exceptions:
        TypeError: If one of the arguments is of an unexpected type.
    """


    # Need to import it each time to update it

    if type(value) in (list, tuple, set, frozenset) and {type(v) for v in value} - {float, int} != set():

        raise TypeError("Value must be a float, int or list of floats and ints.")

    elif type(value) not in (float, int):

        raise TypeError("Value must be a float, int or list of floats and ints.")

    if not type(old_unit) in (float, int):

        raise TypeError("Old unit must be a float or int.")

    if not type(new_unit) in (float, int):

        raise TypeError("New unit must be a float or int.")


    # If it's a value we convert it to the new unit
    if isinstance(value, (float, int)):
        return value / new_unit * old_unit

    # Else if it's a list we convert each value to the new unit
    elif isinstance(value, (list, tuple, set, frozenset)):
        return [v / new_unit * old_unit for v in value]

    # else:
    raise TypeError("Converting provided value(s) failed unexpectedly.")


# Function to calculate position of a brick from any unit
def pos(value: float | int | list[float | int], unit: float | int = Units.METER) -> float | list[float]:

    """
    Function to convert position (or distance*) of a brick from any unit to the unit Brick Rigs use.

    Arguments:
        value: Value or list of values to convert.
        unit: Unit of provided values.

    Returns:
        Converted value.

    Exceptions:
        TypeError: If one of the arguments is of an unexpected type.
    """

    return convert_len(value, unit, Units.UE_UNIT)


# Function to calculate size of a brick from any unit
def size(brick_size: float | int | list[float | int], unit: float | int = Units.METER) -> float | list[float]:

    """
    Function to convert size of a brick from any unit to the unit Brick Rigs use.

    Arguments:
        brick_size: Value or list of values to convert.
        unit: Unit of provided values.

    Returns:
        Converted value.

    Exceptions:
        TypeError: If one of the arguments is of an unexpected type.
    """

    return convert_len(brick_size, unit, Units.THIRD)


# -------------------- COLORS --------------------

SUPPORTED_COLOR_SPACES: Final[set[str]] = {'rgb', 'hsl', 'hsv', 'cmyk'}

def convert_color(color: list[float | int] | tuple[float | int, ...],
                  color_space: Literal['rgb', 'hsl', 'hsv', 'cmyk'], new_color_space: Literal['rgb', 'hsl', 'hsv', 'cmyk'],
                  alpha: bool, old_max: float | int = 255.0, new_max: float | int = 255.0) -> list[int]:

    """
    Convert color from a color space to another

    Arguments:
        color (list[float | int] | tuple[float | int, ...]): List of each channel of the color.
        color_space (Literal['rgb', 'hsl', 'hsv', 'cmyk']): Color space of the color.
        new_color_space (Literal['rgb', 'hsl', 'hsv', 'cmyk']): Color space of the new color.
        alpha (bool): Whether the color has an additional alpha channel
        old_max (float | int): Maximum value of the given color. old_max = 123 -> e.g. white -> [123, 123, 123] / [123, 123, 123, 123]
        new_max (float | int): Maximum value of the new color. new_max = 123 -> e.g. white -> [123, 123, 123] / [123, 123, 123, 123]

    Returns:
        Color converted to the new color space.

    Exceptions:
        TypeError: If one of the arguments is of an unexpected type.
        ValueError: If the color space or new color space is not supported.
    """


    # ----- ERROR CHECKING

    # Check if color is right
    # Is a list
    if not type(color) in (list, tuple):
        raise TypeError("Color must be a list.")

    # If color is of the right length
    if len(color) != len(color_space) + alpha:

        raise TypeError("Color must be a list of length 3 or 4.")

    # Is all floats or integers
    if not all(type(v) in (float, int) for v in color):

        raise TypeError("Color must be a list of floats or integers.")


    # Check if color spaces are right
    if color_space not in SUPPORTED_COLOR_SPACES:

        raise ValueError(f"Color space must be one of {', '.join([repr(space) for space in SUPPORTED_COLOR_SPACES])}.")

    if new_color_space not in SUPPORTED_COLOR_SPACES:

        raise ValueError(f"New color space must be one of {', '.join([repr(space) for space in SUPPORTED_COLOR_SPACES])}.")

    # Check if alpha and max parameters have teh right type (bool, float | int, float | int)
    if not type(alpha) == bool:

        raise TypeError("Alpha must be a boolean.")

    if not type(old_max) in (float, int):

        raise TypeError("Old max must be a float or int.")

    if not type(new_max) in (float, int):

        raise TypeError("New max must be a float or int.")


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

    Arguments:
        color (list[float | int]): List of each channel of the RGB(A) color.
        old_max (float | int): Maximum value of the RGB(A) color. old_max = 123 -> e.g. white -> [123, 123, 123] / [123, 123, 123, 123]

    Returns:
        list[int]: List of each channel of the HSV(A) color.

    Exceptions:
        TypeError: If one of the arguments is of an unexpected type.
        ValueError: If the color space or new color space is not supported.
    """

    alpha: bool = False
    if len(color) == 4:
        alpha = True

    return convert_color(color, 'rgb', 'hsv', alpha, old_max)


def hsv(color: list[float | int], old_max: float = 255.0) -> list[int]:


    """
    Convert from HSV(A) (depending on the length of the list) to RGB(A) (which Brick Rigs uses for colors)

    Arguments:
        color (list[float | int]): List of each channel of the HSV(A) color.
        old_max (float | int): Maximum value of the HSV(A) color. old_max = 123 -> e.g. white -> [123, 123, 123] / [123, 123, 123, 123]

    Returns:
        list[int]: List of each channel of the RGB(A) color.

    Exceptions:
        TypeError: If one of the arguments is of an unexpected type.
        ValueError: If the color space or new color space is not supported or one of the lists are of incorrect length.
    """


    if not type(color) == list:

        raise TypeError("Color must be a list.")


    if not 3 < len(color) <= 4:

        raise ValueError("Color must be a list of 3 or 4 elements.")


    if not all(type(col) in (float, int) for col in color):

        raise ValueError("Color must be a list of 3 or 4 floats or integers.")


    return [int(col / old_max * 255) for col in color]


def hsl(color: list[float | int], old_max: float = 255.0) -> list[int]:

    """
    Convert from HSL(A) (depending on the length of the list) to HSV(A) (which Brick Rigs uses for colors)

    Arguments:
        color (list[float | int]): List of each channel of the RGB(A) color.
        old_max (float | int): Maximum value of the RGB(A) color. old_max = 123 -> e.g. white -> [123, 123, 123] / [123, 123, 123, 123]

    Returns:
        list[int]: List of each channel of the HSV(A) color.

    Exceptions:
        TypeError: If one of the arguments is of an unexpected type.
        ValueError: If the color space or new color space is not supported.
    """

    alpha: bool = False
    if len(color) == 4:
        alpha = True

    return convert_color(color, 'hsl', 'hsv', alpha, old_max)


def cmyk(color: list[float | int], old_max: float = 255.0) -> list[int]:

    """
    Convert from CMYK(A) (depending on the length of the list) to HSV(A) (which Brick Rigs uses for colors)

    Arguments:
        color (list[float | int]): List of each channel of the CMYK(A) color.
        old_max (float | int): Maximum value of the RGB(A) color. old_max = 123 -> e.g. white -> [123, 123, 123] / [123, 123, 123, 123]

    Returns:
        list[int]: List of each channel of the CMYK(A) color.

    Exceptions:
        TypeError: If one of the arguments is of an unexpected type.
        ValueError: If the color space or new color space is not supported.
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

    Arguments:
        prop_name (str): Name of the property. e.g. `'EnabledInputChannel'`
        input_type (str): Type of the input.
        value (float | int): Value of the input.
        source_bricks (list[str]): List of source bricks.

    Returns:
        dict[str, float | int | list[str]]: List of properties.
    """

    return {
        f'{prop_name}.InputAxis': input_type,
        f'{prop_name}.SourceBricks': [] if source_bricks is None else source_bricks,
        f'{prop_name}.Value': value
    }


# Since BrickInput() originates from a class:
#noinspection PyPep8Naming
def BrickInput14(prop_name: str, input_type: str, value: float | int = 1.0, source_bricks: Optional[list[str]] = None) -> dict[str, float | int | list[str]]:

    """
    Converts a list of arguments into a list of properties corresponding to brick inputs to provide similarity with BRCI-C.
    Duplicate of `brci.brick_input14()`

    Arguments:
        prop_name (str): Name of the property. e.g. `'EnabledInputChannel'`
        input_type (str): Type of the input.
        value (float | int): Value of the input.
        source_bricks (list[str]): List of source bricks.

    Returns:
        dict[str, float | int | list[str]]: List of properties.
    """

    return brick_input14(prop_name, input_type, value, source_bricks)
