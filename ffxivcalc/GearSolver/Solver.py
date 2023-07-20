"""
This file contains the logic of the Gear Solver.

The algorithm requires one Fight Object that will be used to compute the DPS. The algorithm will use
the pre-baked simulation in order to quickly simulate the DPS given some gear configuration.
One list of Gear from which to search, the space of materias that are available, etc.

For now the BiS Solver will only work if the Fight has one player variable, meaning it can only solve the BiS for one 

"""

from ffxivcalc.GearSolver.Gear import GearSet, MateriaGenerator, GearType
from ffxivcalc.Jobs.PlayerEnum import RoleEnum, JobEnum
from ffxivcalc.helperCode.exceptions import InvalidFoodSpace, InvalidGearSpace, InvalidMateriaSpace, InvalidFunctionParameter
from math import floor
from copy import deepcopy
import os


def getBaseStat():
    """
    This function returns a base stat dictionnary
    """

    return {
        "MainStat" : 450,
        "WD" : 0,
        "Det" : 390,
        "Ten" : 400,
        "SS" : 400,
        "SkS" : 400,
        "Crit" : 390,
        "DH" : 390
    }  

def computeDamageValue(GearStat : dict, JobMod : int, IsTank : bool, IsCaster : bool):
    """
    this function computes all the damage values given a stat dict.
    GearStat : dict -> Dict containing the value of all stats.
    JobMod : int -> JobMod value of the player.
    IsTank : bool -> True if the player is a tank
    IsCaster : bool -> True if the player is a caster (Magical Ranged or Healer)
    """
    levelMod = 1900
    baseMain = 390  
    baseSub = 400# Level 90 LevelMod values

    f_WD = (GearStat["WD"]+floor(baseMain*JobMod/1000))/100 # Necessary to check if its not 0 since etro only returns the damage multiplier.
    f_DET = floor(1000+floor(140*(GearStat["Det"]-baseMain)/levelMod))/1000# Determination damage
    if IsTank : f_TEN = (1000+floor(100*(GearStat["Ten"]-baseSub)/levelMod))/1000 # Tenacity damage, 1 for non-tank player
    else : f_TEN = 1 # if non-tank
    f_SPD = (1000+floor(130*((GearStat["SS"] if IsCaster else GearStat["SkS"])-baseSub)/levelMod))/1000 # Used only for dots
    f_CritRate = floor((200*(GearStat["Crit"]-baseSub)/levelMod+50))/1000 # Crit rate in decimal
    f_CritMult = (floor(200*(GearStat["Crit"]-baseSub)/levelMod+400))/1000 # Crit Damage multiplier
    f_DH = floor(550*(GearStat["DH"]-baseSub)/levelMod)/1000 # DH rate in decimal
    return f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH

