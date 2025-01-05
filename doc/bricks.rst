===================================
BRCI Supported Bricks Documentation
===================================

Here you will find all brick types and properties in the base, un-modded game.
-----------------------------------------------------------------------------

DATA TYPES
==========

BRCI supports the following types by default:

.. list-table::
    :header-rows: 1
    :widths: 10 10 10 30 30

    * - Type name
      - Expected type(s)
      - Example value
      - Restrictions
      - Description
    * - ``bin``
      - ``bytes | bytearray``
      - ``b'\x00Hello World'``
      - \-
      - Binary data (as bytes or bytearray object).
    * - ``bool``
      - ``bool`` or has ``__bool__`` attr.
      - ``True``
      - \-
      - Boolean represented with ``0x00`` or ``0x01`` for False or True.
    * - ``brick_id``
      - ``str | int``
      - ``'my_new_brick'``
      - \-
      - ``1`` as an ``uint16`` followed by the name "translated" to an ID as ``uint16``.
    * - ``float``
      - ``float``
      - ``12.0``
      - \-
      - Represented as a single-precision floating point number (``float32``).
    * - ``list[3*float]``
      - ``list[float]``
      - ``[1.0, 2.0, 3.0]``
      - ``len(value) == 3``
      - A list of 3 single precision float numbers (``float32``).
    * - ``list[3*uint8]``
      - ``list[int]``
      - ``[1, 2, 3]``
      - ``brci.Limits.U8_MIN <= value[i] <= brci.Limits.U8_MAX and len(value) == 3``
      - A list of 3 ``uint8`` s.
    * - ``list[4*uint8]``
      - ``list[int]``
      - ``[1, 2, 3, 4]``
      - ``brci.Limits.U8_MIN <= value[i] <= brci.Limits.U8_MAX and len(value) == 4``
      - A list of 4 ``uint8`` s.
    * - ``list[6*uint2]``
      - ``list[int]``
      - ``[1, 2, 3, 0, 1, 2]``
      - ``brci.Limits.U2_MIN <= value[i] <= brci.Limits.U2_MAX and len(value) == 6``
      - A list of 6 ``uint2`` s.
    * - ``list[brick_id]``
      - ``list[str | int]``
      - ``['brick1', 2, 'brick3']``
      - ``len(value) <= brci.Limits.U16_MAX``
      - A list of brick ids (``uint16`` s being "translations" of names to an ID). ``len(value)`` as ``uint16`` then all
        brick IDs as ``uint16`` s.
    * - ``str8``
      - ``str``
      - ``'Hello\r\nWorld'``
      - ``len(value) <= brci.Limits.U8_MAX``
      - ``len(value)`` as ``uint8`` then the string encoded in ascii.
    * - ``strany``
      - ``str``
      - ``'\u2728 Hello World \u2728'``
      - ``len(value) <= brci.Limits.I16_MAX + (0 if ascii else 1)``
      - ``len(value) * (1 if ascii else -1)`` as ``uint16`` then the string encoded in either ascii or UTF-16.
    * - ``uint8``
      - ``int``
      - ``146``
      - ``brci.Limits.U8_MIN <= value <= brci.Limits.U8_MAX``
      - \-

If a callable (such as a lambda function) is provided instead of the expected type, BRCI will call it and retrieve it's
returned value as the property's value.

.. TODO

PROPERTIES
==========

.. _prop-name:

(property name)
----
(Property details in a beginner-friendly human-readable format)

BRICKS FORMAT
=============

Bricks go in this format:

``Brick: Letter``

The 'letter' portion is the 'property group', where all bricks with this letter share the same properties.

BRICKS
======

Category: Bricks
----

This category has basic building blocks, the classic LEGO.

.. code:: none

  Example Brick 1: A
  Example Brick 2: B

----

.. list-table::
    :header-rows: 1

    * - Group Letter
      - Properties
    * - A
      - :ref:`prop-name`
    * - B
      - :ref:`prop-name`