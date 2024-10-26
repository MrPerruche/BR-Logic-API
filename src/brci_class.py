import os
import shutil

from .brick import *
from .utils import *
from .write_utils import *
from .write_utils import _convert_brick_names_to_id, _convert_brick_types, _get_property_data, _get_prop_bin
from datetime import datetime
# import os.path -> from .utils
# from typing import Self -> from .brick
# from typing import Final -> from .utils

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

        :param project_name: Name of the folder in which all Brick Rigs file (Vehicle.brv etc.) will be stored.
        :param project_dir: Directory where these folders will go in.
        :param name: Name of the project displayed in-game.
        :param description: Description of the project displayed in-game.
        :param appendix: Hidden binary data in files.
        :param tags: List of tags for the project.
        :param visibility: Visibility of the project, set to VISIBILITY_PUBLIC, VISIBILITY_FRIENDS, VISIBILITY_PRIVATE or VISIBILITY_HIDDEN.
        :param seat: Name of the driver seat (if there is one).
        :param creation_time: Time the project was created (in 100s of nanoseconds since 0001-01-01 00:00:00 UTC).
        :param update_time: Time the project was last updated (in 100s of nanoseconds since 0001-01-01 00:00:00 UTC).
        """

        # Path related
        self.project_name: str = project_name
        self.project_dir: str = project_dir

        # Display text
        self.name: str = name
        self.description: str = description
        self.tags: list[str] = tags
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


    def add_brick(self,
                  brick_type: str,
                  name: str | int,
                  position: Optional[list[float]] = None,
                  rotation: Optional[list[float]] = None,
                  properties: Optional[dict[str, Any]] = None) -> Self:

        # TODO
        """
        Will add a new brick to the creation.

        :param brick_type:
        :param name:
        :param position:
        :param rotation:
        :param properties:
        :return:
        """

        self.bricks.append(self.Brick(brick_type, name, position, rotation, properties))

        return self


    # TODO
    def assert_valid_parameters(self, *args: str) -> None:

        """
        Will raise errors if class parameters are invalid.

        :param args: List of class parameters name.

        Exceptions:
        OSError - Project name (project_name) is invalid
        OSError - Project dir (project_dir) is invalid

        Do not return anything.
        """

        # Project name
        if 'project_name' in args:

            # Valid folder name? cannot be mitigated.
            if not is_valid_folder_name(self.project_name, os.name == 'nt'):

                # Signal there's something wrong
                FM.error("Invalid project name.", "Your os do not support such folder names. As such, this project cannot be created.")

                raise OSError(f"Invalid project name: couldn't create a file named {self.project_name}." +
                              (" Error mitigation failed." if settings['attempt_error_mitigation'] else ""))

        # Project dir
        if 'project_dir' in args:

            # Valid project path? cannot be mitigated.
            if not os.path.exists(self.project_dir):

                # Signal there's something wrong
                FM.error("Invalid project path.", "The path you provided is not valid. As such, this project cannot be created.")

                raise OSError(f"Invalid project path: couldn't create a folder at {self.project_dir}." +
                              (" Error mitigation failed." if settings['attempt_error_mitigation'] else ""))


    def backup(self, dst: str = BACKUP_FOLDER, name: Optional[str] = None) -> Self:

        """
        Backup Brick Rigs' vehicle folder.

        :param dst: Directory where the backup will be stored.
        :param name: Name of the folder in which all Brick Rigs file (Vehicle.brv etc.) will be stored. If none, 100s of nanoseconds since 0001-01-01 00:00:00 UTC will be used.

        Exceptions:
        OSError - Project name (project_name) is invalid
        OSError - Project dir (project_dir) is invalid
        OSError - Backup folder (dst param) not found
        OSError - Backup failed
        FileNotFoundError - No Brick Rigs vehicle folder found.

        Returns the current object.
        """

        # TODO: CHECK IF THIS IS VALID FOR POSIX SYSTEMS.

        folder_name = str(get_time_100ns()) if name is None else name

        # Assert everything is valid
        self.assert_valid_parameters('project_name', 'project_dir')

        if not os.path.exists(dst):

            FM.error("Backup folder not found.",
                     "The path you provided is missing or not valid. As such, this project cannot be created.")

            # This error is cannot be mitigated.
            raise OSError(f"Backup folder not found: couldn't create a folder at {dst}." +
                          (" Error mitigation failed." if settings['attempt_error_mitigation'] else ""))

        # See if there's a path that exist among the list of possible paths, if so, copy it to the backup folder
        try:
            for potential_src in BRICK_RIGS_FOLDER:
                if os.path.exists(potential_src):
                    shutil.copytree(potential_src, os.path.join(dst, folder_name))
                    return self
        # In case something went wrong, just indicating it was an issue whilst doing the backup.
        except OSError as e:
            raise OSError(f'Backup failed! ({e})')

        # Else, then it failed, so we end with an error.
        raise FileNotFoundError("No Brick Rigs vehicle folder found." +
                                (" Error mitigation failed." if settings['attempt_error_mitigation'] else ""))


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

        :param brick_type: Type of the brick.
        :param name: Name or identifier of the brick.
        :param position: (x, y, z) coordinates of the brick's position.
        :param rotation: (pitch, yaw, roll) angles in degrees for the brick's rotation.
        :param properties: Additional properties of the brick as key-value pairs.

        Exceptions:
        <TODO>

        Returns the created brick class object.
        """

        return Brick14(brick_type, name, position, rotation, properties)


    def get_version(self) -> int:

        """
        Returns the version of the Creation object (14).
        """

        return self.__FILE_VERSION


    def write_creation(self, file_name: str = 'Vehicle.brv', exist_ok: bool = True) -> Self:

        """
        Will write the .brv (vehicle) file

        :param file_name: Name of the file (Brick Rigs will search for Vehicle.brv)
        :param exist_ok: If Vehicle.brv already exists: if set to True, replace, else raise an error.

        Exceptions:
        <TODO>

        Returns the current object.
        """

        # ################### VERIFYING PATHS ####################


        if not is_valid_folder_name(os.path.join(self.project_dir, self.project_name, file_name), os.name == 'nt'):

            # This error cannot be mitigated
            FM.error("Invalid path", f"Path {os.path.join(self.project_dir, self.project_name, file_name)} is invalid.\n"
                                     f"A such named folder cannot be created.")

            raise OSError(f"Invalid path {os.path.join(self.project_dir, self.project_name, file_name)}" +
                          (" Error mitigation failed." if settings['attempt_error_mitigation'] else ""))


        if not exist_ok and os.path.exists(os.path.join(self.project_dir, self.project_name, file_name)):

            FM.error("Invalid path", f"Path {os.path.join(self.project_dir, self.project_name, file_name)} is invalid.\n"
                                     f"A such named file cannot be created.")

            if settings['attempt_error_mitigation']:
                FM.success("Cancelling creation file creation")
            else:
                raise OSError(f"Invalid path {os.path.join(self.project_dir, self.project_name, file_name)}")

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


        # -------------------- PART 5: FOOTER AND APPENDIX --------------------

        # Footer
        if self.seat is None:
            buffer.extend(b'\x00\x00')
        else:
            buffer.extend(unsigned_int(brick_id_table[self.seat], 2))

        buffer.extend(self.appendix)



        # #################### WRITING ####################

        os.makedirs(os.path.join(self.project_dir, self.project_name), exist_ok=True)
        with open(os.path.join(self.project_dir, self.project_name, file_name), 'wb') as f:
            f.write(buffer)



        return self


    def write_metadata(self, file_name: str = 'MetaData.brm', exist_ok: bool = True) -> Self:

        """
        Will write the metadata file. TODO

        :return:
        """

        # ################### VERIFYING PATHS ####################


        if not is_valid_folder_name(os.path.join(self.project_dir, self.project_name, file_name), os.name == 'nt'):

            # This error cannot be mitigated
            FM.error("Invalid path", f"Path {os.path.join(self.project_dir, self.project_name, file_name)} is invalid.\n"
                                     f"A such named folder cannot be created.")

            raise OSError(f"Invalid path {os.path.join(self.project_dir, self.project_name, file_name)}" +
                          (" Error mitigation failed." if settings['attempt_error_mitigation'] else ""))

        if not exist_ok and os.path.exists(os.path.join(self.project_dir, self.project_name, file_name)):

            FM.error("Invalid path", f"Path {os.path.join(self.project_dir, self.project_name, file_name)} is invalid.\n"
                                     f"A such named file cannot be created.")

            if settings['attempt_error_mitigation']:
                FM.success("Cancelling metadata file creation")
            else:
                raise OSError(f"Invalid path {os.path.join(self.project_dir, self.project_name, file_name)}")

        # #################### WRITING ####################

        # Initializing stuff
        buffer: bytearray = bytearray()

        # Version number
        buffer.extend(unsigned_int(self.get_version(), 1))

        # File name
        buffer.extend(unsigned_int(-len(self.name), 2))
        buffer.extend(utf16(self.name)[2:])

        # Description:
        buffer.extend(unsigned_int(-len(self.description), 2))
        buffer.extend(utf16(self.description)[2:])

        # Brick Count
        buffer.extend(unsigned_int(len(self.bricks), 2))

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

        # Write changes
        with open(os.path.join(self.project_dir, self.project_name, file_name), 'wb') as f:
            f.write(buffer)

        return self








Creation = TypeVar('Creation', bound=Creation14)
