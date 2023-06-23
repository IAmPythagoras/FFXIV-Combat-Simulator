"""
This file contains the logic of the Gear Solver.

The algorithm requires one Fight Object that will be used to compute the DPS. The algorithm will use
the pre-baked simulation in order to quickly simulate the DPS given some gear configuration.
One list of Gear from which to search, the space of materias that are available, etc.

For now the BiS Solver will only work if the Fight has one player variable, meaning it can only solve the BiS for one 

"""

from ffxivcalc.GearSolver.Gear import GearSet
from ffxivcalc.Jobs.PlayerEnum import RoleEnum
from math import floor

def BiSSolver(Fight, GearSpace : dict, PlayerIndex : int, n : int = 10000):
    """
    Finds the BiS of the player given a Gear search space and a Fight.
    Fight -> Fight object.
    GearSpace : dict -> Dictionnary filled with the different gear pieces the algorithm can search through.
    PlayerIndex : int -> Index of the player for which the user wants to optimize the gearset. Must be the index of the player
                         in the Fight.PlayerList.
    n : int -> Number of tries the solver has.
    """
                             # Computes the PreBakedAction
    Fight.SavePreBakedAction = True
    Fight.PlayerIDSavePreBakedAction = 0
    Fight.SimulateFight(0.01, 500, False, n=0,PPSGraph=False)

    Result = []

    newGearSet = GearSet()

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


                                                levelMod = 1900
                                                baseMain = 390  
                                                baseSub = 400# Level 90 LevelMod values

                                                JobMod = Fight.PlayerList[PlayerIndex].JobMod # Level 90 jobmod value, specific to each job

                                                f_WD = (GearStat["WD"]+floor(baseMain*JobMod/1000))/100 # Necessary to check if its not 0 since etro only returns the damage multiplier.
                                                f_DET = floor(1000+floor(140*(GearStat["Det"]-baseMain)/levelMod))/1000# Determination damage
                                                if Fight.PlayerList[PlayerIndex] == RoleEnum.Tank : f_TEN = (1000+floor(100*(GearStat["Ten"]-baseSub)/levelMod))/1000 # Tenacity damage, 1 for non-tank player
                                                else : f_TEN = 1 # if non-tank
                                                f_SPD = (1000+floor(130*((GearStat["SS"] if RoleEnum == RoleEnum.Caster or RoleEnum == RoleEnum.Healer else GearStat["SkS"])-baseSub)/levelMod))/1000 # Used only for dots
                                                f_CritRate = floor((200*(GearStat["Crit"]-baseSub)/levelMod+50))/1000 # Crit rate in decimal
                                                f_CritMult = (floor(200*(GearStat["Crit"]-baseSub)/levelMod+400))/1000 # Crit Damage multiplier
                                                f_DH = floor(550*(GearStat["DH"]-baseSub)/levelMod)/1000 # DH rate in decimal

                                                ExpectedDamage, RandomDamage = Fight.SimulatePreBakedFight(PlayerIndex, GearStat["MainStat"],f_WD, f_DET, f_TEN, f_SPD, f_CritRate, f_CritMult, f_DH)
                                                Result += [(ExpectedDamage, RandomDamage)]

    print(Result)




    