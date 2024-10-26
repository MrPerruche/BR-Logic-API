from .bricks_utils import _add_mk
from copy import deepcopy
from typing import Any

"""
    '.InputAxis': 'str8',
    '.SourceBricks': 'list[brick_id]',
    '.Value': 'float',
"""


# All different properties and their type
property_types14: dict[str, str] = {
    'ActuatorMode': 'str8',
    'AmmoType': 'str8',
    'AutoHoverInputChannel.InputAxis': 'str8',
    'AutoHoverInputChannel.SourceBricks': 'list[brick_id]',
    'AutoHoverInputChannel.Value': 'float',
    'bAccumulated': 'bool',
    'bAccumulateInput': 'bool',
    'bCanDisableSteering': 'bool',
    'bCanInvertSteering': 'bool',
    'bDriven': 'bool',
    'bGenerateLift': 'bool',
    'bHasBrake': 'bool',
    'bHasHandBrake': 'bool',
    'bInvertDrive': 'bool',
    'bInvertTankSteering': 'bool',
    'BrakeStrength': 'float',
    'bReturnToZero': 'bool',
    'BrickColor': 'list[4*uint8]',
    'BrickMaterial': 'str8',
    'BrickPattern': 'str8',
    'BrickSize': 'list[3*float]',
    'Brightness': 'float',
    'bTankDrive': 'bool',
    'ConnectorSpacing': 'list[6*uint2]',
    'CouplingMode': 'str8',
    'DisplayColor': 'list[3*uint8]',
    'ExitLocation': 'list[3*float]',
    'FlashSequence': 'str8',
    'Font': 'str8',
    'FontSize': 'float',
    'FuelType': 'str8',
    'GearRatioScale': 'float',
    'HornPitch': 'float',
    'IdlerWheels': 'list[brick_id]',
    'Image': 'str8',
    'ImageColor': 'list[3*uint8]',
    'InputChannel.InputAxis': 'str8',
    'InputChannel.SourceBricks': 'list[brick_id]',
    'InputChannel.Value': 'float',
    'InputScale': 'float',
    'LightConeAngle': 'float',
    'LightDirection': 'str8',
    'MaxAngle': 'float',
    'MaxLimit': 'float',
    'MinAngle': 'float',
    'MinLimit': 'float',
    'NumFractionalDigits': 'uint8',
    'Operation': 'str8',
    'OutlineThickness': 'float',
    'OutputChannel.MinIn': 'float',
    'OutputChannel.MinOut': 'float',
    'OutputChannel.MaxIn': 'float',
    'OutputChannel.MaxOut': 'float',
    'OwningSeat': 'brick_id',
    'PitchInputChannel.InputAxis': 'str8',
    'PitchInputChannel.SourceBricks': 'list[brick_id]',
    'PitchInputChannel.Value': 'float',
    'PowerInputChannel.InputAxis': 'str8',
    'PowerInputChannel.SourceBricks': 'list[brick_id]',
    'PowerInputChannel.Value': 'float',
    'RollInputChannel.InputAxis': 'str8',
    'RollInputChannel.SourceBricks': 'list[brick_id]',
    'RollInputChannel.Value': 'float',
    'SensorType': 'str8',
    'SirenType': 'str8',
    'SmokeColor': 'list[3*uint8]',
    'SpawnScale': 'float',
    'SpeedFactor': 'float',
    'SteeringAngle': 'float',
    'SteeringSpeed': 'float',
    'SuspensionDamping': 'float',
    'SuspensionLength': 'float',
    'SuspensionStiffness': 'float',
    'SwitchName': 'strany',
    'Text': 'strany',
    'TextColor': 'list[3*uint8]',
    'ThrottleInputChannel.InputAxis': 'str8',
    'ThrottleInputChannel.SourceBricks': 'list[brick_id]',
    'ThrottleInputChannel.Value': 'float',
    'TirePressureRatio': 'float',
    'TireThickness': 'float',
    'TraceMask': 'str8',
    'TrackColor': 'list[4*uint8]',
    'WheelDiameter': 'float',
    'WheelWidth': 'float',
    'WinchSpeed': 'float',
    'YawInputChannel.InputAxis': 'str8',
    'YawInputChannel.SourceBricks': 'list[brick_id]',
    'YawInputChannel.Value': 'float'
} # {'brick_id', 'list[4*uint8]', 'uint8', 'strany', 'list[brick_id]', 'str8', 'float', 'list[3*float]', 'list[6*uint2]', 'list[3*uint8]', 'bool'}


