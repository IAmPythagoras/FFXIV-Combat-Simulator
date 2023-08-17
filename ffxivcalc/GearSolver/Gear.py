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
    Piety = 6
    MainStat = 7
    WD = 8      

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
    
class Food:
    """
    This class represents food. Food gives a stat bonus that caps at a certain value.
    A food can be "attached" to a GearSet object and will buff it.
    statBonusDict : dict -> Dictionnary where key is the StatType's Name and the value is the cap of that stat with the percentage bonus.
    name : str -> Name of the food
    """

    def __init__(self, statBonusDict : dict, name : str):
        self.name = name
        self.statBonusDict = statBonusDict

    def __str__(self):
        strGenerator = (key + " " + str(int( 100 * self.statBonusDict[key][1])) + "% max of " + str(self.statBonusDict[key][0]) + " |" for key in self.statBonusDict)
        returnStr = "Food " + self.name + " gives -> "
        for gen in strGenerator:
            returnStr += gen
        return returnStr

    def getLimitStatBonus(self, StatName : str) -> int:
        """
        This function returns the limit of a stat for the food.
        StatName : str -> Name of the StatType.
        """

        return self.statBonusDict[StatName][0] if StatName in self.statBonusDict.keys() else 0
    
    def getPercentStatBonus(self, StatName : str) -> float:
        """
        This function  returns the percent bonus from the food for the given StatName
        StatName : str -> Name of the StatType.
        """
        return self.statBonusDict[StatName][1] if StatName in self.statBonusDict.keys() else 0
    

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
        self.illegalMeld = False # This is set to true when this piece of gear is illegaly Overmelded

        for Stats in StatList:
            self.Stat[StatType.name_for_id(Stats.StatType)] = Stats
                             # We look for the highest stat value
            if Stats.StatType != StatType.MainStat and Stats.Value > self.StatLimit : self.StatLimit = Stats.Value

        self.Materias = []   # List of Materia object associated
        self.MateriaLimit = MateriaLimit
        self.MateriasCount = 0

    def __str__(self):
        strGenerator = (str(self.Stat[key]) + " | " for key in self.Stat)
        materiaGenerator = (str(mat) + " | " for mat in self.Materias) if self.MateriasCount > 0 else ("" for i in range(0))
        strReturn = GearType.name_for_id(self.GearType) + " : "
        for stat in strGenerator:
            strReturn += stat
        strReturn += " Materias : "
        for mat in materiaGenerator:
            strReturn += mat

        return strReturn + " Name : " + self.Name

    def __addMateria(self, newMateria : Materia):
        """
        Private function called to add materia to the gear. This function is called by AddMateria and forceAddMateria.
        """
        StatName = StatType.name_for_id(newMateria.StatType)
        newStatValue = self.GetStat(StatName=StatName) + newMateria.Value
        if newStatValue > self.StatLimit:
                             # If true means the materia is wasting ressources.
            newMateria.wasteAmount = newStatValue - self.StatLimit
            newMateria.wasteValue = True

        self.Materias.append(newMateria)
        self.MateriasCount += 1

    def __hasStatType(self, type : StatType) -> bool:
        """
        This private function returns weither the given StatType has non zero value for this gear.
        """
        return (StatType.name_for_id(type) in self.Stat.keys()) and self.hasStatMeld(type)

    def AddMateria(self, newMateria : Materia):
        """
        This function adds a Materia Object to the gear. It will also flag the materia if stat is wasted.
        """

        if len(self.Materias) >= self.MateriaLimit :
            raise MateriaOverflow

        self.__addMateria(newMateria)

    def forceAddMateria(self, newMateria : Materia):
        """
        This function force adds a materia onto the gear. If the gear has reached its maximum materia count
        it will be flagged as "illegal". This function will never raise the MateriaOverflow error.
        """

        if len(self.Materias) >= self.MateriaLimit:
            self.illegalMeld = True

        self.__addMateria(newMateria)

    def hasValidMelding(self) -> bool:
        return not self.illegalMeld

    def getNumberPossibleMateria(self, type : StatType, matGen : MateriaGenerator) -> int:
        """
        This function returns the total number of materia that can be added to the gear with no loss
        of the given stat type. It uses the matGen to find the stat bonus from these materias. It is assumed
        we will use even numbered materia.
        type : StatType -> Type of the stat
        matGen : MateriaGenerator -> Materia generator used to add materias.
        """
        statName = StatType.name_for_id(type)
        statLimitMateria = (self.StatLimit - self.GetStat(StatName=statName)) // matGen.EvenValue
        return min(self.MateriaLimit,statLimitMateria)

    def getMateriaNumber(self, dictData : dict):
        """
        This function returns the number of materia of each StatTypes currently on this gear piece as well
        as if the materia is even or odd.
        (Out) dictData : dict -> This dictionnary is filled with the information. It can hence be passed on every gear pieces of the gear set.
        """

        for mat in self.Materias:
            statName = StatType.name_for_id(mat.StatType)
            if statName in dictData.keys():
                dictData[statName] += 1
            else :
                dictData[statName] = 1

    def canAddMateriaNoLoss(self, newMateria : Materia) -> bool:
        """
        This function returns weither the materia can be added to the gear piece
        without stat loss.
        """
        StatName = StatType.name_for_id(newMateria.StatType)
        return (self.MateriasCount < self.MateriaLimit and 
                (self.GetStat(StatName) if StatName in self.Stat.keys() else 0) + newMateria.Value <= self.StatLimit)
    
    def canReplaceMateriaNoLoss(self, newMateria : Materia) -> bool:
        """
        This function returns True if a materia of the gear piece can be replaced by a new materia
        without stat loss
        """
        StatName = StatType.name_for_id(newMateria.StatType)
        return (self.GetStat(StatName) if StatName in self.Stat.keys() else 0) + newMateria.Value <= self.StatLimit
    
    def hasMateriaType(self, type : StatType) -> bool:
        """
        This function returns weither the gear piece has a materia of the given type
        """
        for mat in self.Materias:
            if mat.StatType == type : return True
        return False

    def ResetMateriaSlot(self):
        """
        This function resets the materias of the gear
        """
        self.Materias = []
        self.MateriasCount = 0

    def removeMateriaType(self, statType : StatType):
        """
        This function removes the first materia of the given StatType found on the gear
        """
        for mat in self.Materias:
            if mat.StatType == statType:
                self.MateriasCount -= 1
                self.Materias.remove(mat)
                break
                        # Check if now is valid meld
        if self.illegalMeld:
            if self.MateriasCount <= self.MateriaLimit: self.illegalMeld = False

    def hasStatMeld(self, type : StatType) -> bool:
        """
        This function returns true if the gear has the given stattype melded to it.
        """

        for mat in self.Materias:
            if mat.StatType == type : return True
        return False

    def GetStat(self, StatName : str = "", StatEnum : int = -2) -> int:
        """
        This function returns the  statv alue associated with thhe given StatEnum value
        or the StatName.
        """

        if StatName == "" and StatEnum == -2 : raise InvalidStatRequest

        statValue = 0

        if StatEnum != -2 :
            name = StatType.id_for_name(StatEnum)
            statValue = self.Stat[name].Value if StatName in self.Stat.keys() else 0
        elif StatName != "":
            statValue = self.Stat[StatName].Value if StatName in self.Stat.keys() else 0

        StatEnum = StatType.id_for_name(StatName) if StatEnum == -2 else StatEnum

        for Materia in self.Materias:
            if Materia.StatType == StatEnum:
                statValue = min(Materia.Value + statValue, self.StatLimit)
        
        return statValue
    
    def getGearTypeName(self) -> str:
        """
        This function returns the type of the gear.
        """
        return GearType.name_for_id(self.GearType)
    
    def getMateriaTypeList(self, IgnoreSpeedMateria : bool = True) -> list[StatType]:
        """
        This function returns a list of all present materia's stattype on the gear.
        """
        statTypeList = []
        for mat in self.Materias:
            if not (mat.StatType in statTypeList) and not ((mat.StatType == StatType.SS or mat.StatType == StatType.SkS) and IgnoreSpeedMateria): 
                statTypeList.append(mat.StatType)
        return statTypeList
    
    def getNumberMateria(self) -> int:
        """
        This function returns the number of materia on this gear
        """
        return len(self.Materias)
    
