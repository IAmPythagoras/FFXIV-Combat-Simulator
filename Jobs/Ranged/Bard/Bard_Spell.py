from Jobs.Base_Spell import DOTSpell
from Jobs.Ranged.Ranged_Spell import BardSpell
import copy
Lock = 0.75


#Requirement

def RefulgentArrowRequiremen(Player, Spell):
    return Player.StraightShotReady

def SidewinderRequirement(Player, Spell):
    return Player.SidewinderCD <= 0

def EmpyrealArrowRequirement(Player, Spell):
    return Player.EmpyrealArrowCD <= 0

def PitchPerfectRequirement(Player, Spell):
    #I will modify the potency of the spell here since if I do it in apply, it will be harder to access spell
    #I won't consider if only 1 repertoire since the spell has by default 100 potency
    if Player.RepertoireStack == 0 : return False
    elif Player.RepertoireStack == 2:
        Spell.Potency += 120
    elif Player.RepertoireStack == 3:
        Spell.Potency += 260
    else:
        input("lol, somehting went wrong in bard")
    return Player.WandererMinuet

def WandererMinuetRequirement(Player, Spell):
    return Player.WandererMinuetCD <= 0

def BattleVoiceRequirement(Player, Spell):
    return Player.BattleVoiceCD <= 0

def BloodLetterRequirement(Player, Spell):
    return Player.BloodLetterStack > 0

def ArmyPaeonRequirement(Player, Spell):
    return Player.ArmyPaeonCD <= 0

def MageBalladRequirement(Player, Spell):
    return Player.MageBalladCD <= 0

def BarrageRequirement(Player, Spell):
    return Player.BarrageCD <= 0

def RagingStrikeRequirement(Player, Spell):
    return Player.RagingStrikeRequirement

#Apply

def ApplyBurstShot(Player, Enemy):
    Player.StraightShotReady = True #We assume it will be true, in reality it has 35% chance

def ApplyRefulgentArrow(Player, Enemy):
    Player.StraightShotReady = False

def ApplyStormbite(Player, Enemy):
    Player.StraightShotReady = True #We assume it will be true, in reality it has 35% chance
    if Player.StormbiteDOT == None:
        Player.StormbiteDOT = copy.deepcopy(StormbiteDOT)
        Player.DOTList.append(Player.StormbiteDOT)
        Player.EffectCDList.append(StormbiteDOTCheck)
    Player.StormbiteDOTTimer = 45

def ApplyCausticbite(Player, Enemy):
    Player.StraightShotReady = True #We assume it will be true, in reality it has 35% chance
    if Player.CausticbiteDOT == None:
        Player.CausticbiteDOT = copy.deepcopy(CausticbiteDOT)
        Player.DOTList.append(Player.CausticbiteDOT)
        Player.EffectCDList.append(CausticbiteDOTCheck)
    Player.CausticbiteDOT = 45

def ApplySidewinder(Player, Enemy):
    Player.SidewinderCD = 60

def ApplyIronJaws(Player, Enemy):
    Player.StraightShotReady = True #We assume it will be true, in reality it has 35% chance

    if Player.StormbiteDOT != None : Player.StormbiteDOTTimer = 45
    if Player.CausticDOT != None : Player.CausticDOTTimer = 45

def ApplyEmpyrealArrow(Player, Enemy):
    Player.EmpyrealArrowCD = 15

def ApplyPitchPerfect(Player, Enemy):
    Player.RepertoireStack = 0


def ApplyBattleVoice(Player, Enemy):
    Player.BattleVoiceTimer = 15
    Player.BattleVoiceCD = 120
    Enemy.BattleVoice = True
    Player.EffectCDList.append(BattleVoiceCheck)

def ApplyBloodLetter(Player, Enemy):
    if Player.BloodLetterStack == 3:
        Player.EffectCDList.append(BloodLetterStackCheck)
        Player.BloodLetterCD = 15
    Player.BloodLetterStack -= 1

def ApplyWandererMinuet(Player, Enemy):
    Player.WandererMinuetCD = 120

    Player.SongTimer = 45
    Enemy.WandererMinuet = True
    Player.EffectCDList.append(WandererCheck)
    #Have to figure out the 80% chance of repertoire
    #Removing Current song
    Player.MageBallad = False
    Player.ArmyPaeon = False
    Player.WandererMinuet = True

def ApplyArmyPaeon(Player, Enemy):
    Enemy.ArmyPaeon = True
    Player.ArmyPaeonCD = 120
    Player.SongTimer = 45
    #Have to remove current song
    Player.MageBallad = False
    Player.ArmyPaeon = True
    Player.WandererMinuet = False

def ApplyMageBallad(Player, Enemy):
    Enemy.Bonus *= 1.01 #DPS Bonus
    Player.SongTimer = 45
    Player.MageBalladCD = 120
    #Have to remove current song
    Player.MageBallad = True
    Player.ArmyPaeon = False
    Player.WandererMinuet = False

