from dataclasses import dataclass, field
from typing import Tuple, Optional, List

from model_enums import *


''' ------------------------- DATA CLASSES ------------------------- '''

# maybe don't need this since SAP default has A992Fy50
""" @dataclass
class MaterialProperty:
    name: str 
    type: MaterialType # 1=steel, 2=concrete, 3=nodesign, 4=aluminum, 5=coldform, 6=rebar, 7=tendon
    elastic_mod: float
    poisson: float
    thermal_coeff: float """

@dataclass
class SectionProperty:
    name: str
    material: str

# inherit from SectionProperty
# Hollow steel section tube
@dataclass
class HSSTProperty(SectionProperty):
    depth: float 
    width: float
    flange_thickness: float
    web_thickness: float
    corner_radius: float

# Hollow steel section square
@dataclass
class HSSSProperty(SectionProperty):
    depth: float 
    width: float
    flange_thickness: float
    web_thickness: float
    corner_radius: float

# hollow steel section round
@dataclass
class HSSRProperty(SectionProperty):
    diameter: float
    thickness: float

@dataclass
class AngleProperty(SectionProperty):
    long_leg: float
    short_leg: float
    long_thickness: float
    short_thickness: float
    fillet_radius: float

@dataclass
class DoubleAngleProperty(SectionProperty):
    total_depth: float
    single_width: float
    horizontal_thickness: float
    vertical_thickness: float
    back_distance: float
    fillet_radius: float

@dataclass
class FrameMember:
    name: str
    start: Tuple[float, float, float]  # (x, y, z) coordinate
    end: Tuple[float, float, float]    # (x, y, z) coordinate
    section: SectionProperty # string section property name
    coordinate_system: str # ex. 'Global'
    start_restraint: Optional[Tuple[bool, bool, bool, bool, bool, bool]] = None # 6DOF restraint
    end_restraint: Optional[Tuple[bool, bool, bool, bool, bool, bool]] = None # 6DOF restraint
    start_release: Optional[Tuple[bool, bool, bool, bool, bool, bool]] = None
    end_release: Optional[Tuple[bool, bool, bool, bool, bool, bool]] = None
    point_loads: Optional[List["PointLoad"]] = None
    distributed_loads: Optional[List["DistributedLoad"]] = None

    # enforce expected structure
    def __post_init__(self):
        if len(self.start) != 3:
            raise ValueError(f"'start' must be a 3-tuple")
        if len(self.end) != 3:
            raise ValueError(f"'end' must be a 3-tuple")
        if (self.start_restraint != None) and (len(self.start_restraint) != 6) :
            raise ValueError(f"'start_restraint' must be a 6-tuple")
        if (self.end_restraint != None) and (len(self.end_restraint) != 6):
            raise ValueError(f"end_restraint must be a 6-tuple")

@dataclass 
class LoadPattern:
    name: str
    type: LoadType # see LoadType in model_enums
    self_weight: int 
    add_load_case: bool # if true, linear static load case is added

@dataclass
class PointLoad:
    location: PointLoadLocation # either start or end
    load_case: str # should verify if this load case exists when instantiating
    load_value: Tuple[float, float, float, float, float, float] # xyz force, xyz moment

    def __point__init__(self):
        if len(self.load_value) != 6:
            raise ValueError(f"'load_value' must be a 6-tuple")

@dataclass
class DistributedLoad:
    load_case: str # should verify if this load case exists when instantiating
    load_type: DistributedLoadType
    load_direction: LoadDirection
    dist_1: float # distance from end I (first point) of frame 
    dist_2: float # distance from end J (second point) of frame
    val_1: float
    val_2: float 
    coordinate_system: Optional[str] = None

