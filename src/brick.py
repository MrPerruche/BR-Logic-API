from typing import Self, Optional, TypeVar, Final, Iterable, Literal
# from collections.abc import MutableMapping, MutableSequence
# from copy import deepcopy
from .bricks import *
from .utils import Limits, FM, settings
from .write_utils import can_be_encoded_in_utf

# from typing import Any -> from .bricks.bricks_utils


SUPPORTED_VERSIONS: Final[frozenset[int]] = frozenset({14})
SUPPORTED_PROPERTY_TYPES: Final[set[str]] = {"bin", "bool", "brick_id", "float", "list[3*float]", "list[6*uint2]",
    "list[3*uint8]", "list[4*uint8]", "list[brick_id]"}


def _has_valid_properties(default_settings: dict[str, Any], property_map: dict[str, str], properties: dict[str, Any], call_callables: bool = False) -> tuple[bool, str]:

    """
    Internal function to check if properties are valid.

    Arguments:
        default_settings (dict[str, Any]): Default settings for a brick
        property_map (dict[str, str]): List of known properties.
        properties (dict[str, Any]): List of properties of the brick
        call_callables (bool): If yes or no we call callable inputs such as lambda functions.

    Returns:
         bool: indicating if it's valid or not and a string with an error message if not.
         str: error message (or empty string if valid)
    """


    if properties.keys() != default_settings.keys():

        for key in properties.keys():
            if key not in default_settings:

                # Key shouldn't be there. Is it not supposed to be here or not supposed to be a thing?
                if key in property_map.keys():
                    return False, f'Property {key} is not a property of this brick.'
                else:
                    return False, f'Unknown property: {key}.'

        for key in default_settings.keys():
            if key not in properties:
                return False, f'Missing property: {key}.'

    for property_, value in properties.items():

        # Set value to analyzed value (to make sure no editions happens)
        analyzed_value = value

        # If it's a callable -> e.g. lambda functions
        if callable(value):

            # If we want to call it, call it
            if call_callables:
                analyzed_value = value()
            # Else don't (maybe because previous executions affect later executions?)
            else:
                continue

        # Get what type the property is (we already checked if it was of a valid type)
        prop_type = property_map[property_]

        match prop_type:

            # Binary: must be bytes or bytearray
            case 'bin':
                if not isinstance(analyzed_value, (bytes, bytearray)):
                    return False, f'Property {property_} must be bytes or bytearray.'

            # Boolean: must be a boolean
            case 'bool':
                if not hasattr(analyzed_value, "__bool__"):
                    return False, f'Property {property_} must be a boolean.'

            # Brick id: must be a string or integers (bricks are represented with strings and integers)
            case 'brick_id':
                if not isinstance(analyzed_value, (str, int)):
                    return False, f'Property {property_} must be a string or an integer.'

            # Float: must be a float
            case 'float':
                if not isinstance(analyzed_value, float):
                    return False, f'Property {property_} must be a float.'

            # List[3*float]: must be a list of 3 floats
            case 'list[3*float]':
                if not isinstance(analyzed_value, list):
                    return False, f'Property {property_} must be a list of 3 floats.'
                if len(analyzed_value) != 3:
                    return False, f'Property {property_} must be a list of 3 floats.'
                if not all(isinstance(item, float) for item in analyzed_value):
                    return False, f'Property {property_} must be a list of 3 floats.'

            # List[3*uint8]: must be a list of 3 integers between 0 and 255
            case 'list[3*uint8]':
                if not isinstance(analyzed_value, list):
                    return False, f'Property {property_} must be a list of 3 integers between {Limits.U8_MIN} and {Limits.U8_MAX}.'
                if len(analyzed_value) != 3:
                    return False, f'Property {property_} must be a list of 3 integers between {Limits.U8_MIN} and {Limits.U8_MAX}.'
                if not all(isinstance(item, int) for item in analyzed_value):
                    return False, f'Property {property_} must be a list of 3 integers between {Limits.U8_MIN} and {Limits.U8_MAX}.'
                if not all(Limits.U8_MIN <= item <= Limits.U8_MAX for item in analyzed_value):
                    return False, f'Property {property_} must be a list of 3 integers between {Limits.U8_MIN} and {Limits.U8_MAX}.'

            # List[4*uint8]: must be a list of 4 integers between 0 and 255
            case 'list[4*uint8]':
                if not isinstance(analyzed_value, list):
                    return False, f'Property {property_} must be a list of 4 integers between {Limits.U8_MIN} and {Limits.U8_MAX}.'
                if len(analyzed_value) != 4:
                    return False, f'Property {property_} must be a list of 4 integers between {Limits.U8_MIN} and {Limits.U8_MAX}.'
                if not all(isinstance(item, int) for item in analyzed_value):
                    return False, f'Property {property_} must be a list of 4 integers between {Limits.U8_MIN} and {Limits.U8_MAX}.'
                if not all(Limits.U8_MIN <= item <= Limits.U8_MAX for item in analyzed_value):
                    return False, f'Property {property_} must be a list of 4 integers between {Limits.U8_MIN} and {Limits.U8_MAX}.'

            # List[6*uint2]: must be a list of 6 integers between 0 and 3
            case 'list[6*uint2]':
                if not isinstance(analyzed_value, list):
                    return False, f'Property {property_} must be a list of 6 integers between {Limits.U2_MIN} and {Limits.U2_MAX}.'
                if len(analyzed_value) != 6:
                    return False, f'Property {property_} must be a list of 6 integers between {Limits.U2_MIN} and {Limits.U2_MAX}.'
                if not all(isinstance(item, int) for item in analyzed_value):
                    return False, f'Property {property_} must be a list of 6 integers between {Limits.U2_MIN} and {Limits.U2_MAX}.'
                if not all(Limits.U2_MIN <= item <= Limits.U2_MAX for item in analyzed_value):
                    return False, f'Property {property_} must be a list of 6 integers between {Limits.U2_MIN} and {Limits.U2_MAX}.'

            # List[brick_id]: must be a list of brick ids (either strings or integers)
            case 'list[brick_id]':
                if not isinstance(analyzed_value, list):
                    return False, f'Property {property_} must be a list of brick ids (either strings or integers).'
                if not isinstance(analyzed_value, (str, int)):
                    return False, f'Property {property_} must be a list of brick ids (either strings or integers).'

            # String (utf-8): must be a string encodable in utf-8
            case 'str8':
                if not isinstance(analyzed_value, str):
                    return False, f'Property {property_} must be a string encodable in utf-8.'
                # Check if it is encodable in utf-8
                if not can_be_encoded_in_utf(analyzed_value):
                    return False, f'Property {property_} must be a string encodable in utf-8.'

            # String (utf-16): must be a string encodable in utf-16.
            case 'strany':
                if not isinstance(analyzed_value, str):
                    return False, f'Property {property_} must be a string encodable in utf-8 or utf-16.'
                # Check if it is encodable in utf-8 and utf-16
                if not can_be_encoded_in_utf(analyzed_value):
                    return False, f'Property {property_} must be a string encodable in utf-8 or utf-16.'

            # Integer: must be an integer between 0 and 255
            case 'uint8':
                if not isinstance(analyzed_value, int):
                    return False, f'Property {property_} must be an integer between {Limits.U8_MIN} and {Limits.U8_MAX}.'
                if not (Limits.U8_MIN <= analyzed_value <= Limits.U8_MAX):
                    return False, f'Property {property_} must be an integer between {Limits.U8_MIN} and {Limits.U8_MAX}.'


