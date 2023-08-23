"""
This file contains the logic of the Gear Solver.

The algorithm requires one Fight Object that will be used to compute the DPS. The algorithm will use
the pre-baked simulation in order to quickly simulate the DPS given some gear configuration.
One list of Gear from which to search, the space of materias that are available, etc.

For now the BiS Solver will only work if the Fight has one player variable, meaning it can only solve the BiS for one 

"""

from ffxivcalc.GearSolver.Gear import GearSet, MateriaGenerator, GearType, StatType
from ffxivcalc.Jobs.PlayerEnum import RoleEnum, JobEnum
from ffxivcalc.helperCode.Progress import ProgressBar
from ffxivcalc.helperCode.exceptions import InvalidFoodSpace, InvalidGearSpace, InvalidMateriaSpace, InvalidFunctionParameter
from math import floor
from copy import deepcopy
import os
import logging
main_logging = logging.getLogger("ffxivcalc")
solver_logging = main_logging.getChild("Solver")


def getBaseStat(IsTank=False):
    """
    This function returns a base stat dictionnary
    """

    return {
        "MainStat" : 450 if not IsTank else 390,
        "WD" : 0,
        "Det" : 390,
        "Ten" : 400,
        "SS" : 400,
        "SkS" : 400,
        "Crit" : 400,
        "DH" : 400,
        "Piety" : 400
    }  

def getGearDPSValue(Fight, gearSet : GearSet, PlayerIndex : int, n : int =10000):
    """
    This function returns the expected damage of a gear set given a fight
    Fight -> Fight object
    gearSet : GearSet -> Gear set to be tested
    PlayerIndex : int -> index of the player to test the gear set on
    n : int -> Number of times to run random simulations.
    """
                             # Computes the PreBakedAction and asks the fight object to remember those actions for the player with the given ID.
                             # The simulated player will be given base stats.
    player = Fight.PlayerList[PlayerIndex]
    IsTank = player.RoleEnum == RoleEnum.Tank 
    IsCaster = player.RoleEnum == RoleEnum.Caster or player.RoleEnum == RoleEnum.Healer
    JobMod = player.JobMod # Level 90 jobmod value, specific to each job

    player.Stat = getBaseStat(IsTank=IsTank)
    Fight.SavePreBakedAction = True
    Fight.PlayerIDSavePreBakedAction = PlayerIndex
    Fight.SimulateFight(0.01, 500, False, n=0,PPSGraph=False)

    GearStat = gearSet.GetGearSetStat(IsTank=IsTank)

    f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
    ExpectedDamage, randomDamageDict, duration, potency = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=n,getInfo = True)

    print(gearSet)
    print("Expected : " + str(ExpectedDamage))
    print("Random : " + str(randomDamageDict))
    print("Duration : " + str(duration))
    print("Potency : " + str(potency))
    print("f_WD : " + str(f_WD) + " f_DET : " + str(f_DET) + " f_TEN : " + str(f_TEN) + " f_SPD : " + str(f_SPD) + " f_CritRate : " + str(f_CritRate) + " f_CritMult : " + str(f_CritMult) + " f_DH : " + str(f_DH))

    return ExpectedDamage, randomDamageDict


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
    DHAuto = floor(140*(GearStat["DH"]-baseMain)/levelMod)/1000 # DH bonus when auto crit/DH
    return f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto

