"""
This file contains the logic of the Gear Solver.

The algorithm requires one Fight Object that will be used to compute the DPS. The algorithm will use
the pre-baked simulation in order to quickly simulate the DPS given some gear configuration.
One list of Gear from which to search, the space of materias that are available, etc.

For now the BiS Solver will only work if the Fight has one player variable, meaning it can only solve the BiS for one 

"""

from ffxivcalc.GearSolver.Gear import GearSet, MateriaGenerator, StatType
from ffxivcalc.Jobs.PlayerEnum import RoleEnum
from math import floor
from copy import deepcopy


def computeDamageValue(GearStat : dict, JobMod : int, IsTank : bool, IsCaster : bool):
    """
    this function computes all the damage values given a stat dict.
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



def BiSSolver(Fight, GearSpace : dict, PlayerIndex : int, n : int = 10000, materiaDepthSearchIterator : int = 7):
    """
    Finds the BiS of the player given a Gear search space and a Fight.
    Fight -> Fight object.
    GearSpace : dict -> Dictionnary filled with the different gear pieces the algorithm can search through.
    PlayerIndex : int -> Index of the player for which the user wants to optimize the gearset. Must be the index of the player
                         in the Fight.PlayerList.
    n : int -> Number of tries the solver has.
    materiaDepthSearchIterator : int -> Depth for which the Materia optimization searches into per step.
    """
                             # Computes the PreBakedAction
    Fight.SavePreBakedAction = True
    Fight.PlayerIDSavePreBakedAction = 0
    Fight.SimulateFight(0.01, 500, False, n=0,PPSGraph=False)
    IsTank = Fight.PlayerList[PlayerIndex] == RoleEnum.Tank
    IsCaster = Fight.PlayerList[PlayerIndex].RoleEnum == RoleEnum.Caster or Fight.PlayerList[PlayerIndex].RoleEnum == RoleEnum.Healer

    newGearSet = GearSet()
    optimalGearSet = GearSet()
    optimalRandomGearSet = {
        "99" : [0,GearSet()],
        "90" : [0,GearSet()],
        "75" : [0,GearSet()],
        "50" : [0,GearSet()],
    }
    curOptimalDPS = 0

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

                                                GearStat = newGearSet.GetGearSetStat()
                                                JobMod = Fight.PlayerList[PlayerIndex].JobMod # Level 90 jobmod value, specific to each job

                                                f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
                                                ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH)

                                                if curOptimalDPS <= ExpectedDamage:
                                                    optimalGearSet = deepcopy(newGearSet)
                                                    curOptimalDPS = ExpectedDamage

                                                for percentile in optimalRandomGearSet:
                                                    if optimalRandomGearSet[percentile][0] == 0 or optimalRandomGearSet[percentile][0][percentile] <= randomDamageDict[percentile]:
                                                        optimalRandomGearSet[percentile][1] = deepcopy(newGearSet)
                                                        optimalRandomGearSet[percentile][0] = randomDamageDict

                             # Will now find optimal Meld for the optimal sets that were found.
    matGen = MateriaGenerator(16, 32)
    print(optimalGearSet)
                             # First optimizes expected BiS
    depth = 4
    limit = optimalGearSet.getMateriaLimit()
    counter = 0
    while True:
        if counter + depth > limit:
            d = limit - counter
        else:
            d = depth
        curBest = materiaBisSolver(optimalGearSet, matGen, 4, d, Fight, Fight.PlayerList[PlayerIndex].JobMod, IsTank, IsCaster, PlayerIndex)
        optimalGearSet = deepcopy(curBest)
        counter += depth
        if counter > limit : break


    print(optimalGearSet)
    text = ""
    text += (str(optimalGearSet) + "\n")
    text += (str(curOptimalDPS) + "\n")
    for percentile in curBest:
        if percentile == "exp":
            pass
        else:
            text += (percentile + "th percentile gear :"+ "\n")
            text += (str(curBest[percentile][1])+ "\n")
            text += ("Damage is : " + str(curBest[percentile][0]) + "\n")
            text += ("========================\n")

    with open('bisSolverResult.txt', 'w') as f:
        f.write(text)
   

def materiaBisSolver(Set : GearSet, matGen : MateriaGenerator, matRange : int, maxDepth : int, Fight, JobMod : int, IsTank : bool, IsCaster : bool,PlayerIndex : int):
    """
    This functions solves the materia BiS for a given gearset.
    trialSet : GearSet -> GearSet for which to optimize Materias
    matGen : MateriaGenerator -> Materia Generator object
    matRange : int -> Since Stats are enum from 0-7, we can say we want the materias to be within what range (6/7 non valid and 5 is TEN).
    maxDepth : int -> Up to what depth to search
    Fight : Fight -> Fight instance
    JobMod : int -> JobMod of the player
    IsTank : bool -> If is a tank
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

    def solver(curDepth, matList, curOptimalDPS):
        for i in range(matRange):
            if curDepth > 1 :
                solver(curDepth - 1, matList, curOptimalDPS)
            else:
                             # Will try to put all the materias in the matList onto the gear pieces.
                trialSet = deepcopy(Set)
                goNext = False
                for matType in matList:
                    newMateria = matGen.GenerateMateria(matType)
                
                             # Will find the first piece of gear on which the materia can go
                    key = trialSet.findFirstPieceMateria(newMateria)
                             # If none we ignore this gear set. for now
                    if key == None:
                        goNext = True
                    else:
                        trialSet.GearSet[key].AddMateria(newMateria)
                if not goNext: 
                    GearStat = trialSet.GetGearSetStat()
                    f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH = computeDamageValue(GearStat, JobMod, IsTank, IsCaster)
                    ExpectedDamage, randomDamageDict = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH)

                    result.append([ExpectedDamage, deepcopy(trialSet)])

                    if curOptimalDPS <= ExpectedDamage:
                        GearSetDict["exp"][1] = deepcopy(trialSet)
                        GearSetDict["exp"][0] = ExpectedDamage
                        curOptimalDPS = ExpectedDamage


                    for percentile in GearSetDict:
                        if percentile == "exp" : pass
                        elif GearSetDict[percentile][0] == 0 or GearSetDict[percentile][0][percentile] <= randomDamageDict[percentile]:
                            GearSetDict[percentile][1] = deepcopy(trialSet)
                            GearSetDict[percentile][0] = randomDamageDict

            matList[curDepth - 1] += 1
        matList[curDepth - 1] = 0

    matList = [0 for i in range(maxDepth)]

    solver(maxDepth, matList, curOptimalDPS)
    #print(GearSetDict["exp"][1])
    #print(GearSetDict["exp"][0])
    curMax = 0
    curBestSet = None
    for set in result:
        if curMax < set[0]:
            curMax = set[0]
            curBestSet = set[1]
    print(curBestSet)
    print(curMax)
    #print(result)
    return curBestSet
    
    

    



