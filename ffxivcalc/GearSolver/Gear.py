"""
This file contains the class for representing gear pieces. It will also contain the class
GearSet which represents a gear set. A player can be given a gear set and will see its stats change
according to the gear set. Every piece of gear will act the same way a piece does in the game.
It will have possible melds (and a limit) and will have stat caps such that some melds do nothing.

This will also contain the Enum "GearType" which will differentiate the type of piece a gear is,
"Food" which can affect a player's stats, Materias which will affect a gear's stats.
"""

from ffxivcalc.helperCode.exceptions import MateriaOverflow, InvalidStatRequest
import json

from enum import IntEnum

class GearType(IntEnum):
    WEAPON = 0
    SHIELD = 1               # Only Paladin has a shield
    HEAD = 2
    BODY = 3
    HANDS = 4
    LEGS = 5
    FEET = 6
    EARRINGS = 7
    NECKLACE = 8
    BRACELETS = 9
    LRING = 10               # Left Ring
    RING = 11                # Right Ring

    @classmethod
    def name_for_id(cls, id : int) -> str:
        # maps from id -> name
        if id in cls.__members__.values():
            return cls(id).name
        return 'INVALID'      
    
    @classmethod
    def id_for_name(cls, name : str) -> int:
        # maps from name -> id
        if name in cls.__members__.keys():
            return cls[name].value
        return -1 # Evaluated as Unknown

class StatType(IntEnum):
    Crit = 0
    DH = 1
    Det = 2
    SS = 3
    SkS = 4
    Ten = 5
    MainStat = 6
    WD = 7      

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

class Stat:
    """
    This class represents a stat on a gear piece.
    StatType -> Type of the stat
    Value -> Value of the stat
    """

    def __init__(self, StatType : StatType, Value : int):
        self.StatType = StatType
        self.Value = Value

    def __str__(self):
        return StatType.name_for_id(self.StatType) + " : " + str(self.Value)

class Materia:
    """
    This class represents a Materia. Gear pieces can have materias,
    Materias have certain types. The increment in stat value is created when creating a "MateriaGenerator"
    object that will generate materias when requested. This lets the user create arbitrary Materias.
    StatType -> Type of the stat
    Value : int -> Value of the bonus stat given by this materia
    """

    def __init__(self, StatType : StatType, Value : int):
        self.StatType = StatType
        self.Value = Value
                             # Information related to if the materia wastes values.
        self.wasteValue = False
        self.wasteAmount = 0

    def __str__(self):
        return StatType.name_for_id(self.StatType) + " : " + str(self.Value) + (" Waste : " + str(self.wasteAmount) if self.wasteValue else "")

class MateriaGenerator:
    """
    This class will generate Materias. It will allow to specify an Even numbered bonus and an odd numbered bonus
    OddValue : int -> Bonus stat given if materia is odd numbered
    EvenValue : int -> Bonus stat given if materia is even numbered
    """
    
    def __init__(self, OddValue : int, EvenValue : int):
        self.OddValue = OddValue
        self.EvenValue = EvenValue

    def GenerateMateria(self,StatType : StatType, Even : bool = True) -> Materia:
        """
        This function generates a Materia. Defaults to an even numbered materia
        StatType -> Type of the stat
        Even : bool -> True if even numbered. False if odd (Defaults to True)
        """
        return Materia(StatType, self.EvenValue if Even else self.OddValue)

