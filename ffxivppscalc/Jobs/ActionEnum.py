# This will contain all action with their IDs in the game. It will map from ids -> name or name -> ids
from enum import IntEnum # Importing enums

# Caster

class CasterActions(IntEnum):
    Swiftcast = 7561
    LucidDreaming = 7562
    Surecast = 7559
    Addle = 7560
    Sleep = 25880

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# BlackMage

class BlackMageActions(IntEnum):
    # Blackmage Actions
    Paradox = 25797
    FireI = 141
    FireII = 147
    FireIII = 152
    FireIV = 3577
    Despair = 16505
    Flare = 162
    HighFireII = 25794
    BlizzardI = 142
    BlizzardII = 25793
    BlizzardIII = 154
    BlizzardIV = 3576
    Freeze = 159
    HighBlizzardII = 25795
    UmbralSoul = 16505
    ThunderIII = 153
    ThunderIV = 7420
    Transpose = 149
    AetherialManipulation = 155
    Scathe = 156
    Manaward = 157
    Manafont = 158
    LeyLines = 3573
    Sharpcast = 3574
    BetweenTheLines = 7419
    Triplecast = 7421
    Foul = 7422
    Xeoglossy = 16507
    Amplifier = 25796

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

# RedMage

class RedmageActions(IntEnum):
    # RedMage actions
    Riposte = 7504
    Corps = 7506
    Verfire = 7510
    Verstone = 7511
    Zwerchhau = 7512
    Moulinet = 7513
    Vercure = 7514
    Redoublement = 7516
    Fleche = 7517
    Acceleration = 7518
    Contre = 7519
    Embolden = 7520
    Manafication = 7521
    Verraise = 7523
    Jolt = 7524
    Verthunder = 25855
    Verareo = 25856
    Impact = 16526
    Engagement = 16527
    Reprise = 16529
    MagickBarrier = 25857
    EnchantedRiposte = 7527
    EnchantedZwerchhau = 7528
    EnchantedRedoublement = 7529
    EnchantedMoulinet = 7530
    EnchantedReprise = 16528
    Resolution = 25858
    Verholy = 7526
    Verflare = 7525
    Scorch = 16530

    @classmethod
    def id_for_name(cls, id) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'Unknown'

    @classmethod
    def name_for_id(cls, name) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown





