import os
import shutil

from .brick import *
from .utils import *
from .write_utils import *
from .write_utils import _convert_brick_names_to_id, _convert_brick_types, _get_property_data, _get_prop_bin
from datetime import datetime
from zlib import compress as zlib_compress
from typing import Callable
# import os.path -> from .utils
# from typing import Self -> from .brick
# from typing import Final -> from .utils
from time import perf_counter  # TODO TEMPORARY FOR TEST

VISIBILITY_PUBLIC: Final[int] = 0
VISIBILITY_FRIENDS: Final[int] = 1
VISIBILITY_PRIVATE: Final[int] = 2
VISIBILITY_HIDDEN: Final[int] = 3

VALID_DRIVER_SEATS: Final[set[str]] = {'Seat_2x2x7s', 'Seat_3x2x2', 'Seat_5x2x1s'}


class Creation14:

    def __init__(self, project_name: str, project_dir: str,
                 name: str = '', description: str = '', appendix: bytes | bytearray = bytearray(), tags: list[str] | None = None,
                 visibility: int = VISIBILITY_PUBLIC, seat: Optional[str | int] = None, creation_time: Optional[int] = None,
                 update_time: Optional[int] = None, size: Optional[list[float]] = None, weight: float = 0.0, price: float = 0.0) -> None:

        """
        Project creation class for version 14 (Brick Rigs 1.7.0+).

        Arguments:
            project_name (str): Name of the folder in which all Brick Rigs file (Vehicle.brv etc.) will be stored.
            project_dir (str): Directory where these folders will go in.
            name (str): Name of the project displayed in-game.
            description (str): Description of the project displayed in-game.
            appendix (bytes | bytearray): Hidden binary data in files.
            tags (list[str] | None): List of tags for the project.
            visibility (int): Visibility of the project, set to VISIBILITY_PUBLIC, VISIBILITY_FRIENDS, VISIBILITY_PRIVATE or VISIBILITY_HIDDEN.
            seat (Optional[str | int]): Name of the driver seat (if there is one).
            creation_time (Optional[int]): Time the project was created (in 100s of nanoseconds since 0001-01-01 00:00:00 UTC).
            update_time (Optional[int]): Time the project was last updated (in 100s of nanoseconds since 0001-01-01 00:00:00 UTC).
            size (Optional[list[float]]): Size of the project (in meters).
            weight (float): Weight of the project (in kilograms).
            price (float): Price of the project (in dollars).
        """

        # Path related
        self.project_name: str = project_name
        self.project_dir: str = project_dir

        # Display text
        self.name: str = name
        self.description: str = description

        self.tags: list[str] = ["Other", "Other", "Other"] if tags is None else tags

        self.creation_time: Optional[int] = creation_time
        self.update_time: Optional[int] = update_time
        self.size: list[float] = [0.0, 0.0, 0.0] if size is None else size
        self.price: float = price
        self.weight: float = weight

        # File
        self.seat: Optional[str | int] = seat
        self.appendix: bytes | bytearray = appendix

        # Other
        self.visibility: int = visibility

        self.bricks: list[Brick14] = []

        # Private
        self.__FILE_VERSION: Final[int] = 14

        # Useful debug log:
        logwrap("debug", f"Created BRCI instance with the following parameters:\n{"\n".join([f"{k}={v}" for k, v in self.__dict__.items()])}")

    def add_brick(self,
                  brick_type: str,
                  name: str | int,
                  position: Optional[list[float]] = None,
                  rotation: Optional[list[float]] = None,
                  properties: Optional[dict[str, Any]] = None) -> Self:

        # TODO
        """
        Will add a new brick to the creation.

        Arguments:
            brick_type (str): Type of the brick.
            name (str | int): Name or identifier of the brick.
            position (Optional[list[float]], optional): (x, y, z) coordinates of the brick's position. Defaults to None.
            rotation (Optional[list[float]], optional): (pitch, yaw, roll) angles in degrees for the brick's rotation. Defaults to None.
            properties (Optional[dict[str, Any]], optional): Additional properties of the brick as key-value pairs. Defaults to None.

        Exceptions:
            ValueError: If the brick type does not exist
            TypeError: One of the arguments is of invalid type
        """

        # I will put a logger call here, but it will be commented out. Only uncomment it if you REALLY need it, because it will spam like crazy.
        #logwrap("debug", f"Added new brick. Information: {brick_type=}, {name=}, {position=}, {rotation=}, {properties=}")

        self.bricks.append(self.Brick(brick_type, name, position, rotation, properties))

        return self


    # TODO
    def assert_valid_parameters(self, *args: str) -> None:

        """
        Will raise errors if class parameters are invalid.

        Arguments:
            *args (str): List of parameters to check.

        Exceptions:
            OSError: Project name (project_name) is invalid
            OSError: Project dir (project_dir) is invalid
        """

        # Project name
        if 'project_name' in args:

            # Valid folder name? cannot be mitigated.
            if not is_valid_folder_name(self.project_name, os.name == 'nt'):

                raise OSError(f"Invalid project name: couldn't create a file named {self.project_name}.")

        # Project dir
        if 'project_dir' in args:

            # Valid project path? cannot be mitigated.
            if not os.path.exists(self.project_dir):

                raise OSError(f"Invalid project path: couldn't create a folder at {self.project_dir}.")


    def backup(self, dst: str = BACKUP_FOLDER, name: Optional[str] = None) -> Self:

        """
        Backup Brick Rigs' vehicle folder.

        Arguments:
            dst (str): Directory where the backup will be stored.
            name (Optional[str]): Name of the folder in which all Brick Rigs file (Vehicle.brv etc.) will be stored. If none, 100s of nanoseconds since 0001-01-01 00:00:00 UTC will be used.

        Exceptions:
        OSError: Project name (project_name) is invalid
        OSError: Project dir (project_dir) is invalid
        OSError: Backup folder (dst param) not found
        OSError: Backup failed
        FileNotFoundError: No Brick Rigs vehicle folder found.

        Returns the current object.
        """

        # TODO: CHECK IF THIS IS VALID FOR POSIX SYSTEMS.
        
        if os.name == 'posix':
            logwrap("warning", "Creation14::backup || This function is still a work in progress and may not work on POSIX systems.")
        
        folder_name = str(get_time_100ns()) if name is None else name

        # Assert everything is valid
        self.assert_valid_parameters('project_name', 'project_dir')

        if not os.path.exists(dst):

            raise OSError(f"Backup folder not found: couldn't create a folder at {dst}.")

        # See if there's a path that exist among the list of possible paths, if so, copy it to the backup folder
        try:
            for potential_src in BRICK_RIGS_FOLDER:
                if os.path.exists(potential_src):
                    shutil.copytree(potential_src, os.path.join(dst, folder_name))
                    return self
        # In case something went wrong, just indicating it was an issue whilst doing the backup.
        except OSError as e:
            logwrap("critical", f"Creation14::backup || Backup failed! ({e})")
            raise OSError(f'Backup failed! ({e})')

        # Else, then it failed, so we end with an error.
        logwrap("critical", f"Creation14::backup || No Brick Rigs vehicle folder found!")
        raise FileNotFoundError("No Brick Rigs vehicle folder found.")


    # Following class naming conventions instead.
    # noinspection PyPep8Naming
    @staticmethod
    def Brick(brick_type: str,
              name: str | int,
              position: Optional[list[float]] = None,
              rotation: Optional[list[float]] = None,
              properties: Optional[dict[str, Any]] = None) -> Brick14:

        """
        Will return the brick class used for this creation class.

        Arguments:
            brick_type (str): Type of the brick.
            name (str | int): Name or identifier of the brick.
            position (Optional[list[float]], optional): (x, y, z) coordinates of the brick's position. Defaults to None.
            rotation (Optional[list[float]], optional): (pitch, yaw, roll) angles in degrees for the brick's rotation. Defaults to None.
            properties (Optional[dict[str, Any]], optional): Additional properties of the brick as key-value pairs. Defaults to None.

        Returns:
            Brick14: Newly created Brick14 object.

        Exceptions:
            ValueError: If the brick type does not exist
            TypeError: Name is of invalid type
        """

        return Brick14(brick_type, name, position, rotation, properties)


    def get_version(self) -> int:

        """
        Returns the version of the Creation object (14).

        Returns:
            int: Version of the Creation object
        """

        return self.__FILE_VERSION


    def write_creation(self, file_name: str = 'Vehicle.brv', exist_ok: bool = True) -> Self:

        """
        Will write the .brv (vehicle) file

        Arguments:
            file_name (str): Name of the file (Brick Rigs will search for Vehicle.brv)
            exist_ok (bool): If Vehicle.brv already exists: if set to True, replace, else raise an error.

        Returns:
            Self

        Exceptions:
            OSError: Invalid path
            ValueError: Invalid value for one of the properties
            NameError: Unknown brick name (brick with this name missing from brci.Creation().bricks) set in one of the properties
            brci.BrickError: One of the bricks are invalid, raising unexpected error.
        """

        # ################### VERIFYING PATHS ####################


        if not is_valid_folder_name(os.path.join(self.project_dir, self.project_name, file_name), os.name == 'nt'):

            raise OSError(f"Invalid path {os.path.join(self.project_dir, self.project_name, file_name)}")


        if not exist_ok and os.path.exists(os.path.join(self.project_dir, self.project_name, file_name)):

            raise OSError(f"Path exists: {os.path.join(self.project_dir, self.project_name, file_name)}")

        # #################### TREATMENT ####################

        # Bricks
        num_bricks: int = len(self.bricks)
        # Brick Types
        brick_types: set[str] = {brick.get_type() for brick in self.bricks}
        brick_types_to_index: dict[str, int] = {brick_type: i for i, brick_type in enumerate(brick_types)}
        num_brick_types: int = len(brick_types)

        # Properties
        prop_id_t_type: dict[int, str]
        prop_type_t_id: dict[str, int]
        prop_id_t__val_id_t_val: dict[int, dict[int, Any]]
        prop_id_t__val_t_val_id: dict[int, dict[int, int]]
        prop_id_t_type, prop_type_t_id, prop_id_t__val_id_t_val, prop_id_t__val_t_val_id = _get_property_data(self.bricks, bricks14)
        
        logwrap("debug", "Creation14::write_creation || Calculated header properties, instantiating buffer...")

        # #################### GENERATION ####################

        buffer: bytearray = bytearray()

        # -------------------- PART 1: HEADER --------------------

        # Version
        buffer.extend(unsigned_int(self.__FILE_VERSION, 1))

        # Bricks, unique bricks, unique properties
        buffer.extend(unsigned_int(num_bricks, 2))
        buffer.extend(unsigned_int(num_brick_types, 2))
        buffer.extend(unsigned_int(len(prop_id_t_type), 2))  # number of properties, could be another var

        # Brick types
        buffer.extend(_convert_brick_types(brick_types))

        logwrap("debug", "Creation14::write_creation || Header properties -> Buffer completed...")

        # -------------------- PART 2: BRICK TYPES --------------------

        # for brick_t in brick_types:
        #     buffer.extend(unsigned_int(len(brick_t), 1))  # Str len
        #     buffer.extend(utf8(brick_t))  # Str

        # -------------------- PART 3: PROPERTIES --------------------

        # Get all brick IDs
        brick_id_table: dict[str | int, int] = _convert_brick_names_to_id(self.bricks)

        for type_, id_ in prop_type_t_id.items():

            # Property name
            buffer.extend(unsigned_int(len(type_), 1))
            buffer.extend(utf8(type_))

            # Number of properties
            buffer.extend(unsigned_int(len(set(prop_id_t__val_id_t_val[id_])), 2))

            # Convert all properties of this type to binary
            properties_binary, properties_binary_addon = _get_prop_bin(property_types14[type_], id_, prop_id_t__val_id_t_val, brick_id_table)

            # Write all that
            buffer.extend(unsigned_int(len(properties_binary), 4))
            buffer.extend(properties_binary)
            buffer.extend(properties_binary_addon)

        logwrap("debug", "Creation14::write_creation || Brick Properties -> Buffer completed...")

        # -------------------- PART 4: BRICKS --------------------

        for brick in self.bricks:

            property_bin: bytearray = bytearray()

            # Write brick id
            buffer.extend(unsigned_int(brick_types_to_index[brick.get_type()], 2))

            # Write number of non-default properties
            brick_properties: dict[str, Any] = {prop: val for prop, val in brick.properties.items()
                                                if bricks14[brick.get_type()][prop] != val}

            # Write property ids
            property_bin.extend(unsigned_int(len(brick_properties), 1))  # Number of non-default properties
            for prop, val in brick_properties.items():
                prop_id: int = prop_type_t_id[prop]
                property_bin.extend(unsigned_int(prop_id, 2))  # id of the property type
                property_bin.extend(unsigned_int(prop_id_t__val_t_val_id[prop_id][id(val)], 2))  # id of the value

            # Position (X, Y, Z)
            property_bin.extend(sp_float(brick.position[0]))
            property_bin.extend(sp_float(brick.position[1]))
            property_bin.extend(sp_float(brick.position[2]))
            # Rotation (Y, Z, X / Pitch, Yaw, Roll)
            property_bin.extend(sp_float(brick.rotation[1]))
            property_bin.extend(sp_float(brick.rotation[2]))
            property_bin.extend(sp_float(brick.rotation[0]))

            # Write changes
            buffer.extend(unsigned_int(len(property_bin), 4))
            buffer.extend(property_bin)

        logwrap("debug", "Creation14::write_creation || Bricks -> Buffer completed...")

        # -------------------- PART 5: FOOTER AND APPENDIX --------------------

        # Footer
        if self.seat is None:
            buffer.extend(b'\x00\x00')
        else:
            buffer.extend(unsigned_int(brick_id_table[self.seat], 2))

        buffer.extend(self.appendix)

        logwrap("debug", "Creation14::write_creation || Footer/Appendix -> Buffer completed. Writing file...")

        # #################### WRITING ####################

        os.makedirs(os.path.join(self.project_dir, self.project_name), exist_ok=True)
        with open(os.path.join(self.project_dir, self.project_name, file_name), 'wb') as f:
            f.write(buffer)

        logwrap("info", "Creation writing successful.")

        return self


    def write_metadata(self, file_name: str = 'MetaData.brm', exist_ok: bool = True) -> Self:

        """
        Will write the metadata file.

        Arguments:
            file_name (str): Name of the file to write.
            exist_ok (bool): If True, will overwrite the file if it already exists.

        Returns:
            Self

        Exceptions:
            OverflowError: One of the values are invalid causing an overflow error.
            UnicodeEncodeException: One of the values are invalid causing an encoding error.
        """

        # ################### VERIFYING PATHS ####################


        if not is_valid_folder_name(os.path.join(self.project_dir, self.project_name, file_name), os.name == 'nt'):

            raise OSError(f"Invalid path {os.path.join(self.project_dir, self.project_name, file_name)}")

        if not exist_ok and os.path.exists(os.path.join(self.project_dir, self.project_name, file_name)):

            raise OSError(f"Invalid path {os.path.join(self.project_dir, self.project_name, file_name)}")

        # #################### WRITING ####################

        logwrap("info", f"Creation14::write_metadata || Instantiating buffer, writing basic details...")

        # Initializing stuff
        buffer: bytearray = bytearray()

        # Version number
        buffer.extend(unsigned_int(self.get_version(), 1))

        # File name
        buffer.extend(signed_int(-len(self.name), 2))
        buffer.extend(utf16(self.name)[2:])

        # Description:
        buffer.extend(signed_int(-len(self.description), 2))
        buffer.extend(utf16(self.description)[2:])

        # Brick Count
        buffer.extend(unsigned_int(len(self.bricks), 2))

        logwrap("info", "Creation14::write_metadata || Basic details -> Buffer completed...")

        # Vehicle Size
        for axis_size in self.size:
            buffer.extend(sp_float(axis_size))

        # Author TODO
        buffer.extend(unsigned_int(16, 1))
        buffer.extend(b'\x00' * 8)

        # Write time (100 nanosecond Gregorian bigint value)
        # Creation time
        if self.creation_time is None:
            buffer.extend(
                unsigned_int(int((datetime.now() - datetime(1, 1, 1)).total_seconds() * 1e7), 8)
            )
        else:
            buffer.extend(unsigned_int(self.creation_time, 8))

        logwrap("info", "Creation14::write_metadata || Extended details -> Buffer completed...")

        # Update time
        if self.update_time is None:
            buffer.extend(
                unsigned_int(int((datetime.now() - datetime(1, 1, 1)).total_seconds() * 1e7), 8)  # TODO PUT THAT ON time_100_ns() or idk
            )
        else:
            buffer.extend(unsigned_int(self.update_time, 8))

        # Visibility mode
        buffer.extend(unsigned_int(self.visibility, 1))

        # Tags
        buffer.extend(unsigned_int(len(self.tags), 2))
        for tag in self.tags:
            buffer.extend(unsigned_int(len(tag), 1))
            buffer.extend(utf8(tag))

        logwrap("info", "Creation14::write_metadata || All details -> Buffer completed. Writing file...")

        # Write changes
        if not os.path.exists(os.path.join(self.project_dir, self.project_name)):
            # Create the directory. open() will NOT do it for us.
            os.makedirs(os.path.join(self.project_dir, self.project_name), exist_ok=True)
        with open(os.path.join(self.project_dir, self.project_name, file_name), 'wb') as f:
            f.write(buffer)

        logwrap("info", "Creation14::write_metadata || Metadata writing successful.")

        return self


    def write_preview(self, image_path: str, file_name: str = 'Preview.png', exist_ok: bool = True) -> Self:

        """
        Will write preview for a file. A few default previews are included in brci. See brci.BRCI_THUMBNAIL, ...

        Arguments:
            image_path (str): Path to the image.
            file_name (str): Name of the file to write.
            exist_ok (bool): If True, will overwrite the file if it already exists.

        Returns:
            Self

        Exceptions:
            OSError: Image not found
            OSError: Preview already exists
        """

        # ################### VERIFYING PATHS ####################

        if not os.path.exists(image_path):

            raise OSError(f"Image missing {os.path.join(self.project_dir, self.project_name, file_name)}.")

        # TODO CHECK FOR PATH & NAME VALIDITY

        if not exist_ok and os.path.exists(os.path.join(self.project_dir, self.project_name, file_name)):

            raise OSError(f"Invalid path {os.path.join(self.project_dir, self.project_name, file_name)}")

        # ################### WRITING IMAGE ####################

        with open(image_path, 'rb') as f:
            image = f.read()

        with open(os.path.join(self.project_dir, self.project_name, file_name), 'wb') as f:
            f.write(image)

        return self


    def create_preview(self, bitmap_image: list[list[list[int]]], file_name: str = 'Preview.png', exist_ok: bool = True) -> Self:

        """
        Will create a preview for the file using a given a grid of RGBA values

        Arguments:
            bitmap_image (list[list[list[int]]]): A grid of RGBA values
            file_name (str): Name of the file to write.
            exist_ok (bool): If True, will overwrite the file if it already exists.

        Returns:
            Self

        Exceptions:
            NotImplementedError: Not working yet
            todo
        """

        raise NotImplementedError()

        if not exist_ok and os.path.exists(os.path.join(self.project_dir, self.project_name, file_name)):

            raise OSError(f"Invalid path {os.path.join(self.project_dir, self.project_name, file_name)}")


        # GENERATION

        height = len(bitmap_image)
        width = len(bitmap_image[0])

        pixels_list: list[list[int]] = [pixel for row in bitmap_image for pixel in row]

        header = b'\x89PNG\r\n\x1a\n'

        # IHDR chunk
        ihdr_data = struct_pack('>IIBBIB', width, height, 8, 6, 0, 0)
        ihdr_chunk = b'IHDR' + ihdr_data
        ihdr_crc = struct_pack('>I', crc32(b'IHDR' + ihdr_data))

        # IDAT chunk (compressed RGBA data)
        # Flatten the RGBA data into a byte string and add the filter byte for each row
        raw_data = b''.join(
            [b'\x00' + bytes([channel for pixel in pixels_list[y * width:(y + 1) * width] for channel in pixel]) for y in range(height)]
        )

        # Compress the raw image data using zlib (deflate)
        compressed_data = zlib_compress(raw_data)
        idat_chunk = b'IDAT' + compressed_data
        idat_crc = struct_pack('>I', crc32(b'IDAT' + compressed_data))

        # IEND chunk (empty chunk)
        iend_chunk = b'IEND' + b'\x00\x00\x00\x00'

        # Writing to file
        os.makedirs(os.path.join(self.project_dir, self.project_name), exist_ok=True)
        with open(os.path.join(self.project_dir, self.project_name, file_name), 'wb') as f:
            f.write(header)
            f.write(struct_pack('>I', len(ihdr_data)) + ihdr_chunk + ihdr_crc)
            f.write(struct_pack('>I', len(compressed_data)) + idat_chunk + idat_crc)
            f.write(struct_pack('>I', len(iend_chunk)) + iend_chunk)

        return self




    def read_creation(self, file_name: str = 'Vehicle.brv', brick_name: str | int = 0) -> Self:
        """
        Will read the .brv (vehicle) file, and append it to the creation's bricks.

        Arguments:
            file_name (str): Path of the .brv file
            brick_name: (str | int): If int, will set names as index + brick_name. Else, will replace {index} placeholder.

        Returns:
            Self

        Exceptions:
            FileNotFoundError: Invalid path
            NotImplementedError: Either this function isn't finished, or the file being read is from a higher version
            todo
        """

        if not settings['wip_features']: raise NotImplementedError()

        file_path = os.path.join(self.project_dir, self.project_name, file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Invalid path {file_path}")

        with open(file_path, 'rb') as f:
            file = bytearray(f.read())

        start_t = perf_counter()  # TODO TEMPORARY FOR TEST
        
        # That's all we need from the with statement.
        # Now we need to write, in reverse.

        # Find name of bricks
        if type(brick_name) == int:
            name_func = lambda index: index + brick_name
        else:
            name_func = lambda index: brick_name.replace("{index}", str(index))

        # -------------------- PART 1: HEADER INFO -------------------- #

        file_version: int = get_unsigned_int(extract_bytes(file, 1))

        # Version check:
        if file_version != self.get_version():
            raise NotImplementedError(f"Version {file_version} mismatch, {self.get_version()})")

        # The next two bytes are the number of bricks in the creation. (uint16)
        num_bricks: int = get_unsigned_int(extract_bytes(file, 2))

        # The next two bytes are the number of unique brick types.
        num_brick_types: int = get_unsigned_int(extract_bytes(file, 2))
        # And the next two, the number of unique properties:
        num_properties: int = get_unsigned_int(extract_bytes(file, 2))

        logwrap("debug", "Creation14::read_creation || Buffer -> Header info completed...")


        # -------------------- PART 2: BRICK TYPES  -------------------- #

        brick_types: set = set()
        for _ in range(num_brick_types):
            brick_types.add(extract_str8(file))
        brick_types_tuple = tuple(brick_types)

        logwrap("debug", "Creation14::read_creation || Buffer -> Brick types completed...")



        # -------------------- PART 3: PROPERTIES -------------------- #

        properties: dict[str, list[Any]] = {}

        for _ in range(num_properties):

            prop_name: str = extract_str8(file)
            num_values: int = get_unsigned_int(extract_bytes(file, 2))
            bin_len: int = get_unsigned_int(extract_bytes(file, 4))
            bin_properties: bytearray = extract_bytes(file, bin_len)

            bin_values: list[bytearray] = []
            values: list[any] = []

            if num_values > 1:
                first_len: int = get_unsigned_int(extract_bytes(file, 2))

                if first_len == 0:
                    for _ in range(num_values):
                        bin_values.append(extract_bytes(bin_properties, get_unsigned_int(extract_bytes(file, 2))))

                else: # if num_values > 1:
                    bin_values = [extract_bytes(bin_properties, first_len) for _ in range(num_values-1)]

            else:
                bin_values = [bin_properties]

            for bin_value in bin_values:

                print(prop_name, bin_value)
                print(first_len)

                match property_types14[prop_name]:

                    case 'bin':
                        values.append(bin_value)

                    case 'bool':
                        values.append(bin_value == b'\x01')

                    case 'brick_id':
                        values.append(name_func(get_unsigned_int(bin_value[-2:])-1))

                    case 'float':
                        values.append(get_sp_float(bin_value))

                    case 'list[3*float]':
                        values.append([get_sp_float(bin_value[i:i+4]) for i in range(0, 12, 4)])

                    case 'list[3*uint8]':
                        values.append([get_unsigned_int(bin_value[i:i+1]) for i in range(0, 3, 1)])

                    case 'list[4*uint8]':
                        values.append([get_unsigned_int(bin_value[i:i+1]) for i in range(0, 4, 1)])

                    case 'list[6*uint2]':
                        values.append([(get_unsigned_int(bin_value) >> i) & 0x3 for i in range(12, -1, -2)])

                    case 'list[brick_id]':
                        values.append([name_func(get_unsigned_int(extract_bytes(bin_value, 2))-1) for _ in range(get_unsigned_int(extract_bytes(bin_value, 2)))])

                    case 'str8':
                        values.append(extract_str8(bin_value))

                    case 'strany':
                        values.append(extract_str16(bin_value))

                    case 'uint8':
                        values.append(get_unsigned_int(bin_value))

            properties.update({prop_name: values})

        logwrap("debug", "Creation14::read_creation || Buffer -> Properties completed...")

        # -------------------- PART 4: BRICKS -------------------- #


        # Setting up stuff
        property_type_names: tuple[str, ...] = tuple(properties.keys())

        for brick in range(num_bricks):

            # Get type of the brick
            brick_type: str = brick_types_tuple[get_unsigned_int(extract_bytes(file, 2))]

            # PROPERTIES
            # Get number of properties
            num_brick_properties: int = get_unsigned_int(extract_bytes(file, 1))

            # Get properties
            brick_properties: dict = {}
            for _ in range(num_brick_properties):
                # Retrieve IDs
                prop_id: int = get_unsigned_int(extract_bytes(file, 2))
                val_id: int = get_unsigned_int(extract_bytes(file, 2))

                # Obtain value from IDs and append them to already collected properties
                brick_properties.update({
                    property_type_names[prop_id]: property_type_names[prop_id][val_id]
                })

            # Get position and rotation
            position: list[float] = [get_sp_float(extract_bytes(file, 4)) for _ in range(3)]
            rotation: list[float] = [get_sp_float(extract_bytes(file, 4)) for _ in range(3)]
            rotation = [rotation[2], rotation[0], rotation[1]]  # (Y Z X) -> (X Y Z)

            # Done. Add the brick to the list
            self.add_brick(brick_type=brick_type,
                           name=name_func(brick),
                           position=position,
                           rotation=rotation,
                           properties=brick_properties
            )

        # -------------------- PART 5: FOOTER --------------------

        seat_id: int = get_unsigned_int(extract_bytes(file, 2))

        if seat_id != 0:
            self.seat = name_func(seat_id-1)

        end_t = perf_counter()    # TODO TEMPORARY FOR TEST
        print(f"time (reading excluded): {end_t - start_t:,.6f}")  # TODO TEMPORARY FOR TEST



        return self




Creation = TypeVar('Creation', bound=Creation14)
