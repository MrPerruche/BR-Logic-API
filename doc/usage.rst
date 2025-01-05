==============
BASICS OF BRCI
==============

This document covers essential concepts for BRCI usage, helping you get started and pick up best practices.


Setting up BRCI
---------------

BRCI supports the following versions of Brick Rigs files:

- Version ``14`` for Brick Rigs 1.7 - 1.7.4

BRCI follows the principles of Object-Oriented Programming (OOP), where each file version is represented by a specific
class. These classes are named according to the version of the Brick Rigs file they work with. For example:

- ``brci.Creation14`` for Brick Rigs version 14
- Only version 14 is supported so far.

When initializing BRCI, you need to create an instance of the appropriate class based on the version of the Brick Rigs
file you're working with. For type hinting, the generic brci.Creation class is available, but when creating the instance
you must specify the version of the Brick Rigs file (e.g., ``brci.Creation14()``).

To initialize an instance, two arguments are required: ``project_name`` and ``project_dir``.
These define the location where your Brick Rigs files are created. For example, if ``project_name`` is ``'my_vehicle'``
and ``project_dir`` is ``'C:\\my_script\\Projects'``, the files will be created in the
``C:\\my_script\\Projects\\my_vehicle`` directory. These variables can be modified at any time.

BRCI provides several predefined paths options that you can choose, that could help you especially if you are
inexperienced. Paths marked with an asterix (*) are not recommended if BRCI was installed using pip. They are:

- \* ``brci.BRCI_CWD``: Current Working Directory of BRCI.
- ``brci.BRICK_RIGS_FOLDER``: List of paths where Brick Rigs vehicle files *could* be stored.
- \* ``brci.PROJECT_FOLDER``: Folder included in BRCI for storing projects.
- \* ``brci.BACKUP_FOLDER``: Folder included in BRCI for storing backups.

**Example of initializing BRCI:**

.. code-block:: python

  import brci

  creation: brci.Creation = brci.Creation14(
      project_name='my_vehicle',
      project_dir=brci.PROJECT_FOLDER
  )

Creation classes can take a lot more arguments:

.. list-table::
  :widths: 20 80

  * - ``brci.Creation15``, ``brci.Creation14``
    - - ``project_name`` (``str``): Folder name.
      - ``project_dir`` (``str``): Directory.
      - ``name`` (``str``): Display name.
      - ``description`` (``str``): Description.
      - ``appendix`` (``bytes | bytearray``): Hidden binary data.
      - ``tags`` (``list[str] | None``): List of tags.
      - ``visibility`` (``int``): Visibility.
      - ``seat`` (``Optional[str | int]``): Name of the driver seat.
      - ``creation_time`` (``Optional[int]``): Time of creation.
      - ``update_time`` (``Optional[int]``): Time of last update.
      - ``size`` (``Optional[list[float]]``): Size of the project (meters).
      - ``weight`` (``float``): Weight of the project (kilograms).
      - ``price`` (``float``): Price of the project (dollars).

All arguments can be directly modified post-initialization.


Building with BRCI
------------------

To place bricks in our build, we have 3 functions or classes:

- ``brci.Brick<version>``: Brick class itself
- ``brci.Creation<version>.Brick``: Returns the provided brick with the same version as the creation class. Common to
  all creation classes.
- ``brci.Creation<version>.add_brick``: Directly adds a newly created brick to the creation's brick list

These 3 functions or classes all take the same arguments:

- ``brick_type`` (``str``): Type of the brick. e.g ``'ScalableCone'``.
- ``name`` (``str | int``): Name of the brick.
- ``position`` (``Optional[list[float]]``): Position of the brick.
- ``rotation`` (``Optional[list[float]]``): Rotation of the brick.
- ``properties`` (``Optional[dict[str, Any]]``): Properties of the brick.

All arguments can be directly modified post-initialization except for ``brick_type``. To modify it, use the method
``.set_type(new_type: str)`` and accessed it with ``.get_type()``.

If bricks are not directly created using the ``add_brick`` method, they can be added to the creation instance by
modifying the ``.bricks`` attribute. This is a list of ``brci.Brick<version>`` objects, and you can use methods like
``.append()`` or ``.extend()`` to add new bricks.

BRCI features many functions to help you build your creation, from

**Example of building with BRCI:**

.. code-block:: python

  import brci

  creation: brci.Creation = brci.Creation14(
      project_name='my_vehicle',
      project_dir=brci.PROJECT_FOLDER
  )

  for i in range(5):
      creation.add_brick(
          'ScalableCone',
          f'Random_scalable_{i}',
          position=brci.pos([random.uniform(0, 100) for _ in range(3)]),
          rotation=[random.uniform(-180, 180) for _ in range(3)],
          properties={
              "BrickSize": [brci.size(random.uniform(10, 20), brci.Units.CENTIMETERS) for _ in range(3)],
          }
      )

  creation.write_creation(exist_ok=True)