# Assign all properties
def default_properties14() -> dict[str, Any]:
    return deepcopy({'BrickColor': [0, 0, 127, 255], 'BrickPattern': 'Default', 'BrickMaterial': 'Plastic'})


# Initialize bricks for later
bricks14: dict[str, Any] = {}


# ACTUATORS. Last update: 1.7.4

_add_mk(bricks14, ('Actuator_1sx1sx1s_02_Top', 'Actuator_1sx1sx1s_Male', 'Actuator_1sx1sx1s_Top',
        'Actuator_1sx1sx2s_Top', 'Actuator_1x1x1s_Top', 'Actuator_1x1x1_Top', 'Actuator_1x1x3_Top', 'Actuator_1x1x6_Top',
        'Actuator_2x1x1s_02_Top', 'Actuator_2x1x1s_Male', 'Actuator_2x1x1s_Top', 'Actuator_2x2x1s_Angular_Top',
        'Actuator_2x2x1s_Top', 'Actuator_2x2x2_Top', 'Actuator_2x2x15_Top', 'Actuator_4x1x1s_Top', 'Actuator_4x4x1s_Top',
        'Actuator_6x2x1s_Top', 'Actuator_8x8x1_Top', 'Actuator_20x2x1s_Top'),
    default_properties14())

_add_mk(bricks14, ('Actuator_1sx1sx1s_Bottom', 'Actuator_1sx1sx1s_Female', 'Actuator_1sx1sx2s_Bottom',
        'Actuator_1x1sx1s_Bottom', 'Actuator_1x1x1s_Bottom', 'Actuator_1x1x1_Bottom', 'Actuator_1x1x3_Bottom',
        'Actuator_1x1x6_Bottom', 'Actuator_2x1sx1s_Bottom', 'Actuator_2x1x1s_02_Bottom',
        'Actuator_2x1x1s_Bottom', 'Actuator_2x1x1s_Female', 'Actuator_2x2x1s_Angular_Bottom',
        'Actuator_2x2x1s_Bottom', 'Actuator_2x2x2_Bottom', 'Actuator_2x2x15_Bottom', 'Actuator_4x1x1s_Bottom',
        'Actuator_4x4x1s_Bottom', 'Actuator_6x2x1s_Bottom', 'Actuator_8x8x1_Bottom',
        'Actuator_20x2x1s_Bottom'),
    default_properties14() | {
        'ActuatorMode': 'Accumulated',
        'InputChannel.InputAxis': 'Auxiliary',
        'InputChannel.SourceBricks': [],
        'InputChannel.Value': 1.0,
        'SpeedFactor': 1.0,
        'MinLimit': 0.0,
        'MaxLimit': 0.0
    }
)


# AVIATION. Last update: 1.7.4

_add_mk(bricks14, ('BladeHolder_2x1', 'Prop_5x1', 'Prop_10x1', 'Rotor_3x4', 'Rotor_4x8', 'Blade_20x2', 'Blade_26x2'),
    default_properties14()
)

_add_mk(bricks14, ('Wing_2x2x1s', 'Wing_2x2x1s_L', 'Wing_2x2x1s_R', 'WingRounded_2x2x1s', 'Wing_2x3x1s',
        'Wing_2x3x1s_L', 'Wing_2x3x1s_R', 'Wing_2x4x1s_L', 'Wing_2x4x1s_R', 'Wing_3x3x1s', 'Wing_4x8x1s_L',
        'Wing_4x8x1s_R'),
    default_properties14() | {
        'bGenerateLift': True
    }
)

_add_mk(bricks14, ('Flap_1x4x1s', 'Flap_2x8x1s'),
    default_properties14() | {
        'bGenerateLift': True,
        'InputChannel.InputAxis': 'None',
        'InputChannel.SourceBricks': [],
        'InputChannel.Value': 1.0,
        'MinAngle': -22.5,
        'MaxAngle': 22.5,
        'bAccumulateInput': True
    }
)