class GearSet:
    """
    This class corresponds to a gearset. A player can have a gear set. A gear set is a list of Gear.
    """

    def __init__(self):
        self.GearSet = {}
        self.Food = None

    def __iter__(self):
        self.gearSetIter = iter(self.GearSet)
        return self

    def __next__(self):
        key = next(self.gearSetIter)
        return self.GearSet[key]

    def removeMateriaType(self, StatType):
        """
        This function removes the first materia of the valid StatType found in every gear piece.
        """
        for key in self.GearSet:
            self.GearSet[key].removeMateriaType(StatType)

    def removeFirstFoundMateriaInvalidPiece(self, type : StatType) -> str:
        """
        This function removes the first found materia of the given type on an invalid gear piece.
        If none is found the function returns None and otherwise it returns the name of the gear piece.
        """

        for gear in self:
            if not gear.hasValidMelding() and gear.hasStatMeld(type): 
                gear.removeMateriaType(type)
                return gear.getGearTypeName()
        return None

    def removeMateriaSpecGear(self, gearName : str, type : StatType):
        """
        This function removes the first materia of the given type from the given gear of the gear set
        """

        if gearName in self.GearSet.keys():
            self.GearSet[gearName].removeMateriaType(type)

    def addFood(self, newFood : Food):
        """
        This function adds newFood to the gearset.
        """
        self.Food = newFood

    def removeFood(self):
        """
        This function removes the food on the gear set.
        """
        self.Food = None

    def __str__(self):
        gearInfoGenerator = (str(self.GearSet[gear]) + "\n" for gear in self.GearSet)
        GearInfo = ""
        for info in gearInfoGenerator:
            GearInfo += info

        return "Gearset's info:\n" + GearInfo + " Final Stats : " + str(self.GetGearSetStat()) + "\n" + self.strMateriaNumber() + "\n" + str(self.Food)

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

    def strMateriaNumber(self) -> str:
        """
        This function find the number of materia in the gear set and displays it in an easy way to understand.
        """

        dataDict = {}

        for key in self.GearSet:
            self.GearSet[key].getMateriaNumber(dataDict)
        
        returnStr = "Materia numbers : "

        for stat in dataDict:
            returnStr += stat + " " + str(dataDict[stat]) + "x" + " |"
        
        return returnStr

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
    
    def getMateriaTypeLimit(self, type : StatType, matGen : MateriaGenerator) -> int:
        """
        This function returns the total number of even materia (of the given MateriaGenerator object) of a given type the gear set can additionally receive.
        
        type : StatType -> Type of the materia
        matGen : MateriaGenerator : -> Materia Generator
        """

        limit = 0
        for gear in self:
            limit += gear.getNumberPossibleMateria(type, matGen)
        return limit
    
    def getNumberMateria(self) -> int:
        """
        This function returns the current number of materia on the gear set.
        """
        total = 0
        for gear in self: total += gear.getNumberMateria()
        return total
    
    def ResetGearSet(self):
        self.GearSet = {}
        
    def GetGearSetStat(self):
        Stat = {
        "MainStat" : 450,
        "WD" : 0,
        "Det" : 390,
        "Ten" : 400,
        "SS" : 400,
        "SkS" : 400,
        "Crit" : 400,
        "DH" : 400,
        "Piety" : 390
    }       
        
                             # Getting stats from gear and materia
        for key in self.GearSet:
            GearPiece = self.GearSet[key]
            for type in StatType:
                Stat[type.name] += GearPiece.GetStat(type.name)

                             # Getting stats from food
        if self.Food != None:
            for type in StatType:
                percentBonus = self.Food.getPercentStatBonus(type.name)
                limitBonus = self.Food.getLimitStatBonus(type.name)

                if percentBonus != 0:
                    flatBonus = min(int(percentBonus * Stat[type.name]), limitBonus)
                    Stat[type.name] += flatBonus

        return Stat
    
    def hasValidMelding(self) -> bool:
        """
        This function returns weither all pieces in the GearSet have valid melding
        """
        valid = True
        for gear in self:
            valid = valid and gear.hasValidMelding()
        return valid
    
    def getMateriaTypeList(self, IgnoreSpeedMateria : bool = True, ignoreValidMeld : bool = False) -> list[StatType]:
        """
        This function returns a list of type of the materias present in the gear set
        IgnoreSpeedMateria : bool -> If true the function will only return non Speed related stattype.
        ignoreValidMeld : bool -> If true, function only returns materias type that are on at least one gear with invalidMelding.
        """
        statTypeList = []
        for gear in self:
            if not (gear.hasValidMelding() and ignoreValidMeld) : statTypeList += [type for type in gear.getMateriaTypeList(IgnoreSpeedMateria=IgnoreSpeedMateria) if not (type in statTypeList)]
        return statTypeList    