def BiSSolver(Fight, GearSpace : dict, MateriaSpace : list, FoodSpace : list, PercentileToOpt : list = ["exp", "99", "90", "75", "50"],
              materiaDepthSearchIterator : int = 1, randomIteration : int = 10000, oddMateriaValue : int = 18, evenMateriaValue : int = 36,
              PlayerIndex : int = 0, mendSpellSpeed : bool = False, maxSPDValue : int = 5000, minSPDValue : int = 0, useNewAlgo : bool = False, oversaturationIterationsPreGear : int = 0,
              oversaturationIterationsPostGear : int = 0, findOptMateriaGearBF : bool = False):
    """
    Finds the BiS of the player given a Gear search space and a Fight. The Solver will output to a file named
    bisSolver[Job]Result[number].txt with all the relevant information and returns the gearSets. The solver outputs the best Expected Damage GearSet as well as
    the best GearSet for the 50th, 75th, 90th and 99th DPS. The solver requires at least one piece of every possible slots.
    Note that is is possible to give a "prebaked" BiS by only giving 1 choice for some pieces and that it is also possible to
    add materias to the pieces in the GearSpace before running the solver. 
    Note that since the percentile's BiS are using random damage this is only an approximation and might miss the actual best in slot. So it 
    is recommended to run this solver multiple times or with very high value of randomIteration. 

    It is also recommend to have useNewAlgo set to true in order to use the faster and more efficient algorithm.
    If you are solving for the Expected Damage BiS it is also recommend to have findOptMateriaGearBF set to True in order to try
    every possible gear set as otherwise the best meld is only found once a gear set is found.

    Fight -> Fight object.
    GearSpace : dict -> Dictionnary filled with the different gear pieces the algorithm can search through. Must have at least one of each gear types
    Materiaspace : list -> List of all the stats the solver will look through when optimizing melds. Must be at least 3 materias
    FoodSpace : list -> List of all food to look into. Must be non-empty
    PercentileToOpt : list -> List of all gearset to optimize. Exp means to optimize expected damage.
    materiaDepthSearchIterator : int -> Depth for which the Materia optimization searches into per step.
    randomIteration : int -> Number of times the solver will simulate random runs. Must be at least 100
    oddMateriaValue : int -> Stat gained from odd Materia
    evenMateriaValue : int -> Stat gained from even Materia
    PlayerIndex : int -> Index of the player for which the user wants to optimize the gearset. Must be the index of the player in the Fight.PlayerList.
    mendSpellSpeed : bool -> If True the solver will look at Spell Speed value for speed.
    maxSPDValue : int -> Max Spell Speed or skill Speed value. Every gear set above that value will be discarded.
    minSPDValue : int -> Min Spell Speed or skill Speed value. Every gear set under that value will be discarded.
    useNewAlgo : bool -> If set to true will use V2 of materiaBiSSolver
    oversaturationIterationsPreGear : int -> Number of times the algorithm will oversaturate gear before looking for best gear set
    oversaturationIterationsPostGear : int -> Number of times the algorithm will oversaturate gear before looking for best materias
    findOptMateriaGearBF : bool -> If true solver will find best gearset/food/melding using given algorithm. Only recommended for Expected.
    """

                             # Checking the validity of the given search space and some other parameters.
    if materiaDepthSearchIterator <= 0: raise InvalidFunctionParameter("BisSolver", "materiaDepthSearchIterator", "Must be higher than 1.")
    if randomIteration < 100 : raise InvalidFunctionParameter("BisSolver", "randomIteration", "Must be higher than or 100")
    if PlayerIndex < 0 or PlayerIndex > len(Fight.PlayerList) - 1: raise InvalidFunctionParameter("BisSolver", "PlayerIndex", "Invalid index value")
    if useNewAlgo and oversaturationIterationsPreGear + oversaturationIterationsPostGear < 1: raise InvalidFunctionParameter("BiSSolver", "OverSaturationIteration", "If using newAlgo, must oversaturate gearset at least once. (oversaturationIterationsPreGear + oversaturationIterationsPostGear >= 1)")
    if useNewAlgo and (StatType.SS in MateriaSpace or StatType.SkS in MateriaSpace) : raise InvalidFunctionParameter("BiSSolver", "MateriaSpace", "MateriaSpace cannot invclue Speed Materias while using V2")
    if findOptMateriaGearBF and PercentileToOpt != ["exp"] : raise InvalidFunctionParameter("BiSSolver", "PercentileToOpt", "Can only optimize Expected if findOptMateriaGearBF is True")
    if minSPDValue > maxSPDValue : raise InvalidFunctionParameter("BiSSolver", "Limitations to Speed Values", "minSPDValue cannot be bigger than maxSPDValue")
    expectedGearSpaceKeys = ["WEAPON", "HEAD", "BODY", "HANDS", "LEGS", "FEET", "EARRINGS", "NECKLACE", "BRACELETS", "LRING", "RING"]
    for key in expectedGearSpaceKeys:
        if not (key in GearSpace.keys()) or len(GearSpace[key]) == 0: raise InvalidGearSpace(key)
    if len(MateriaSpace) < 3 : raise InvalidMateriaSpace
    if len(FoodSpace) == 0 : raise InvalidFoodSpace

                             # Computes the PreBakedAction and asks the fight object to remember those actions for the player with the given ID.
                             # The simulated player will be given base stats.

    IsTank = Fight.PlayerList[PlayerIndex].RoleEnum == RoleEnum.Tank
    IsCaster = Fight.PlayerList[PlayerIndex].RoleEnum == RoleEnum.Caster or Fight.PlayerList[PlayerIndex].RoleEnum == RoleEnum.Healer
    JobMod = Fight.PlayerList[PlayerIndex].JobMod # Level 90 jobmod value, specific to each job

    Fight.PlayerList[PlayerIndex].Stat = getBaseStat(IsTank=IsTank)
    Fight.SavePreBakedAction = True
    Fight.PlayerIDSavePreBakedAction = PlayerIndex
    Fight.SimulateFight(0.01, 500, False, n=0,PPSGraph=False)

    matGen = MateriaGenerator(oddMateriaValue, evenMateriaValue)
    newGearSet = GearSet()
    optimalGearSet = GearSet()
    optimalRandomGearSet = {key : [0,GearSet()] for key in PercentileToOpt}
    optimalRandomGearSetMateria = {key : [0,GearSet(),{}] for key in PercentileToOpt}

                            # Removing exp from optimalRandom.
    if "exp" in optimalRandomGearSet.keys(): 
        optimalRandomGearSet.pop("exp")
        optimalRandomGearSetMateria.pop("exp")

    for key in GearSpace.keys():
        for gear in GearSpace[key]:
            for type in MateriaSpace:
                for j in range(oversaturationIterationsPreGear):
                    if type != 3: 
                        for i in range(gear.getNumberPossibleMateria(type, matGen)) : gear.forceAddMateria(matGen.GenerateMateria(type))
                    
    curOptimalDPS = 0
                             # Finding total number of possibilities for ProgressBar
    total = 1
    for key in GearSpace:
        total *= len(GearSpace[key])

    gearBFpB = ProgressBar.init(total, "Finding Best Gear Set")
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
                                                newGearSet.AddGear(Ring)

                                                curBestFoodExpectedDPS = 0
                                                curBestFoodExpectedSet = None
                                                curBestFoodRandomDPS = {key : [0,None,{}] for key in optimalRandomGearSetMateria}


                                                                        # Adding here so I don't forget. SpS/SkS are not usually as high as the other
                                                                        # stats here because we do not oversaturate with Speed melds. THis could
                                                                        # affect the buff given by food. Should add an option to add all the SpS/SkS bonus
                                                                        # from food to see if this affects the final results.
                                                for food in FoodSpace:
                                                    trialSet = deepcopy(newGearSet)
                                                    trialSet.addFood(food)
                                                    GearStat = trialSet.GetGearSetStat(IsTank=IsTank)
                                                                         # Will test for SpS/SkS to see if it can fall within the accepted minSPDValue.
                                                                         # Checking if 0 before so we can speedup if it will work for sure.

                                                    gearSetMaxSPDValue = ((GearStat["SS"] if mendSpellSpeed else GearStat["SkS"]) + trialSet.getMateriaTypeLimit((StatType.SS if mendSpellSpeed else StatType.SkS), matGen) * matGen.EvenValue)
                                                    gearSetMaxSPDValueFood = min(int(gearSetMaxSPDValue * 0.1) + gearSetMaxSPDValue, gearSetMaxSPDValue + 103)
                                                    canReachMinSPD = (minSPDValue == 0) or gearSetMaxSPDValueFood >= minSPDValue

                                                    if not canReachMinSPD:
                                                        continue
                                                                         # Will find optimal meld with food
                                                    if findOptMateriaGearBF: 
                                                        trialSet, exp, ra = materiaBisSolverV3(trialSet, matGen, MateriaSpace, Fight, Fight.PlayerList[PlayerIndex].JobMod, IsTank, IsCaster, PlayerIndex, "exp",0,mendSpellSpeed,minSPDValue=minSPDValue,maxSPDValue=maxSPDValue,oversaturationIterationsPostGear=oversaturationIterationsPostGear,findOptMateriaGearBF=findOptMateriaGearBF)

                                                    GearStat = trialSet.GetGearSetStat(IsTank=IsTank)

                                                    if not ((mendSpellSpeed and GearStat["SS"] > maxSPDValue) or (not mendSpellSpeed and GearStat["SkS"] > maxSPDValue)):

                                                        JobMod = Fight.PlayerList[PlayerIndex].JobMod # Level 90 jobmod value, specific to each job
                                
                                                        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
                                                        ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=randomIteration)

                                                        if curBestFoodExpectedDPS <= ExpectedDamage:
                                                            curBestFoodExpectedSet = deepcopy(trialSet)
                                                            curBestFoodExpectedDPS = ExpectedDamage

                                                        for percentile in curBestFoodRandomDPS:
                                                            if curBestFoodRandomDPS[percentile][0] <= randomDamageDict[percentile]:
                                                                curBestFoodRandomDPS[percentile][0] = randomDamageDict[percentile]
                                                                curBestFoodRandomDPS[percentile][1] = deepcopy(trialSet)
                                                                curBestFoodRandomDPS[percentile][2] = deepcopy(randomDamageDict)

                                                if curOptimalDPS < curBestFoodExpectedDPS:
                                                    optimalGearSet = deepcopy(curBestFoodExpectedSet)
                                                    curOptimalDPS = curBestFoodExpectedDPS

                                                for percentile in optimalRandomGearSet:
                                                    if optimalRandomGearSet[percentile][0] <= curBestFoodRandomDPS[percentile][0]:
                                                        optimalRandomGearSet[percentile][0] = curBestFoodRandomDPS[percentile][0]
                                                        optimalRandomGearSet[percentile][1] = deepcopy(curBestFoodRandomDPS[percentile][1])
                                                next(gearBFpB)        

                             # Only do optimal meld if not already found
    if not findOptMateriaGearBF:
        for percentile in PercentileToOpt:
            if percentile == "exp" : 
                solver_logging.warning("Optimal oversaturated gear set : \n" + (str(optimalGearSet)) + "\nDamage : " + str(curOptimalDPS))
            else : solver_logging.warning("Optimal oversaturated gear set : \n" + (str(optimalRandomGearSet[percentile][1])) + "\nDamage : " + str(optimalRandomGearSet[percentile][0]))
                                # Will now find optimal Meld for the optimal sets that were found.
        if useNewAlgo:
            print("Using BF up-down")
            if "exp" in PercentileToOpt : 
                print("Optimizing Best Expected BiS materia")
                optimalGearSet, curMax, curRandom = materiaBisSolverV3(optimalGearSet, matGen, MateriaSpace, Fight, Fight.PlayerList[PlayerIndex].JobMod, IsTank, IsCaster, PlayerIndex, "exp",0,mendSpellSpeed,minSPDValue=minSPDValue,maxSPDValue=maxSPDValue,oversaturationIterationsPostGear=oversaturationIterationsPostGear,findOptMateriaGearBF=findOptMateriaGearBF)
                                    # Will now optimize the random BiS. Every percentile's gearset is optimized by using
                                    # the value of the DPS as their percentile. So the 90th percentile BiS is chosen using the
                                    # materia arrangement that maximizes the 90th percentile DPS.
            for percentile in optimalRandomGearSet:
                if percentile != "exp" : 
                    print("Optimizing " + percentile + "th percentile BiS")
                    optimalRandomGearSetMateria[percentile][1], optimalRandomGearSetMateria[percentile][0], curRandom = materiaBisSolverV3(optimalRandomGearSet[percentile][1], matGen, MateriaSpace, Fight, Fight.PlayerList[PlayerIndex].JobMod, IsTank, IsCaster, PlayerIndex, percentile,randomIteration,mendSpellSpeed,minSPDValue=minSPDValue,maxSPDValue=maxSPDValue, oversaturationIterationsPostGear=oversaturationIterationsPostGear)
                    optimalRandomGearSetMateria[percentile][2] = deepcopy(curRandom)
        else:
            print("Using BF down-up")
            depth = materiaDepthSearchIterator 
            limit = optimalGearSet.getMateriaLimit()  # Number of materia the gearset can support
            if materiaDepthSearchIterator > limit: raise InvalidFunctionParameter("BisSolver", "materiaDepthSearchIterator", "Must be lower than the limit of the gear set")

            counter = 0              # Materia counter
            curMax = 0               # cur Max DPS
            curRandom = {}           # DPS percentiles of current best
            if "exp" in PercentileToOpt : print("Optimizing Best Expected BiS materia")
            while True:
                if not "exp" in PercentileToOpt: break
                print("Progress : " + str(counter)+"/"+str(limit))
                if counter + materiaDepthSearchIterator > limit:
                    d = limit - counter
                else:
                    d = materiaDepthSearchIterator
                curBest, curMax, curRandom = materiaBisSolver(optimalGearSet, matGen, MateriaSpace, d, Fight, Fight.PlayerList[PlayerIndex].JobMod, IsTank, IsCaster, PlayerIndex, "exp",0,mendSpellSpeed,maxSPDValue=maxSPDValue)
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
                        curBest, curMax, curRandom = materiaBisSolver(curBest, matGen, MateriaSpace, d, Fight, Fight.PlayerList[PlayerIndex].JobMod, IsTank, IsCaster, PlayerIndex,percentile,randomIteration,mendSpellSpeed, maxSPDValue=maxSPDValue)
                        counter += depth
                        if counter >= limit : break
                    optimalRandomGearSetMateria[percentile][0] = curMax
                    optimalRandomGearSetMateria[percentile][1] = deepcopy(curBest)
                    optimalRandomGearSetMateria[percentile][2] = deepcopy(curRandom)

            
    text = "Solver result " + ("(Using BF up-down)" if useNewAlgo else "(Using BF down-up)") + "\n"

    GearStat = optimalGearSet.GetGearSetStat(IsTank=IsTank)
    f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
    logging.getLogger("ffxivcalc").setLevel(level=logging.DEBUG)
    curMax, curRandom, duration, potency = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=randomIteration, getInfo=True)
    if "exp" in PercentileToOpt:
        #optimalGearSet.addFood(curBestExpectedFood)
        text += "Best optimal : "
        text += (str(optimalGearSet) + "\n")
        text += ("Expected Damage : " + str(curMax) + "\n")
        text += ("Potency : " + str(potency))
        text += ("TimeStamp : " + str(duration))
        text += ("Random Damage : " + str(curRandom) + "\n")
        text += str(computeDamageValue(optimalGearSet.GetGearSetStat(IsTank=IsTank), JobMod, IsTank, IsCaster))

    for percentile in optimalRandomGearSetMateria:
        GearStat = optimalRandomGearSetMateria[percentile][1].GetGearSetStat(IsTank=IsTank)
        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
        optimalRandomGearSetMateria[percentile][0], optimalRandomGearSetMateria[percentile][2] = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=randomIteration)
        text += (percentile + "th percentile gear :"+ "\n")
        text += (str(optimalRandomGearSetMateria[percentile][1])+ "\n")
        text += ("Expected Damage : " + str(optimalRandomGearSetMateria[percentile][0]) + "\n")
        text += ("Random Damage : " + str(optimalRandomGearSetMateria[percentile][2]) + "\n")
        text += str(computeDamageValue(optimalRandomGearSetMateria[percentile][1].GetGearSetStat(IsTank=IsTank), JobMod, IsTank, IsCaster))
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
   
