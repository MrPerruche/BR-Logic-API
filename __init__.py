###############################################################################################################
##                                                                                                           ##
##                                                                                                           ##
##                                    Brick Rigs Creation Interface (BRCI)                                   ##
##           Take advantage of Python's dynamic nature to create and edit creations in Brick Rigs.           ##
##                                                                                                           ##
##                                          Originally authored by:                                          ##
##                                        MrPerruche (@perru_, Perru)                                        ##
##                                       Copper (@kitethelunatic, Kite)                                      ##
##                                       ANC (@absolutely_no_context)                                        ##
##                                     Infernia829 (@spectre829, Spectre)                                    ##
##                                   Erzbengel Raziel (@erzbengel_raziel)                                    ##
##                                        TLM (@tlm_gujarati) (M.I.A)                                        ##
##                                                                                                           ##
##                                                                                                           ##
##                         Rewrite authored primarily by MrPerruche (@perru_, Perru)                         ##
##                             With some help from Copper (@kitethelunatic, Kite)                            ##
##                                                                                                           ##
##                      Find BRCI's repository here: https://github.com/MrPerruche/BRCI                      ##
##                                                                                                           ##
###############################################################################################################

"""
Brick Rigs Creation Interface (BRCI)
====================================

### Take advantage of Python's dynamic nature to create and edit creations in Brick Rigs.
BRCI is a package written in python that allows you to create and edit your creations though code.<br>
This gives you quite a lot of freedom as, for example:
- Values can be determined at runtime.
- You can edit an existing vehicle or brick and it's properties.
- You can convert objects in code to bricks in-game.

Usage
-----
Most functions will have docstrings, as well as BRCI having markdown files and a GitHub wiki.

An example of using BRCI::


  >>> import BRCI as brci
  ... 
  >>> vehicle = brci.Creation14()
  ...
  >>> # Some configuration options for the creation...
  >>> vehicle.name = "My Creation"
  >>> vehicle.folder_name = "my_creation" # The name of the folder the creation's vehicle file and metadata are saved in.
  >>>                                     # Please do not use spaces, caps, etc. However, it's sanity checked and they are removed.
  >>> vehicle.project_folder = brci.PROJECT_FOLDER # The path the vehicle folder (vehicle.folder_name) is saved in. Defaults to brci.PROJECT_FOLDER
  >>> vehicle.description = "My brand new creation!"
  ...
  >>> # Some BRCI configuration...
  >>> TODO ADD VEHICLE CONFIG IN DOCSTRING
  ...
  >>> # Adding some bricks...
  >>> # Note for BRCI version C users, BRCI now natively includes a whole ton of utilties, such as RGBA brick colors!
  >>> vehicle.new_brick(brick_type="ScalableBrick", brci_name="My New Brick!", properties={"BrickColor": brci.rgba([255, 0, 255, 255])}, position=[0, 0, 0], rotation=[0, 0, 0])
  ...
  >>> # You can also add it like this:
  >>> brick = brci.Brick14(brick_type="ScalableBrick", brci_name="My Second Brick!", properties={"BrickColor": brci.rgba([255, 0, 255, 255])}, position=[0, 0, 0], rotation=[0, 0, 0])
  ...
  >>> # But we don't want the red to be 255! We want the green to be 255!
  >>> vehicle.edit_brick(brci_name="My new Brick!", properties_to_update={"BrickColor": brci.rgba([0, 255, 0, 255])})
  ...
  >>> # Finally, we can save it and put it in our game.
  >>> vehicle.write_creation_image() # Note: you can specify a custom preview! Please, please look at the docstring for all the functions!
  >>> vehicle.write_metadata() # Name can be specified for metadata and vehicle file!
  >>> vehicle.write_vehicle_file()
  >>> vehicle.copy_to_br_vehicles() # You can specify the path of the Vehicles folder as well if your setup is weird. PLEASE look at the docstring.
  >>> vehicle.clear_all_bricks() # Clear all the bricks from the creation, but keep the vehicle file and metadata. Good for reusing the same Creation14 object.
"""

from .src.brci_class import *
from .src.property_utils import *
# from brci.src.brick import *  # import from .brci_class
# from brci..utils import *  # import from .brci_class