def ImportGear(fileName : str) -> dict:
    """
    This function imports a list of gear. It reads the given file and will output a dictionnary with heach
    gear type as key with a list of all gear of that type in the import file.
    fileName : str -> Name of the file. Must be formatted correctly
    """

    f = open(fileName) #Opening save

    data = json.load(f) #Loading json file

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

if __name__ == "__main__":
    from ffxivcalc.GearSolver.Solver import computeDamageValue, getGearDPSValue
    matGen = MateriaGenerator(18, 36)
    foodDict = {"Crit" : [63, 0.1], "Det" : [103, 0.1]}
    raidFood = Food(foodDict, "Baked Eggplant")

    data = ImportGear("DRKGear.json")
    Crit = 0
    DH = 1
    Det = 2
    SS = 3
    SkS = 4
    Weapon = data["WEAPON"][0]
    Weapon.AddMateria(matGen.GenerateMateria(4))
    Weapon.AddMateria(matGen.GenerateMateria(4))

    Head = data["HEAD"][0]
    Head.AddMateria(matGen.GenerateMateria(4))
    Head.AddMateria(matGen.GenerateMateria(4))

    Body = data["BODY"][1]
    Body.AddMateria(matGen.GenerateMateria(4))
    Body.AddMateria(matGen.GenerateMateria(4))

    Hand = data["HANDS"][0]
    Hand.AddMateria(matGen.GenerateMateria(1))
    Hand.AddMateria(matGen.GenerateMateria(1))

    Leg = data["LEGS"][0]
    Leg.AddMateria(matGen.GenerateMateria(1))
    Leg.AddMateria(matGen.GenerateMateria(1))

    Feet = data["FEET"][1]
    Feet.AddMateria(matGen.GenerateMateria(1))
    Feet.AddMateria(matGen.GenerateMateria(1))

    Ear = data["EARRINGS"][1]
    Ear.AddMateria(matGen.GenerateMateria(1))
    Ear.AddMateria(matGen.GenerateMateria(1))

    Neck = data["NECKLACE"][0]
    Neck.AddMateria(matGen.GenerateMateria(1))
    Neck.AddMateria(matGen.GenerateMateria(1))

    Bracelet = data["BRACELETS"][1]
    Bracelet.AddMateria(matGen.GenerateMateria(1))
    Bracelet.AddMateria(matGen.GenerateMateria(1))

    Lring = data["LRING"][0]
    Lring.AddMateria(matGen.GenerateMateria(1))
    Lring.AddMateria(matGen.GenerateMateria(1))

    ring = data["RING"][0]
    ring.AddMateria(matGen.GenerateMateria(1))
    ring.AddMateria(matGen.GenerateMateria(1))

    gSet = GearSet()
    gSet.AddGear(Weapon)
    gSet.AddGear(Head)
    gSet.AddGear(Body)
    gSet.AddGear(Hand)
    gSet.AddGear(Leg)
    gSet.AddGear(Feet)
    gSet.AddGear(Ear)
    gSet.AddGear(Neck)
    gSet.AddGear(Bracelet)
    gSet.AddGear(Lring)
    gSet.AddGear(ring)
    gSet.addFood(raidFood)

    print(gSet)