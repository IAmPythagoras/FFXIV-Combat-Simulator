# This file will contain the enums of all jobs and class
from enum import IntEnum # Importing enums

class PlayerEnum(IntEnum):
    # Parent enum class for all other enums. Will have
    # the two functions.

    @classmethod
    def name_for_id(cls, id : int) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def id_for_name(cls, name : str) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown


class RoleEnum(PlayerEnum):
    # Enum for all roles

    Caster = 1
    Healer = 2
    Melee = 3
    Tank = 4
    PhysicalRanged = 5


class JobEnum(PlayerEnum):
    # Enum for all jobs

    # Caster
    BlackMage = 1
    Summoner = 2
    RedMage = 3

    # Healer
    WhiteMage = 4
    Astrologian = 5
    Sage = 6
    Scholar = 7

    # Melee
    Ninja = 8
    Samurai = 9
    Reaper = 10
    Monk = 11
    Dragoon = 12

    # Tank
    Gunbreaker = 13
    DarkKnight = 14
    Paladin = 15
    Warrior = 16

    # Physical ranged
    Machinist = 17
    Bard = 18
    Dancer = 19

    # Pet
    Pet = 20