def BiSSolver(Fight, GearSpace : dict, MateriaSpace : list, FoodSpace : list, PercentileToOpt : list = ["exp", "99", "90", "75", "50"],
              materiaDepthSearchIterator : int = 5, randomIteration : int = 10000, oddMateriaValue : int = 18, evenMateriaValue : int = 36,
              PlayerIndex : int = 0, maxSPDValue : int = 5000):
    """
    Finds the BiS of the player given a Gear search space and a Fight. The Solver will output to a file named
    bisSolver[Job]Result[number].txt with all the relevant information and returns the gearSets. The solver outputs the best Expected Damage GearSet as well as
    the best GearSet for the 50th, 75th, 90th and 99th DPS. The solver requires at least one piece of every possible slots.
    Note that is is possible to give a "prebaked" BiS by only giving 1 choice for some pieces and that it is also possible to
    add materias to the pieces in the GearSpace before running the solver. 
    Note that since the percentile's BiS are using random damage this is only an approximation and might miss the actual best in slot. So it 
    is recommended to run this solver multiple times or with very high value of randomIteration. Furthermore, using BF algorithm to look
    for all (usually) 22 best melds at the same time is impossible due to how large the search space would be, this code takes adds materia iteratively
    which makes the computation faster, but is also not guaranteed to give the true BiS. The solver finds the best GearSet without melds first, then finds the best
    meldings and then finds the best food. 
    Fight -> Fight object.
    GearSpace : dict -> Dictionnary filled with the different gear pieces the algorithm can search through. Must have at least one of each gear types
    Materiaspace : list -> List of all the stats the solver will look through when optimizing melds. Must be at least 3 materias
    FoodSpace : list -> List of all food to look into. Must be non-empty
    PercentileToOpt : list -> List of all gearset to optimize. Exp means to optimize expected damage.
    materiaDepthSearchIterator : int -> Depth for which the Materia optimization searches into per step.
    randomIteration : int -> Number of times the solver will simulate random runs. Must be at least 100
    oddMateriaValue : int -> Stat gained from odd Materia
    evenMateriaValue : int -> Stat gained from even Materia
    PlayerIndex : int -> Index of the player for which the user wants to optimize the gearset. 
                                Must be the index of the player in the Fight.PlayerList.
    maxSPDValue : int -> Max Spell Speed or skill Speed value. Every gear set above that value will be discarded.
    """

                             # Checking the validity of the given search space and some other parameters.
    if materiaDepthSearchIterator <= 0: raise InvalidFunctionParameter("BisSolver", "materiaDepthSearchIterator", "Must be higher than 1.")
    if randomIteration < 100 : raise InvalidFunctionParameter("BisSolver", "randomIteration", "Must be higher than or 100")
    if PlayerIndex < 0 or PlayerIndex > len(Fight.PlayerList) - 1: raise InvalidFunctionParameter("BisSolver", "PlayerIndex", "Invalid index value")
    expectedGearSpaceKeys = ["WEAPON", "HEAD", "BODY", "HANDS", "LEGS", "FEET", "EARRINGS", "NECKLACE", "BRACELETS", "LRING", "RING"]
    for key in expectedGearSpaceKeys:
        if not (key in GearSpace.keys()) or len(GearSpace[key]) == 0: raise InvalidGearSpace(key)
    
    if len(MateriaSpace) < 3 : raise InvalidMateriaSpace

    if len(FoodSpace) == 0 : raise InvalidFoodSpace


                             # Computes the PreBakedAction and asks the fight object to remember those actions for the player with the given ID.
                             # The simulated player will be given base stats.
    Fight.PlayerList[PlayerIndex].Stat = getBaseStat()
    Fight.SavePreBakedAction = True
    Fight.PlayerIDSavePreBakedAction = PlayerIndex
    Fight.SimulateFight(0.01, 500, False, n=0,PPSGraph=False)

    IsTank = Fight.PlayerList[PlayerIndex] == RoleEnum.Tank
    IsCaster = Fight.PlayerList[PlayerIndex].RoleEnum == RoleEnum.Caster or Fight.PlayerList[PlayerIndex].RoleEnum == RoleEnum.Healer
    JobMod = Fight.PlayerList[PlayerIndex].JobMod # Level 90 jobmod value, specific to each job

    newGearSet = GearSet()
    optimalGearSet = GearSet()
    optimalRandomGearSet = {key : [0,GearSet()] for key in PercentileToOpt}
    optimalRandomGearSetMateria = {key : [0,GearSet(),{}] for key in PercentileToOpt}

                            # Removing exp from optimalRandom.
    if "exp" in optimalRandomGearSet.keys(): 
        optimalRandomGearSet.pop("exp")
        optimalRandomGearSetMateria.pop("exp")

    curOptimalDPS = 0
    i = 0
                             # Need at least one of each gear piece.
    for Weapon in GearSpace["WEAPON"]:
        newGearSet.AddGear(Weapon)
        for Head in GearSpace["HEAD"]:
            newGearSet.AddGear(Head)
            for Body in GearSpace["BODY"]:
                newGearSet.AddGear(Body)
                for Hands in GearSpace["HANDS"]:
                    newGearSet.AddGear(Hands)
                    for Legs in GearSpace["LEGS"]:
                        newGearSet.AddGear(Legs)
                        for Feet in GearSpace["FEET"]:
                            newGearSet.AddGear(Feet)
                            for Earrings in GearSpace["EARRINGS"]:
                                newGearSet.AddGear(Earrings)
                                for Necklace in GearSpace["NECKLACE"]:
                                    newGearSet.AddGear(Necklace)
                                    for Bracelets in GearSpace["BRACELETS"]:
                                        newGearSet.AddGear(Bracelets)
                                        for LRing in GearSpace["LRING"]:
                                            newGearSet.AddGear(LRing)
                                            for Ring in GearSpace["RING"]:
                                                print(i)
                                                i+=1
                                                newGearSet.AddGear(Ring)

                                                GearStat = newGearSet.GetGearSetStat()

                                                if not (GearStat["SS"] > maxSPDValue or GearStat["SkS"] > maxSPDValue):
                                                    JobMod = Fight.PlayerList[PlayerIndex].JobMod # Level 90 jobmod value, specific to each job

                                                    f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
                                                    ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, n=randomIteration)

                                                    if curOptimalDPS <= ExpectedDamage:
                                                        optimalGearSet = deepcopy(newGearSet)
                                                        curOptimalDPS = ExpectedDamage

                                                    for percentile in optimalRandomGearSet:
                                                        if optimalRandomGearSet[percentile][0] == 0 or optimalRandomGearSet[percentile][0][percentile] <= randomDamageDict[percentile]:
                                                            optimalRandomGearSet[percentile][1] = deepcopy(newGearSet)
                                                            optimalRandomGearSet[percentile][0] = randomDamageDict

                             # Will now find optimal Meld for the optimal sets that were found.
    matGen = MateriaGenerator(oddMateriaValue, evenMateriaValue)
                             # First optimizes expected BiS
    print("Optimizing Best Expected BiS materia")
    depth = materiaDepthSearchIterator 
    limit = optimalGearSet.getMateriaLimit()  # Number of materia the gearset can support
    if materiaDepthSearchIterator > limit: raise InvalidFunctionParameter("BisSolver", "materiaDepthSearchIterator", "Must be lower than the limit of the gear set")

    counter = 0              # Materia counter
    curMax = 0               # cur Max DPS
    curRandom = {}           # DPS percentiles of current best
    
    while True:
        if not "exp" in PercentileToOpt: break
        print("Progress : " + str(counter)+"/"+str(limit))
        if counter + materiaDepthSearchIterator > limit:
            d = limit - counter
        else:
            d = materiaDepthSearchIterator
        curBest, curMax, curRandom = materiaBisSolver(optimalGearSet, matGen, MateriaSpace, d, Fight, Fight.PlayerList[PlayerIndex].JobMod, IsTank, IsCaster, PlayerIndex, "exp",randomIteration,maxSPDValue=maxSPDValue)
                             # Taking a copy of the found best and incrementing materia counter
        optimalGearSet = deepcopy(curBest)
        counter += materiaDepthSearchIterator
        if counter >= limit : break
        

                             # Will now optimize the random BiS. Every percentile's gearset is optimized by using
                             # the value of the DPS as their percentile. So the 90th percentile BiS is chosen using the
                             # materia arrangement that maximizes the 90th percentile DPS.
    for percentile in optimalRandomGearSet:
        if percentile in PercentileToOpt:
            print("Optimizing " + percentile + "th percentile BiS")
            limit = optimalRandomGearSet[percentile][1].getMateriaLimit()
            curBest = optimalRandomGearSet[percentile][1]
            counter = 0
            while True:
                print("Progress : " + str(counter)+"/"+str(limit))
                if counter + depth > limit:
                    d = limit - counter
                else:
                    d = depth
                curBest, curMax, curRandom = materiaBisSolverV2(curBest, matGen, MateriaSpace, Fight, Fight.PlayerList[PlayerIndex].JobMod, IsTank, IsCaster, PlayerIndex,percentile,randomIteration, maxSPDValue=maxSPDValue)
                counter += depth
                break
                if counter >= limit : break
            optimalRandomGearSetMateria[percentile][0] = curMax
            optimalRandomGearSetMateria[percentile][1] = deepcopy(curBest)
            optimalRandomGearSetMateria[percentile][2] = deepcopy(curRandom)

                             # Optimizing food
    text = "Solver result\n"
    print("Optimizing Food")
    curMax = 0
    curBestExpectedFood = None
    for food in FoodSpace:
        if not "exp" in PercentileToOpt: break
        testSet = deepcopy(optimalGearSet)
        testSet.addFood(food)
        GearStat = testSet.GetGearSetStat()
        if not (GearStat["SS"] > maxSPDValue or GearStat["SkS"] > maxSPDValue):
            f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
            ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH,n=randomIteration)

            if curMax < ExpectedDamage:
                curBestExpectedFood = deepcopy(food)
                curMax = ExpectedDamage
    if "exp" in PercentileToOpt:
        optimalGearSet.addFood(curBestExpectedFood)
        text += "Best optimal : "
        text += (str(optimalGearSet) + "\n")
        text += ("Expected Damage : " + str(curMax) + "\n")
        text += ("Random Damage : " + str(curRandom) + "\n")
        text += str(computeDamageValue(optimalGearSet.GetGearSetStat(), JobMod, IsTank, IsCaster))

    for percentile in optimalRandomGearSetMateria:
        bestFood = None
        for food in FoodSpace:
            if not(percentile in PercentileToOpt): break
            testSet = deepcopy(optimalRandomGearSetMateria[percentile][1])
            testSet.addFood(food)
            GearStat = testSet.GetGearSetStat()
            if not (GearStat["SS"] > maxSPDValue or GearStat["SkS"] > maxSPDValue):
                JobMod = Fight.PlayerList[PlayerIndex].JobMod # Level 90 jobmod value, specific to each job
                f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
                ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH,n=randomIteration)
                if optimalRandomGearSetMateria[percentile][2][percentile] < randomDamageDict[percentile]:
                    optimalRandomGearSetMateria[percentile][0] = ExpectedDamage
                    bestFood = food
                    optimalRandomGearSetMateria[percentile][2] = randomDamageDict
        optimalRandomGearSetMateria[percentile][1].addFood(bestFood)

    for percentile in optimalRandomGearSetMateria:
        text += (percentile + "th percentile gear :"+ "\n")
        text += (str(optimalRandomGearSetMateria[percentile][1])+ "\n")
        text += ("Expected Damage : " + str(optimalRandomGearSetMateria[percentile][0]) + "\n")
        text += ("Random Damage : " + str(optimalRandomGearSetMateria[percentile][2]) + "\n")
        text += str(computeDamageValue(optimalRandomGearSetMateria[percentile][1].GetGearSetStat(), JobMod, IsTank, IsCaster))
        text += ("========================\n")

                             # Will find appropriate name for the file so it doesn't overwrite another existing file
    filenameSkeleton = 'bisSolver' + JobEnum.name_for_id(Fight.PlayerList[PlayerIndex].JobEnum) + "Result"
    testFileName = filenameSkeleton
    counter = 1
    while os.path.isfile(testFileName + ".txt"):
        testFileName = filenameSkeleton + "(" + str(counter) + ")"
        counter += 1
    with open(testFileName + ".txt", 'w') as f:
        f.write(text)

    return optimalGearSet, optimalRandomGearSetMateria
   