def ApplyBarrage(Player, Enemy):
    Player.EffectList.append(BarrageEffect)
    Player.StraightShotReady = True
    Player.BarrageCD = 120

def ApplyRagingStrike(Player, Enemy):
    Player.MultDPSBonus *=1.15
    Player.RagingStrikeTimer = 20
    Player.EffectCDList.append(RagingStrikeCheck)

#Effect

def BarrageEffect(Player, Spell):
    if Spell.WeaponSkill:
        Spell.Potency *= 3 #Triples potency. Shouldn't be a problem since Bard has no combo
        Player.EffectToRemove.append(BarrageEffect)

#Check

def RagingStrikeCheck(Player, Enemy):
    if Player.RagingStrikeTimer <= 0:
        Player.MultDPSBonus /= 1.2
        Player.EffectToRemove.append(RagingStrikeCheck)

def StormbiteDOTCheck(Player, Enemy):
    if Player.StormbiteDOTTimer <= 0:
        Player.DOTList.remove(Player.StormbiteDOT)
        Player.StormbitDOT = None
        Player.EffectToRemove.append(StormbiteDOTCheck)

def CausticbiteDOTCheck(Player, Enemy):
    if Player.CausticbitDOTTimer <= 0:
        Player.DOTList.remove(Player.CausticbiteDOT)
        Player.CausticbiteDOT = None
        Player.EffectToRemove.append(CausticbiteDOTCheck)

def WandererCheck(Player, Enemy):
    if Player.SongTimer <= 0 or not (Player.WandererMinuet): #We check if timer, or if it becomes false because another song has begun
        Enemy.WandererMinuet = False
        Player.WandererMinuet = True
        Player.EffectToRemove.append(WandererCheck)

def ArmyPaeonCheck(Player, Enemy):
    if Player.SongTimer <= 0 or not (Player.ArmyPaeon):
        Enemy.ArmyPaeon = False
        Player.ArmyPaeon = False
        Player.EffectToRemove.append(ArmyPaeonCheck)

def MageBalladCheck(Player, Enemy):
    if Player.SongTimer <= 0 or not (Player.MageBallad):
        Enemy.Bonus /= 1.01 #Remove DPSBonus
        Player.MageBallad = False
        Player.EffectToRemove.append(MageBalladCheck)

def BattleVoiceCheck(Player, Enemy):
    if Player.BattleVoiceTimer <= 0:
        Player.EffectToRemove.append(BattleVoiceCheck)
        Enemy.BattleVoice = False

def BloodLetterStackCheck(Player, Enemy):
    if Player.BloodLetterCD <= 0:
        if Player.BloodLetterStack == 2:
            Player.EffectToRemove.append(BloodLetterStackCheck)
        else:
            Player.BloodLetterCD = 15
        Player.BloodLetterStack += 1







#GCD
BurstShot = BardSpell(0, True, 2.5, 220, ApplyBurstShot, [])
RegulgentArrow = BardSpell(1, True, 2.5, 280, ApplyRefulgentArrow, [RefulgentArrowRequiremen])
Stormbite = BardSpell(2, True, 2.5, 100, ApplyStormbite, [])
Causticbite = BardSpell(3, True, 2.5, 150, ApplyCausticbite, [])
StormbiteDOT = DOTSpell(-20, 25)
CausticbiteDOT = DOTSpell(-21, 20)
IronJaws = BardSpell(5, True, 2.5, 100, ApplyIronJaws, [])



#Song
WandererMinuet = BardSpell(8, False, 0, 100, ApplyWandererMinuet, [WandererMinuetRequirement])
ArmyPaeon = BardSpell(11, False, 0, 100, ApplyArmyPaeon, [ArmyPaeonRequirement])
MageBallad = BardSpell(12, False, 0, 100, ApplyMageBallad, [MageBalladRequirement])
#oGCD
Sidewinder = BardSpell(4, False, 0, 300, ApplySidewinder, [SidewinderRequirement])
EmpyrealArrow = BardSpell(6, False, 0, 200, ApplyEmpyrealArrow, [EmpyrealArrowRequirement])
PitchPerfect = BardSpell(7, False, 0, 100, ApplyPitchPerfect, [PitchPerfectRequirement])
BattleVoice = BardSpell(9, False, 0, 0, ApplyBattleVoice, [BattleVoiceRequirement])
BloodLetter = BardSpell(10, False, 0, 110, ApplyBloodLetter, [BloodLetterRequirement])
Barrage = BardSpell(13, False, 0, 0, ApplyBarrage, [BarrageRequirement])
RagingStrike = BardSpell(14, False, 0, 0, ApplyRagingStrike, [RagingStrikeRequirement])