def materiaBisSolver(Set : GearSet, matGen : MateriaGenerator, matSpace : list[int], maxDepth : int, Fight, JobMod : int, IsTank : bool, IsCaster : bool,PlayerIndex : int, percentile : str, randomIteration : int,mendSpellSpeed : bool,maxSPDValue : int = 5000):
    """

    NOT RECOMMENDED TO USE SINCE SLOW.

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
    pB = ProgressBar.init(len(matSpace)**maxDepth, "Finding best " + str(maxDepth) + " next meld")
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
                    GearStat = trialSet.GetGearSetStat(IsTank=IsTank)
                    if not ((mendSpellSpeed and GearStat["SS"] > maxSPDValue) or (not mendSpellSpeed and GearStat["SkS"] > maxSPDValue)):
                        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
                        ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=randomIteration)

                        result.append([ExpectedDamage, deepcopy(trialSet), randomDamageDict])
                next(pB)
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
    
def materiaBisSolverV2(Set : GearSet, matGen : MateriaGenerator, matSpace : list[int], Fight, JobMod : int, IsTank : bool, IsCaster : bool,PlayerIndex : int, percentile : str, randomIteration : int, mendSpellSpeed : bool,maxSPDValue : int = 5000, oversaturationIterationsPostGear : int = 0,findOptMateriaGearBF = False):
    """
    
    DEPRECATED
    
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
            for j in range(oversaturationIterationsPostGear):
                if type != StatType.SS or type != StatType.SkS: 
                    for i in range(gear.getNumberPossibleMateria(type, matGen)) : gear.forceAddMateria(matGen.GenerateMateria(type))

    while not optimalSet.hasValidMelding():
        for key in optimalSet.GearSet.keys():
            if not optimalSet.GearSet[key].hasValidMelding():
                curMaxDPS = 0
                curTypeToRemove = None
                solver_logging.warning("Working on " + key)
                solver_logging.warning(optimalSet.GetGearSetStat(IsTank=IsTank))

                for type in matSpace:
                    if optimalSet.GearSet[key].hasStatMeld(type):
                        testSet = deepcopy(optimalSet)
                        testSet.removeMateriaSpecGear(key, type)

                        GearStat = testSet.GetGearSetStat(IsTank=IsTank)
                        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
                        ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=randomIteration)
                        
                        if percentile == "exp" and ExpectedDamage > curMaxDPS:
                            curMaxDPS = ExpectedDamage
                            curTypeToRemove = type
                        elif percentile != "exp" and randomDamageDict[percentile] > curMaxDPS:
                            curMaxDPS = randomDamageDict[percentile]
                            curTypeToRemove = type

                        solver_logging.warning("Trial by removing " + StatType.name_for_id(type) + " dps : " + (str(ExpectedDamage) if percentile == "exp" else str(randomDamageDict[percentile])) + (" Expected : " + str(ExpectedDamage) if percentile != "exp" else ""))

                optimalSet.removeMateriaSpecGear(key,curTypeToRemove)
                solver_logging.warning("Removing " + StatType.name_for_id(curTypeToRemove) + " Damage is now " + str(curMaxDPS))


                             # Will now add SpS/SkS until required amount
    solver_logging.warning("Replacing by SpS/SkS meld until required amount")
    GearStat = optimalSet.GetGearSetStat(IsTank=IsTank)
    curBestSSDPS = 0
    curBestOptimal = None
    while optimalSet.GetGearSetStat(IsTank=IsTank)["SS"] + 36 < maxSPDValue:
                             # Will look for materia to remove that has smallest DPS loss if replaced with SpS/SkS
        materia = matGen.GenerateMateria(3)
        curPieceToEdit = ""
        curBestDPS = 0
        curTypeToReplace = None
        for gear in optimalSet:
            gearName = gear.getGearTypeName()
            if gear.canReplaceMateriaNoLoss(materia):
                solver_logging.warning("Working on " + gearName)
                for mat in gear.Materias:
                    if mat.StatType != 3:
                        trialSet = deepcopy(optimalSet)
                        trialSet.removeMateriaSpecGear(gearName,mat.StatType)

                        trialSet.GearSet[gearName].AddMateria(materia)
                        GearStat = trialSet.GetGearSetStat(IsTank=IsTank)
                        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
                        ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=randomIteration)
                        
                        solver_logging.warning("Trial by replacing " + (StatType.name_for_id(mat.StatType)) + " : " + (str(ExpectedDamage) if percentile == "exp" else str(randomDamageDict[percentile])) + (" Expected : " + str(ExpectedDamage) if percentile != "exp" else ""))
                        
                        if percentile == "exp" and ExpectedDamage > curBestDPS:
                            curBestDPS = ExpectedDamage
                            curPieceToEdit = gearName
                            curTypeToReplace = mat.StatType
                        elif percentile != "exp" and randomDamageDict[percentile] > curBestDPS:
                            curBestDPS = randomDamageDict[percentile]
                            curPieceToEdit = gearName
                            curTypeToReplace = mat.StatType    

                             # Will now replace the found materia with SpS/SkS
        

        if curPieceToEdit == "":
                             # Means none was found that could have meld
            break

        optimalSet.removeMateriaSpecGear(curPieceToEdit, curTypeToReplace)
        optimalSet.GearSet[curPieceToEdit].AddMateria(deepcopy(materia))

        GearStat = optimalSet.GetGearSetStat(IsTank=IsTank)
        f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
        ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=randomIteration)

        solver_logging.warning("Replacing " + StatType.name_for_id(curTypeToReplace) + " from " + curPieceToEdit + " Damage : " + (str(ExpectedDamage) if percentile == "exp" else str(randomDamageDict[percentile])) + (" Expected : " + str(ExpectedDamage) if percentile != "exp" else ""))

        if percentile == "exp" and ExpectedDamage > curBestSSDPS:
            curBestSSDPS = ExpectedDamage
            curBestOptimal = deepcopy(optimalSet)
            solver_logging.warning("Optimal at " + str(GearStat["SS"]))
        elif percentile != "exp" and randomDamageDict[percentile] > curBestSSDPS:
            curBestSSDPS = randomDamageDict[percentile]
            curBestOptimal = deepcopy(optimalSet)
            solver_logging.warning("Optimal at " + str(GearStat["SS"]))

    optimalSet = deepcopy(curBestOptimal) if curBestOptimal != None else optimalSet

    

    f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
    ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=randomIteration)

    return optimalSet, ExpectedDamage, randomDamageDict