# TODO
def new_properties(properties: dict[str, Literal["bin", "bool", "brick_id", "float", "list[3*float]", "list[6*uint2]",
                       "list[3*uint8]", "list[4*uint8]", "list[brick_id]", "str8", "strany", "uint8"]],
                   affected_versions: Iterable[int] = SUPPORTED_VERSIONS) -> None:

    """
    Add or edit a property in the list of known properties and their type.

    Arguments:
        properties (dict[str, str]): Dictionary with property names (str) as keys and their corresponding property type (str) as values.
        affected_versions (Iterable[int], optional): List of all versions that will see these changes applied. Defaults to all known versions.
    """

    # Making sure everything is supported
    sanitized_versions: set[int] = set()
    sanitized_properties: dict[str, str] = {}

    # Make sure affected versions are right:
    for ver in affected_versions:
        if ver not in SUPPORTED_VERSIONS:

            raise ValueError(f"Unknown or non-supported file version {ver!r}")

    # Making sure types are right:
    for p, t in properties.items():
        if t not in SUPPORTED_PROPERTY_TYPES:

            raise ValueError(f"Unknown property type {t!r} (for {p!r})")

        # else:
        sanitized_properties.update({p: t})

    for ver in sanitized_versions:
        if ver == 14:
            bricks14.update(sanitized_properties)