class Gear:
    """
    This class represent a gear piece.
    GearType -> Type of the gear piece
    StatList : list(Stat) -> List of all stat of the gear piece.
    MateriaLimit : int -> Limit of materia the gear can receive.
    Name : str -> Used to differentiate same type gear
    """
    def __init__(self, GearType : GearType, StatList : list, MateriaLimit : int = 2, Name : str = ""):
        self.GearType = GearType
        self.Stat = {}
        self.Name = Name
        self.StatLimit = 0   # StatLimit of a gear is always equal to the highest stat of it.

        for Stats in StatList:
            self.Stat[StatType.name_for_id(Stats.StatType)] = Stats
                             # We look for the highest stat value
            if Stats.Value > self.StatLimit : self.StatLimit = Stats.Value

        self.Materias = []   # List of Materia object associated
        self.MateriaLimit = MateriaLimit
        self.MateriasCount = 0

    def __str__(self):
        strGenerator = (str(self.Stat[key]) + " | " for key in self.Stat)
        materiaGenerator = (str(mat) + " | " for mat in self.Materias) if self.MateriasCount > 0 else ("" for i in range(0))
        strReturn = GearType.name_for_id(self.GearType) + " : "
        for stat in strGenerator:
            strReturn += stat

        for mat in materiaGenerator:
            strReturn += mat

        return strReturn + " Name : " + self.Name


    def AddMateria(self, newMateria : Materia):
        """
        This function adds a Materia Object to the gear. It will also flag the materia if stat is wasted.
        """

        if len(self.Materias) >= self.MateriaLimit :
            raise MateriaOverflow

        self.Materias.append(newMateria)
        self.MateriasCount += 1
        StatName = StatType.name_for_id(newMateria.StatType)
        newStatValue = (self.Stat[StatName].Value if StatName in self.Stat.keys() else 0)  + newMateria.Value
        if newStatValue > self.StatLimit:
                             # If true means the materia is wasting ressources.
            newMateria.wasteAmount = newStatValue - self.StatLimit
            newMateria.wasteValue = True

    def canAddMateriaNoLoss(self, newMateria : Materia) -> bool:
        """
        This function returns weither the materia can be added to the gear piece
        without stat loss.
        """
        StatName = StatType.name_for_id(newMateria.StatType)
        return (self.MateriasCount < self.MateriaLimit and 
                (self.GetStat(StatName=StatName) if StatName in self.Stat.keys() else 0) + newMateria.Value <= self.StatLimit)

    def ResetMateriaSlot(self):
        """
        This function resets the materias of the gear
        """
        self.Materias = []
        self.MateriasCount = 0
        

    def GetStat(self, StatName : str = "", StatEnum : int = -2) -> int:
        """
        This function returns the  statv alue associated with thhe given StatEnum value
        or the StatName.
        """

        if StatName == "" and StatEnum == -2 : raise InvalidStatRequest

        statValue = 0

        if StatEnum != -2 :
            name = StatType.id_for_name(StatEnum)
            if name in self.Stat.keys(): 
                statValue = self.Stat[name].Value if StatName in self.Stat.keys() else 0
        elif StatName != "":
            if StatName in self.Stat.keys():
                statValue = self.Stat[StatName].Value if StatName in self.Stat.keys() else 0

        StatEnum = StatType.id_for_name(StatName) if StatEnum == -2 else StatEnum

        for Materia in self.Materias:
            if Materia.StatType == StatEnum:
                statValue = min(Materia.Value + statValue, self.StatLimit)
        
        return statValue
            
class GearSet:
    """
    This class corresponds to a gearset. A player can have a gear set. A gear set is a list of Gear.
    """

    def __init__(self):
        self.GearSet = {}

    def __str__(self):
        gearInfoGenerator = (str(self.GearSet[gear]) + "\n" for gear in self.GearSet)
        GearInfo = ""
        for info in gearInfoGenerator:
            GearInfo += info
        return "Gearset's info:\n" + GearInfo + " Final Stats : " + str(self.GetGearSetStat())

    def findFirstPieceMateria(self, newMateria : Materia) -> str:
        """
        This function returns the key to the first piece of gear
        in the gear set that can have the newMateria attached to it
        without loss. If none is found, the function returns None
        """
        for key in self.GearSet:
            if self.GearSet[key].canAddMateriaNoLoss(newMateria):
                return key
        return None

    def AddGear(self, newGear : Gear):
        """
        This function is used to add a new gear to the gear set. If a gear of the type is already present it is switched.
        """
        self.GearSet[GearType.name_for_id(newGear.GearType)] = newGear
    def RemoveGear(self, Type : int):
        """
        This function removes the gear of the given type. If the gear set does not have the gear type then nothing happens.
        """
        name = GearType.name_for_id(Type)
        if name in self.GearSet:
            self.GearSet.pop(name)

    def getMateriaLimit(self) -> int:
        """
        This function returns the total number of materia the GearSet can receive, as well
        as the total of Odd and Even it can receive.

        FOR NOW ASSUMES ALL MATERIAS ARE EVEN
        """
        limit = 0
        for key in self.GearSet:
            limit += self.GearSet[key].MateriaLimit
        return limit

    def ResetGearSet(self):
        self.GearSet = {}
        
    def GetGearSetStat(self):
        Stat = {
        "MainStat" : 0,
        "WD" : 0,
        "Det" : 390,
        "Ten" : 400,
        "SS" : 400,
        "SkS" : 400,
        "Crit" : 390,
        "DH" : 390
    }   

        for key in self.GearSet:
            GearPiece = self.GearSet[key]
            for type in StatType:
                Stat[type.name] += GearPiece.GetStat(type.name)

        return Stat
    