def materiaBisSolverV3(Set : GearSet, matGen : MateriaGenerator, matSpace : list[int], Fight, JobMod : int, IsTank : bool, IsCaster : bool,PlayerIndex : int, 
                       percentile : str, randomIteration : int, mendSpellSpeed : bool,minSPDValue : int = 0, maxSPDValue : int = 5000, oversaturationIterationsPostGear : int = 0, findOptMateriaGearBF : bool = False):   
    """
    This function finds the best melds for the given Gear Set.

    The algorithm will first remove materias until the gear set is valid by removing the materias that are deemed
    less contributing. After that SpS/SkS will replace lowest impact materias until Speed values are achieved.

    THIS FUNCTION HAS NOT YET BEEN SHOWED TO BE OPTIMAL, BUT IT IS THE BEST ONE I HAVE FOUND.

    Set : GearSet -> GearSet to optimize
    matGen : MateriaGenerator -> Materia Generator
    matSpace : list[int] -> list of Materias to consider when oversaturating and removing.
    Fight -> Fight to consider
    JobMod : int -> Value of the JobMod of the player the Gear Set is on.
    IsTank : bool -> True if the player is a tank
    IsCaster : bool -> True if the player is a caster
    PlayerIndex : int -> Index of the player in the Fight's PlayerList
    percentile : str -> Percentile to optimize. "exp" is Expected.
    randomIteration : int -> Number of time to run random simulations.
    mendSpellSpeed : bool -> If true the algorithm will add SpS materias and not SkS
    maxSPDValue : int -> Maximum Speed value for the Gear Set with melds.
    minSPDValue : int -> Minimal Speed value for the Gear Set with melds.
    oversaturationIterationsPostGear : int -> Number of times the algorithm will oversaturate the gear set.
    findOptMateriaGearBF : bool -> If true means we are solving materias for every possible gear set/food. So this simply mutes the ProgressBar usually present.
    """
    optimalSet = deepcopy(Set)
                                 # This first loop will forceAddMateria to the whole set until no more can be
    for gear in optimalSet:
        for type in matSpace:
            for j in range(oversaturationIterationsPostGear):
                if type != 3: 
                    for i in range(gear.getNumberPossibleMateria(type, matGen)) : gear.forceAddMateria(matGen.GenerateMateria(type))

                             # Will remove materias until the gearset is valid.
    if not findOptMateriaGearBF : 
        pB = ProgressBar.init(optimalSet.getNumberMateria() - optimalSet.getMateriaLimit(), "Removing oversaturated")

    while not optimalSet.hasValidMelding():

        curMaxDPS = 0
        curTypeToRemove = None
        
        for type in optimalSet.getMateriaTypeList(ignoreValidMeld=True):
                             # Will trial which materia type is the best to remove.
                             # SkS/SpS are not yet on the gear set, so they are ignored.
            trialSet = deepcopy(optimalSet)
            gearName = trialSet.removeFirstFoundMateriaInvalidPiece(type)

            GearStat = trialSet.GetGearSetStat(IsTank=IsTank)

            f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
            ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=randomIteration)
            
            solver_logging.warning("Trial by removing " + StatType.name_for_id(type) + " from " + gearName + " : " + (str(ExpectedDamage) if percentile == "exp" else str(randomDamageDict[percentile])) + (" Expected : " + str(ExpectedDamage) if percentile != "exp" else ""))
            solver_logging.warning("Dict Stat : " + str(GearStat))
            if percentile == "exp" and ExpectedDamage > curMaxDPS:
                curMaxDPS = ExpectedDamage
                curTypeToRemove = type
            elif percentile != "exp" and randomDamageDict[percentile] > curMaxDPS:
                curMaxDPS = randomDamageDict[percentile]
                curTypeToRemove = type

                             # Will now remove the best meld to remove from oversaturated gear piece
        if optimalSet.removeFirstFoundMateriaInvalidPiece(curTypeToRemove) == None:
            solver_logging.error("Trying to remove materia that isn't illegal")
            raise InvalidMateriaSpace
        
        solver_logging.warning("Removing " + StatType.name_for_id(curTypeToRemove))
        if not findOptMateriaGearBF : next(pB)

    #############

    exploringDepth = 22
    curDepth = 0
    solver_logging.warning("Exploring DH/Det replacement in a depth of " + str(exploringDepth))

    trialSetDH = deepcopy(optimalSet)
    trialSetDHCurMaxDPS = 0
    trialSetDet = deepcopy(optimalSet)
    trialSetDetCurMaxDPS = 0

    while True:

        hasChangedMeld = False

        for gear in trialSetDH:
            if gear.hasStatMeld(StatType.Det) and gear.canReplaceMateriaNoLoss(matGen.GenerateMateria(StatType.DH)):
                hasChangedMeld = True
                curDepth += 1
                gear.removeMateriaType(StatType.Det)
                gear.AddMateria(matGen.GenerateMateria(StatType.DH))

                GearStat = trialSetDH.GetGearSetStat(IsTank=IsTank)

                f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
                ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=randomIteration)

                if ExpectedDamage > curMaxDPS and ExpectedDamage > trialSetDHCurMaxDPS :
                    optimalSet = deepcopy(trialSetDH)
                    trialSetDHCurMaxDPS = ExpectedDamage
        
        if not hasChangedMeld : break

    curDepth = 0

    while True:

        hasChangedMeld = False

        for gear in trialSetDet:
            if gear.hasStatMeld(StatType.DH) and gear.canReplaceMateriaNoLoss(matGen.GenerateMateria(StatType.Det)):
                hasChangedMeld = True
                curDepth += 1
                gear.removeMateriaType(StatType.DH)
                gear.AddMateria(matGen.GenerateMateria(StatType.Det))

                GearStat = trialSetDH.GetGearSetStat(IsTank=IsTank)

                f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
                ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=randomIteration)
                
                if ExpectedDamage > curMaxDPS and ExpectedDamage > trialSetDHCurMaxDPS and ExpectedDamage > trialSetDetCurMaxDPS :
                    optimalSet = deepcopy(trialSetDH)
                    trialSetDHCurMaxDPS = ExpectedDamage

        if not hasChangedMeld : break


    ############

    solver_logging.warning("Replacing materias until SpS/SkS values are achieved.")

    optimalSpeedSet = deepcopy(optimalSet)
    curMaxSpeedDPS = curMaxDPS

    GearStat = optimalSet.GetGearSetStat(IsTank=IsTank)
    pBTotal = max(0,int((maxSPDValue - GearStat["SS"])/matGen.EvenValue))

    haveFoundMinSPDSet = GearStat[("SS" if mendSpellSpeed else "SkS")] >= minSPDValue
    
    if not findOptMateriaGearBF : 
        pBTotal = max(1,int((maxSPDValue - GearStat["SS"])/matGen.EvenValue))
        pbReplace = ProgressBar.init(pBTotal, "Replacing by SpS/SkS")

    while (GearStat["SS"] if mendSpellSpeed else GearStat["SkS"]) + matGen.EvenValue < maxSPDValue:
        curMaxDPS = 0
        curTypeToReplace = None
        curGearPieceToReplace = None
        mat = matGen.GenerateMateria(StatType.SS if mendSpellSpeed else StatType.SkS)

        for type in optimalSet.getMateriaTypeList():
            trialSet = deepcopy(optimalSet)
            for gear in trialSet:
                             # Will look for first piece of gear that
                             # can have the desired type replaced by SpS or SkS
                if gear.hasStatMeld(type) and gear.canReplaceMateriaNoLoss(mat):
                    gear.removeMateriaType(type)
                    gear.AddMateria(mat)

                    GearStat = trialSet.GetGearSetStat(IsTank=IsTank)

                    f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
                    ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=randomIteration)

                    solver_logging.warning("Trial be replacing " + StatType.name_for_id(type) + " from " + gear.getGearTypeName() + " : " + (str(ExpectedDamage) if percentile == "exp" else str(randomDamageDict[percentile])) + (" Expected : " + str(ExpectedDamage) if percentile != "exp" else ""))
                    
                    if percentile == "exp" and ExpectedDamage > curMaxDPS:
                        curMaxDPS = ExpectedDamage
                        curTypeToReplace = type
                        curGearPieceToReplace = gear.getGearTypeName()
                    elif percentile != "exp" and randomDamageDict[percentile] > curMaxDPS:
                        curMaxDPS = randomDamageDict[percentile]
                        curTypeToReplace = type
                        curGearPieceToReplace = gear.getGearTypeName()
                    break
        
                             # We will now replace the highest valued DPS materia with SpS or SkS
        if curTypeToReplace == None:
                             # If curTypeToReplace is still none, then no possible materias can be removed so we exit.
            solver_logging.warning("Cannot find any materia to replace")
            break
        
        optimalSet.removeMateriaSpecGear(curGearPieceToReplace, curTypeToReplace)
        optimalSet.GearSet[curGearPieceToReplace].AddMateria(mat)
        GearStat = optimalSet.GetGearSetStat(IsTank=IsTank)
        solver_logging.warning("Replacing " + StatType.name_for_id(curTypeToReplace) + " from " + curGearPieceToReplace + " Speed is now : " + str(GearStat[("SS" if mendSpellSpeed else "SkS")]))
        if not findOptMateriaGearBF : next(pbReplace)

                             # Will now compare with previous best to see if new Speed values are better
                             # Or take the first set has minSPDValue
        if curMaxDPS > curMaxSpeedDPS or ((not haveFoundMinSPDSet) and GearStat[("SS" if mendSpellSpeed else "SkS")] > minSPDValue):
            if not haveFoundMinSPDSet and GearStat[("SS" if mendSpellSpeed else "SkS")] > minSPDValue : 
                haveFoundMinSPDSet = True
                solver_logging.warning("Found minSPDValue set with SPD value : " + str(GearStat[("SS" if mendSpellSpeed else "SkS")]))
            curMaxSpeedDPS = curMaxDPS
            optimalSpeedSet = deepcopy(optimalSet)
            solver_logging.warning("Found new optimal Speed set with damage " + str(curMaxDPS) + " Speed value : " + str(GearStat[("SS" if mendSpellSpeed else "SkS")]))

    optimalSet = deepcopy(optimalSpeedSet)

    return optimalSet, 0, {}