def materiaBisSolver(Set : GearSet, matGen : MateriaGenerator, matSpace : list[int], maxDepth : int, Fight, JobMod : int, IsTank : bool, IsCaster : bool,PlayerIndex : int, percentile : str, randomIteration : int,maxSPDValue : int = 5000):
    """
    This functions solves the materia BiS for a given gearset.
    trialSet : GearSet -> GearSet for which to optimize Materias
    matGen : MateriaGenerator -> Materia Generator object
    matSpace : list -> list of all the stats the materia solver will use for melds.
    maxDepth : int -> Up to what depth to search
    Fight : Fight -> Fight instance
    JobMod : int -> JobMod of the player
    IsTank : bool -> If is a tank
    percentile : str -> percentile of the optimization. exp is expected
    maxSPDValue : int -> max Spell Speed or Skill Speed value. Any gear set with higher than that value will be discarded.
    """
    GearSetDict = {
        "99" : [0,GearSet()],
        "90" : [0,GearSet()],
        "75" : [0,GearSet()],
        "50" : [0,GearSet()],
        "exp" : [0,GearSet()]
    }
    curOptimalDPS = 0

    result = []
    matRange = len(matSpace)

    def solver(curDepth, matList, curOptimalDPS):
        for i in range(matRange):
            if curDepth > 1 :
                             # Going recursively until at the max depth
                solver(curDepth - 1, matList, curOptimalDPS)
            else:
                             # Will try to put all the materias in the matList onto the gear pieces.
                trialSet = deepcopy(Set)
                goNext = False
                for matType in matList:
                    newMateria = matGen.GenerateMateria(matSpace[matType])
                
                             # Will find the first piece of gear on which the materia can go
                    key = trialSet.findFirstPieceMateria(newMateria)
                             # If none we ignore this gear set. for now
                    if key == None:
                        goNext = True
                    else:
                        trialSet.GearSet[key].AddMateria(newMateria)
                if not goNext: 
                    GearStat = trialSet.GetGearSetStat()
                    if not (GearStat["SS"] > maxSPDValue or GearStat["SkS"] > maxSPDValue):
                        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
                        ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH,n=randomIteration)

                        result.append([ExpectedDamage, deepcopy(trialSet), randomDamageDict])
            matList[curDepth - 1] += 1
        matList[curDepth - 1] = 0

    matList = [0 for i in range(maxDepth)]
                             # solver will find all possible arrangements of materias of the given matSpace and try all of them.
    solver(maxDepth, matList, curOptimalDPS)
                             # result now has all the result. So we take the max of each percentile.
                             # The metric used here the dps corresponding to the percentile or expected.
    curMaxDPS = 0
    curExpected = 0
    curBestSet = None
    curBestRandom = {}
    if percentile == "exp":
        for gSet in result:
            if gSet[0] > curMaxDPS:
                curMaxDPS = gSet[0]
                curExpected = curMaxDPS
                curBestSet = gSet[1]
                curBestRandom = gSet[2]
    else:
        for gSet in result:
            if gSet[2][percentile] > curMaxDPS:
                curMaxDPS = gSet[2][percentile]
                curExpected = gSet[0]
                curBestSet = gSet[1]
                curBestRandom = gSet[2]

    return curBestSet, curExpected, curBestRandom
    