def ImportGear(fileName : str) -> dict:
    """
    This function imports a list of gear. It reads the given file and will output a dictionnary with heach
    gear type as key with a list of all gear of that type in the import file.
    fileName : str -> Name of the file. Must be formatted correctly
    """

    #f = open(fileName) #Opening save

    #data = json.load(f) #Loading json file
    data = [
{
"GearType" : 0,
"MateriaLimit" : 2,
"Name" : "Raid",
"StatList" : [
["Crit", 306],
["SS", 214],
["MainStat", 416],
["WD", 132]
]},
{
"GearType" : 0,
"MateriaLimit" : 2,
"Name" : "Tome",
"StatList" : [
["Crit", 212],
["SS", 303],
["MainStat", 409],
["WD", 131]
]},
{
"GearType" : 2,
"MateriaLimit" : 2,
"Name" : "Raid",
"StatList" : [
["SS", 184],
["Det", 129],
["MainStat", 248]
]},
{
"GearType" : 2,
"MateriaLimit" : 2,
"Name" : "Tome",
"StatList" : [
["Crit", 184],
["DH", 129],
["MainStat", 248]
]},
{
"GearType" : 3,
"MateriaLimit" : 2,
"Name" : "Raid",
"StatList" : [
["SS", 292],
["DH", 204],
["MainStat", 394]
]},
{
"GearType" : 3,
"MateriaLimit" : 2,
"Name" : "Tome",
"StatList" : [
["Crit", 292],
["Det", 204],
["MainStat", 394]
]},
{
"GearType" : 4,
"MateriaLimit" : 2,
"Name" : "Raid",
"StatList" : [
["Det", 129],
["Crit", 184],
["MainStat", 248]
]},
{
"GearType" : 4,
"MateriaLimit" : 2,
"Name" : "Tome",
"StatList" : [
["SS", 184],
["DH", 129],
["MainStat", 248]
]},
{
"GearType" : 5,
"MateriaLimit" : 2,
"Name" : "Raid",
"StatList" : [
["Crit", 204],
["DH", 292],
["MainStat", 394]
]},
{
"GearType" : 5,
"MateriaLimit" : 2,
"Name" : "Tome",
"StatList" : [
["Det", 292],
["SS", 204],
["MainStat", 394]
]},
{
"GearType" : 6,
"MateriaLimit" : 2,
"Name" : "Raid",
"StatList" : [
["Det", 184],
["SS", 129],
["MainStat", 248]
]},
{
"GearType" : 6,
"MateriaLimit" : 2,
"Name" : "Tome",
"StatList" : [
["Crit", 129],
["DH", 184],
["MainStat", 248]
]},
{
"GearType" : 7,
"MateriaLimit" : 2,
"Name" : "Raid",
"StatList" : [
["Crit", 145],
["Det", 102],
["MainStat", 196]
]},
{
"GearType" : 7,
"MateriaLimit" : 2,
"Name" : "Tome",
"StatList" : [
["DH", 102],
["SS", 145],
["MainStat", 196]
]},
{
"GearType" : 8,
"MateriaLimit" : 2,
"Name" : "Raid",
"StatList" : [
["SS", 102],
["DH", 145],
["MainStat", 196]
]},
{
"GearType" : 8,
"MateriaLimit" : 2,
"Name" : "Tome",
"StatList" : [
["Det", 145],
["Crit", 102],
["MainStat", 196]
]},
{
"GearType" : 9,
"MateriaLimit" : 2,
"Name" : "Raid",
"StatList" : [
["Crit", 145],
["Det", 102],
["MainStat", 196]
]},
{
"GearType" : 9,
"MateriaLimit" : 2,
"Name" : "Tome",
"StatList" : [
["Det", 145],
["SS", 102],
["MainStat", 196]
]},
{
"GearType" : 10,
"MateriaLimit" : 2,
"Name" : "Raid",
"StatList" : [
["Det", 102],
["Crit", 145],
["MainStat", 196]
]},
{
"GearType" : 11,
"MateriaLimit" : 2,
"Name" : "Raid",
"StatList" : [
["SS", 102],
["DH", 145],
["MainStat", 196]
]}
]
    GearDict = {}


    for GearPiece in data:
        type = GearType.name_for_id(GearPiece["GearType"])
        StatList = [Stat(StatType.id_for_name(S[0]), S[1]) for S in GearPiece["StatList"]]
        ImportedGear = Gear(GearPiece["GearType"], StatList, MateriaLimit = GearPiece["MateriaLimit"], Name = GearPiece["Name"])
        if type in GearDict.keys():
            GearDict[type].append(ImportedGear)
        else:
            GearDict[type] = [ImportedGear]

    return GearDict