def new_types(types: Iterable[str], properties: dict[str, Any], common_properties: bool = True,
              affected_versions: Iterable[int] = SUPPORTED_VERSIONS) -> None:


    """
    Function to modify or implement custom (modded) bricks.

    Arguments:
        types (Iterable[str]): List of custom brick types.
        properties (dict[str, Any]): Dictionary with property names (str) as keys and their corresponding property type (str) as values.
        common_properties (bool, optional): Whether to add common properties. Defaults to True.
        affected_versions (Iterable[int], optional): List of all versions that will see these changes applied. Defaults to all known versions.
    """

    # I know repetition should be avoided, but speed is more important.

    # Making sure everything is supported
    sanitized_affected_versions: set[int] = {ver for ver in affected_versions if ver in SUPPORTED_VERSIONS}

    for ver in sanitized_affected_versions:

        if ver == 14:
            for brick_type in types:
                bricks14.update({brick_type: properties})  # Puts properties
                if common_properties: bricks14[brick_type].update(default_properties14())  # Puts common properties


class Brick14:

    def __init__(self,
                 brick_type: str,
                 name: str | int,
                 position: Optional[list[float]] = None,
                 rotation: Optional[list[float]] = None,
                 properties: Optional[dict[str, Any]] = None) -> None:

        """
        Will store all data for a single brick.

        Arguments:
            brick_type (str): Type of the brick.
            name (str | int): Name or identifier of the brick.
            position (Optional[list[float]], optional): (x, y, z) coordinates of the brick's position. Defaults to None.
            rotation (Optional[list[float]], optional): (pitch, yaw, roll) angles in degrees for the brick's rotation. Defaults to None.
            properties (Optional[dict[str, Any]], optional): Additional properties of the brick as key-value pairs. Defaults to None.

        Exceptions:
            ValueError: If the brick type does not exist
            TypeError: Name is of invalid type
        """

        if type(name) not in (str, int):
            raise TypeError(f"Name must be a string or integer, not {type(name).__name__}.")

        # Set all variables
        self._brick_type = brick_type
        self.name: str | int = name
        self.position: list[float] = [0.0, 0.0, 0.0] if position is None else position
        self.rotation: list[float] = [0.0, 0.0, 0.0] if rotation is None else rotation
        self.properties: dict[str, Any] = {} if properties is None else properties

        # Set properties to something meaningful (will keep already set properties if they've valid!)
        self.set_type(brick_type)


    def get_type(self) -> str:

        """
        Will return the brick type of the Brick14 object.

        Returns:
            str: Type of the Brick14 object
        """
        return self._brick_type


    def is_invalid_brick(self, call_callables: bool = False) -> list[str]:

        """
        Will return all invalid values for this brick.

        Arguments:
            call_callables (bool): Whether to call the callables or not. Defaults to False.

        Returns:
            list[str]: List of invalid values
        """

        # Doc inherited from _Brick.is_valid_brick()
        invalid_values: list[str] = []

        # Check for name: is a string or integer
        if not isinstance(self.name, (str, int)):
            invalid_values.append('name')

        # Check for position: is a list of 3 floats or integers
        if not (isinstance(self.position, list) or len(self.position) == 3 or
                all(isinstance(x, (float, int)) for x in self.position)):

            invalid_values.append('position')

        # Check for rotation: is a list of 3 floats or integers
        if not (isinstance(self.rotation, list) or len(self.rotation) == 3 or
                all(isinstance(x, (float, int)) for x in self.rotation)):

            invalid_values.append('rotation')

        # Check properties
        valid_properties, _ = _has_valid_properties(bricks14[self._brick_type], property_types14, self.properties, call_callables)
        if not valid_properties:

            invalid_values.append('properties')

        return invalid_values


    def set_type(self, new_type: str) -> Self:

        """
        Sets the brick to a new type. Attempts to preserve any property in common with the new brick.

        Arguments:
            new_type (str): New type of the brick.

        Returns:
            Self

        Exceptions:
            ValueError: if the new type does not exist
        """

        # Make sure this brick exists
        if new_type in bricks14.keys():

            # Get new set of properties
            new_prop: dict[str, Any] = deepcopy(bricks14[new_type])

            for property_ in self.properties.keys():
                if property_ in new_prop:
                    new_prop[property_] = self.properties[property_]

            # Edit self for the new brick type
            self.properties = new_prop
            self._brick_type = new_type

        else:
            raise ValueError(f"Brick type {new_type!r} does not exist")

        return Self




Brick = TypeVar('Brick', bound=Brick14)