def materiaBisSolverV4(Set : GearSet, matGen : MateriaGenerator, matSpace : list[int], Fight, JobMod : int, IsTank : bool, IsCaster : bool,PlayerIndex : int, percentile : str, randomIteration : int, mendSpellSpeed : bool,maxSPDValue : int = 5000, oversaturationIterationsPostGear : int = 0, findOptMateriaGearBF : bool = False):   
    """
    This function finds the best melds for the given Gear Set.

    The algorithm will first remove materias until the gear set is valid by removing the materias that are deemed
    less contributing. After that SpS/SkS will replace lowest impact materias until Speed values are achieved.

    THIS FUNCTION HAS NOT YET BEEN SHOWED TO BE OPTIMAL, BUT IT IS THE BEST ONE I HAVE FOUND.

    Set : GearSet -> GearSet to optimize
    matGen : MateriaGenerator -> Materia Generator
    matSpace : list[int] -> list of Materias to consider when oversaturating and removing.
    Fight -> Fight to consider
    JobMod : int -> Value of the JobMod of the player the Gear Set is on.
    IsTank : bool -> True if the player is a tank
    IsCaster : bool -> True if the player is a caster
    PlayerIndex : int -> Index of the player in the Fight's PlayerList
    percentile : str -> Percentile to optimize. "exp" is Expected.
    randomIteration : int -> Number of time to run random simulations.
    mendSpellSpeed : bool -> If true the algorithm will add SpS materias and not SkS
    maxSPDValue : int -> Maximum Speed value for the Gear Set with melds.
    oversaturationIterationsPostGear : int -> Number of times the algorithm will oversaturate the gear set.
    findOptMateriaGearBF : bool -> If true means we are solving materias for every possible gear set/food. So this simply mutes the ProgressBar usually present.
    """
    optimalSet = deepcopy(Set)
                                 # This first loop will forceAddMateria to the whole set until no more can be
    for gear in optimalSet:
        for type in matSpace:
            for j in range(oversaturationIterationsPostGear):
                if type != 3: 
                    for i in range(gear.getNumberPossibleMateria(type, matGen)) : gear.forceAddMateria(matGen.GenerateMateria(type))

                             # Will remove materias until the gearset is valid.
    if not findOptMateriaGearBF : 
        pB = ProgressBar.init(optimalSet.getNumberMateria() - optimalSet.getMateriaLimit(), "Removing oversaturated")

    while not optimalSet.hasValidMelding():

        curMaxDPS = 0
        curTypeToRemove = None
        curTypeToRemove2 = None
        
        for type in optimalSet.getMateriaTypeList(ignoreValidMeld=True):
                             # Will trial which materia type is the best to remove.
                             # SkS/SpS are not yet on the gear set, so they are ignored.
            trialSet = deepcopy(optimalSet)
            gearName = trialSet.removeFirstFoundMateriaInvalidPiece(type)

            secondIterated = trialSet.getMateriaTypeList(ignoreValidMeld=True) if trialSet.getNumberMateria() > 22 else [None]

            for secondType in secondIterated:
                trialSetTwo = deepcopy(trialSet)
                gearName = trialSetTwo.removeFirstFoundMateriaInvalidPiece(secondType) if secondType != None else ""

                GearStat = trialSetTwo.GetGearSetStat(IsTank=IsTank)

                f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
                ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=randomIteration)

                solver_logging.warning("Trial by removing " + StatType.name_for_id(type) + " and " + StatType.name_for_id(secondType) + " : " + (str(ExpectedDamage) if percentile == "exp" else str(randomDamageDict[percentile])) + (" Expected : " + str(ExpectedDamage) if percentile != "exp" else ""))
                solver_logging.warning("Dict Stat : " + str(GearStat))
                if percentile == "exp" and ExpectedDamage > curMaxDPS:
                    curMaxDPS = ExpectedDamage
                    curTypeToRemove = type
                    curTypeToRemove2 = secondType
                elif percentile != "exp" and randomDamageDict[percentile] > curMaxDPS:
                    curMaxDPS = randomDamageDict[percentile]
                    curTypeToRemove = type

                             # Will now remove the best meld to remove from oversaturated gear piece
        if optimalSet.removeFirstFoundMateriaInvalidPiece(curTypeToRemove) == None or (curTypeToRemove2 != None and optimalSet.removeFirstFoundMateriaInvalidPiece(curTypeToRemove2) == None):
            solver_logging.error("Trying to remove materia that isn't illegal")
            solver_logging.error(curTypeToRemove)
            solver_logging.error(curTypeToRemove2)
            solver_logging.error(str(optimalSet.getNumberMateria()))
            raise InvalidMateriaSpace
        
        solver_logging.warning("Removing " + StatType.name_for_id(curTypeToRemove) + " and " + (StatType.name_for_id(curTypeToRemove2) if curTypeToRemove2 != None else "None"))
        if not findOptMateriaGearBF : 
            next(pB)
            next(pB)


    solver_logging.warning("Replacing materias until SpS/SkS values are achieved.")

    optimalSpeedSet = deepcopy(optimalSet)
    curMaxSpeedDPS = curMaxDPS

    GearStat = optimalSet.GetGearSetStat(IsTank=IsTank)
    pBTotal = max(0,int((maxSPDValue - GearStat["SS"])/matGen.EvenValue))
    
    if not findOptMateriaGearBF : 
        pBTotal = max(1,int((maxSPDValue - GearStat["SS"])/matGen.EvenValue))
        pbReplace = ProgressBar.init(pBTotal, "Replacing by SpS/SkS")

    while (mendSpellSpeed and GearStat["SS"] + matGen.EvenValue < maxSPDValue) or (not mendSpellSpeed and GearStat["SkS"] + matGen.EvenValue < maxSPDValue):

        curMaxDPS = 0
        curTypeToReplace = None
        curGearPieceToReplace = None
        mat = matGen.GenerateMateria(StatType.SS if mendSpellSpeed else StatType.SkS)

        for type in optimalSet.getMateriaTypeList():
            trialSet = deepcopy(optimalSet)
            for gear in trialSet:
                             # Will look for first piece of gear that
                             # can have the desired type replaced by SpS or SkS
                if gear.hasStatMeld(type) and gear.canReplaceMateriaNoLoss(mat):
                    gear.removeMateriaType(type)
                    gear.AddMateria(mat)

                    GearStat = trialSet.GetGearSetStat(IsTank=IsTank)

                    f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
                    ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH, DHAuto, n=randomIteration)

                    solver_logging.warning("Trial be replacing " + StatType.name_for_id(type) + " from " + gear.getGearTypeName() + " : " + (str(ExpectedDamage) if percentile == "exp" else str(randomDamageDict[percentile])) + (" Expected : " + str(ExpectedDamage) if percentile != "exp" else ""))
                    
                    if percentile == "exp" and ExpectedDamage > curMaxDPS:
                        curMaxDPS = ExpectedDamage
                        curTypeToReplace = type
                        curGearPieceToReplace = gear.getGearTypeName()
                    elif percentile != "exp" and randomDamageDict[percentile] > curMaxDPS:
                        curMaxDPS = randomDamageDict[percentile]
                        curTypeToReplace = type
                        curGearPieceToReplace = gear.getGearTypeName()
                    break
        
                             # We will now replace the highest valued DPS materia with SpS or SkS
        if curTypeToReplace == None:
                             # If curTypeToReplace is still none, then no possible materias can be removed so we exit.
            solver_logging.warning("Cannot find any materia to replace")
            break
        
        optimalSet.removeMateriaSpecGear(curGearPieceToReplace, curTypeToReplace)
        optimalSet.GearSet[curGearPieceToReplace].AddMateria(mat)
        GearStat = optimalSet.GetGearSetStat(IsTank=IsTank)
        solver_logging.warning("Replacing " + StatType.name_for_id(curTypeToReplace) + " from " + curGearPieceToReplace)
        if not findOptMateriaGearBF : next(pbReplace)

                             # Will now compare with previous best to see if new Speed values are better
        if curMaxDPS > curMaxSpeedDPS:
            curMaxSpeedDPS = curMaxDPS
            optimalSpeedSet = deepcopy(optimalSet)
            solver_logging.warning("Found new optimal Speed set with damage " + str(curMaxDPS) + " Speed value : " + str(GearStat["SS"]))

    return optimalSpeedSet, 0, {}
                










        




    




    