def materiaBisSolverV2(Set : GearSet, matGen : MateriaGenerator, matSpace : list[int], Fight, JobMod : int, IsTank : bool, IsCaster : bool,PlayerIndex : int, percentile : str, randomIteration : int, maxSPDValue : int = 5000):
    """
    This function serves same purpose as materiaBisSolver(), but instead of going deeper into the materia serach space iteratively,
    we start at the bottom with a theoretical max meld. So every gear piece will have every materia that they can have with no limit.
    They are only limited by the maxStat. We will then remove materias from gear piece until the melding is legal.
    """

    optimalSet = deepcopy(Set)
    optimalPercentileDPS = 0
    optimalExpectedDPS = 0
                             # This first loop will forceAddMateria to the whole set until no more can be
    for gear in optimalSet:
        for type in matSpace:
            for i in range(gear.getNumberPossibleMateria(type, matGen)) : gear.forceAddMateria(matGen.GenerateMateria(type))

    GearStat = optimalSet.GetGearSetStat()
    f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
    ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH,n=randomIteration)

    optimalExpectedDPS = ExpectedDamage
    optimalPercentileDPS = randomDamageDict[percentile]
    
    for key in optimalSet.GearSet.keys():
        while not optimalSet.GearSet[key].hasValidMelding():
            curMinDPS = optimalPercentileDPS
            curTypeToRemove = None
            
            for type in matSpace:
                testSet = deepcopy(optimalSet)

                testSet.removeMateriaSpecGear(key, type)

                GearStat = testSet.GetGearSetStat()
                f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
                ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH,n=randomIteration)

                if randomDamageDict[percentile] < curMinDPS:
                    curMinDPS = randomDamageDict[percentile]
                    curTypeToRemove = type

            optimalSet.removeMateriaSpecGear(key,curTypeToRemove)

    GearStat = optimalSet.GetGearSetStat()

    f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
    ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH,n=randomIteration)
    
    #input("SOLVER 2.0 TEST")

    #print(optimalSet)
    #print(ExpectedDamage)
    #print(randomDamageDict)
    #input()
    return optimalSet, ExpectedDamage, randomDamageDict

        
            




        




    




    