_add_mk(bricks14, ('Turbine_6x2x2', 'Turbine_8x4x2', 'Turbine_12x8x5'),
    default_properties14() | {
        'PowerInputChannel.InputAxis': 'None',
        'PowerInputChannel.SourceBricks': [],
        'PowerInputChannel.Value': 1.0,
        'AutoHoverInputChannel.InputAxis': 'None',
        'AutoHoverInputChannel.SourceBricks': [],
        'AutoHoverInputChannel.Value': 1.0,
        'ThrottleInputChannel.InputAxis': 'None',
        'ThrottleInputChannel.SourceBricks': [],
        'ThrottleInputChannel.Value': 1.0,
        'PitchInputChannel.InputAxis': 'None',
        'PitchInputChannel.SourceBricks': [],
        'PitchInputChannel.Value': 1.0,
        'YawInputChannel.InputAxis': 'None',
        'YawInputChannel.SourceBricks': [],
        'YawInputChannel.Value': 1.0,
        'RollInputChannel.InputAxis': 'None',
        'RollInputChannel.SourceBricks': [],
        'RollInputChannel.Value': 1.0
    }
)


# BRICKS. Last update: 1.7.4

_add_mk(bricks14, ('Brick_1x1x1s', 'Brick_1x1x1s_Flat', 'Brick_1x1x1', 'Brick_1x1x3', 'Brick_1x1x4',  'Brick_1x1x6',
        'Brick_2x1x1s', 'Brick_1x1x1s_Flat', 'BrickRounded_2x1x1s', 'BrickRounded_2x1x1s_Flat', 'Brick_2x1x1',
        'Brick_2x1x6', 'Brick_2x2x1s', 'Brick_2x2x1s_Flat', 'BrickRoundedCorner_2x2x1s', 'CornerBrick_2x2x1s',
        'Brick_2x2x1', 'CornerBrick_2x2x1', 'Brick_3x1x1s', 'Brick_3x1x1s_Flat', 'BrickRounded_3x1x1s',
        'BrickRounded_3x1x1s_Flat', 'Brick_3x1x1', 'Brick_3x2x1s', 'Brick_3x2x1s_Flat', 'Brick_3x2x1', 'Brick_4x1x1s',
        'Brick_4x1x1s_Flat', 'BrickRounded_4x1x1s',  'BrickRounded_4x1x1s_Flat', 'Brick_4x1x1', 'Brick_4x2x1s',
        'Brick_4x4x1s_Flat', 'Brick_5x1x1s', 'Brick_5x1x1s_Flat', 'BrickRounded_5x1x1s', 'BrickRounded_5x1x1s_Flat',
        'Brick_5x1x1', 'BrickRounded_5x1x1s', 'BrickRounded_5x1x1s_Flat', 'Brick_5x1x1', 'Brick_5x2x1s',
        'Brick_5x2x1s_Flat', 'Brick_5x2x1', 'Brick_6x1x1s', 'Brick_6x1x1s_Flat', 'BrickRounded_6x1x1s',
        'BrickRounded_6x1x1s_Flat', 'Brick_6x1x1', 'Brick_6x2x1s', 'Brick_6x2x1s_Flat', 'Brick_6x2x1', 'Weight_6x2x3',
        'Brick_6x4x1s', 'Brick_6x4x1s_Flat', 'Brick_6x6x1s', 'Brick_6x6x1s_Flat', 'Brick_8x1x1s', 'Brick_8x1x1s_Flat',
        'BrickRounded_8x1x1s', 'BrickRounded_8x1x1s_Flat', 'Brick_8x1x1', 'Brick_8x2x1s', 'Brick_8x2x1s_Flat',
        'Brick_8x2x1', 'Brick_8x4x1s', 'Brick_8x4x1s_Flat', 'Brick_8x6x1s', 'Brick_8x6x1s_Flat', 'Brick_8x8x1s',
        'Brick_8x8x1s_Flat', 'Brick_10x1x1s', 'Brick_10x1x1s', 'Brick_10x1x1', 'Brick_10x2x1s', 'Brick_10x2x1s_Flat',
        'Brick_10x2x1', 'Brick_10x4x1s', 'Brick_10x4x1s_Flat', 'Brick_10x6x1s', 'Brick_10x6x1s_Flat', 'Brick_10x8x1s',
        'Brick_10x8x1s_Flat', 'Brick_12x1x1s', 'Brick_12x1x1', 'Brick_12x6x1s', 'Brick_12x6x1s_Flat', 'Brick_12x8x1s',
        'Brick_12x8x1s_Flat', 'Brick_12x12x1', 'Brick_16x1x1', 'Brick_16x8x1s', 'Brick_16x8x1s_Flat', 'Brick_20x1x1',
        'Brick_24x12x1'),
    default_properties14() | {
        'bGenerateLift': False
    }
)


# CAMERAS. Last update: 1.7.4

_add_mk(bricks14, ('Camera_1sx1sx1s', 'Camera_2x1x1', 'TargetMaker_1x1x1'),
    default_properties14() | {
        'OwningSeat': None
    }
)


# COUPLINGS. Last update: 1.7.4

_add_mk(bricks14, ('Coupling_1sx1sx1s_Front_Female', 'Coupling_1x1x1s_Front_Female', 'Coupling_2x2x1s_Female',
        'Coupling_2x2x1s_Front_Female', 'Coupling_4x1x2s_Top'),
    default_properties14()
)

_add_mk(bricks14, ('Coupling_1sx1sx1s_Front_Male', 'Coupling_1x1x1s_Front_Male', 'Coupling_2x2x1s_Front_Male',
        'Coupling_2x2x1s_Male', 'Coupling_4x1x2s_Bottom', 'Coupling_6x2x1s_Male'),
    default_properties14() | {
        'CouplingMode': 'Static',
        'InputChannel.InputAxis': 'None',
        'InputChannel.SourceBricks': [],
        'InputChannel.Value': 1.0
    }
)


# DECORATIONS. Last update: 1.7.4

_add_mk(bricks14, ('ImageBrick', 'ImageCylinder'),
    default_properties14() | {
        'bGenerateLift': False,
        'BrickSize': [6.0, 6.0, 1.0],
        'ConnectorSpacing': [3, 3, 3, 3, 3, 0],
        'Image': 'Arrow',
        'ImageColor': [0, 0, 255]
    }
)

_add_mk(bricks14, ('Flag_3x1x2',),
    default_properties14() | {
        'bGenerateLift': False,
        'BrickSize': [6.0, 1.0, 6.0],
        'ConnectorSpacing': [3, 3, 3, 3, 3, 3],
        'Image': 'Arrow',
        'ImageColor': [0, 0, 255]
    }
)

_add_mk(bricks14, ('TextBrick', 'TextCylinder'),
    default_properties14() | {
        'bGenerateLift': False,
        'BrickSize': [6.0, 6.0, 1.0],
        'ConnectorSpacing': [3, 3, 3, 3, 3, 0],
        'Text': 'Text',
        'Font': 'Roboto',
        'FontSize': 60.0,
        'TextColor': [0, 0, 0],
        'OutlineThickness': 0.0
    }
)

_add_mk(bricks14, ('Antenna_1x1x8', 'Antenna_2x1x1s', 'Handle_1x2x4s', 'Handle_4x1x1'),
    default_properties14()
)

_add_mk(bricks14, ('Bumper_4sx6x2', 'Bumper_4sx8x7s', 'Door_L_3x1x1', 'Door_R_3x1x1', 'Door_L_3x1x2',
        'Door_R_3x1x2', 'WindowedDoor_L_3x1x4', 'WindowedDoor_R_3x1x4', 'Grid_2x1x1s_02', 'Grid_2x1x1s',
        'GridZylinder_2x2x1s', 'SteeringWheel_5sx5sx1s', 'SteeringWheel_2x2x1s'),
    default_properties14() | {
        'bGenerateLift': False
    }
)


# FIRE AND WATER. Last update: 1.7.4

_add_mk(bricks14, ('Float',),
    default_properties14() | {
        'BrickSize': [3.0, 3.0, 3.0],
        'ConnectorSpacing': [3, 3, 3, 3, 3, 0]
    }
)

_add_mk(bricks14, ('Detonator_1x1x1s',),
    default_properties14() | {
        'InputChannel.InputAxis': 'Action1',
        'InputChannel.SourceBricks': [],
        'InputChannel.Value': 1.0
    }
)

_add_mk(bricks14, ('PumpZylinder_2x2x2',),
    default_properties14() | {
        'InputChannel.InputAxis': 'None',
        'InputChannel.SourceBricks': [],
        'InputChannel.Value': 1.0
    }
)



##TEMPORTARY
_add_mk(bricks14, ('ScalableBrick', 'ScalableZylinder'),
        default_properties14() | {
            'BrickSize': [3.0, 3.0, 3.0],
            'ConnectorSpacing': [3, 3, 3, 3, 3, 3],
            'bGenerateLift': False
        })
