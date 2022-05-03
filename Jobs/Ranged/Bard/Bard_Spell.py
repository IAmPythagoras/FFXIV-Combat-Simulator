from Jobs.Base_Spell import DOTSpell
from Jobs.Ranged.Ranged_Spell import BardSpell
import copy
Lock = 0.75

#Thanks for birdy for da help lol. Bitchiest bard I've ever known, much love

"""
Because of the inherent random nature of Bard, every spell that requires luck based proc
will be avaible at all time. However, the Player object will keep track of an expected amount of
procs and will compare it at the end to the number of actually done procs of that ability.
A check will be done notheless to make sure a rotation is at least possible given enough luck
"""


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
    if Player.MaximumRepertoire == 0 : return False
    elif Player.MaximumRepertoire == 2:
        Spell.Potency += 120
    elif Player.MaximumRepertoire == 3:
        Spell.Potency += 260
    else:
        input("lol, somehting went wrong in bard")
    return Player.WandererMinuet

def PitchPerfect1Requirement(Player, Spell):
    if Player.MaximumRepertoire < 1:#It will not be possible to cast in any case
        return False
    else:
        #We can cast it, and we have to check the chances
        need = min(0, Player.ExpectedRepertoire - 1)
        Player.UsedRepertoireAdd += need
        return True

def PitchPerfect2Requirement(Player, Spell):
    if Player.MaximumRepertoire < 2:#It will not be possible to cast in any case
        return False
    else:
        #We can cast it, and we have to check the chances
        need = min(0, Player.ExpectedRepertoire - 2)
        Player.UsedRepertoireAdd += need
        return True

def PitchPerfect3Requirement(Player, Spell):
    if Player.MaximumRepertoire < 3:#It will not be possible to cast in any case
        return False
    else:
        #We can cast it, and we have to check the chances
        need = min(0, Player.ExpectedRepertoire - 3)
        Player.UsedRepertoireAdd += need
        return True

def WandererMinuetRequirement(Player, Spell):
    return Player.WandererMinuetCD <= 0

def BattleVoiceRequirement(Player, Spell):
    return Player.BattleVoiceCD <= 0

def BloodLetterRequirement(Player, Spell):
    #This requirement will check if the spell can be casted. If it cannot, it will cast it anyway, but will add to
    #the UsedBloodLetterReduction so we know by how much we go over it
    if Player.BloodLetterStack <= 0:# In which case we have to add to UsedBloodLetterReduction
        #We will look at the current cooldown on the ability, and add the rest of what it needs
        #Might want to check and make it more punishing if we are not in mage ballad

        need = 15 - Player.BloodLetterCD #What reduction we need
        Player.UsedBloodLetterReduction += need

    return True

def ArmyPaeonRequirement(Player, Spell):
    return Player.ArmyPaeonCD <= 0

def MageBalladRequirement(Player, Spell):
    return Player.MageBalladCD <= 0

def BarrageRequirement(Player, Spell):
    return Player.BarrageCD <= 0

def RagingStrikeRequirement(Player, Spell):
    return Player.RagingStrikeRequirement

def RadiantFinaleRequirement(Player, Spell):
    return Player.MageCoda or Player.ArmyCoda or Player.WandererCoda

def BlastArrowRequirement(Player, Spell):
    return Player.BlastArrowReady

#Apply

def ApplyBurstShot(Player, Enemy):
    Player.StraightShotReady = True #We assume it will be true, in reality it has 35% chance
    Player.ExpectedRefulgent += 0.35

def ApplyRefulgentArrow(Player, Enemy):
    Player.StraightShotReady = False
    Player.UsedRefulgent += 1

def ApplyStormbite(Player, Enemy):
    Player.StraightShotReady = True #We assume it will be true, in reality it has 35% chance
    Player.ExpectedRefulgent += 0.35
    if Player.StormbiteDOT == None:
        Player.StormbiteDOT = copy.deepcopy(StormbiteDOT)
        Player.DOTList.append(Player.StormbiteDOT)
        Player.EffectCDList.append(StormbiteDOTCheck)
    Player.StormbiteDOTTimer = 45

def ApplyCausticbite(Player, Enemy):
    Player.StraightShotReady = True #We assume it will be true, in reality it has 35% chance
    Player.ExpectedRefulgent += 0.35
    if Player.CausticbiteDOT == None:
        Player.CausticbiteDOT = copy.deepcopy(CausticbiteDOT)
        Player.DOTList.append(Player.CausticbiteDOT)
        Player.EffectCDList.append(CausticbiteDOTCheck)
    Player.CausticbiteDOT = 45

def ApplySidewinder(Player, Enemy):
    Player.SidewinderCD = 60

def ApplyIronJaws(Player, Enemy):
    Player.StraightShotReady = True #We assume it will be true, in reality it has 35% chance
    Player.ExpectedRefulgent += 0.35

    if Player.StormbiteDOT != None : Player.StormbiteDOTTimer = 45
    if Player.CausticDOT != None : Player.CausticDOTTimer = 45

def ApplyEmpyrealArrow(Player, Enemy):
    Player.EmpyrealArrowCD = 15

def ApplyPitchPerfect1(Player, Enemy):
    Player.MaximumRepertoire = max(0, Player.MaximumRepertoire - 1)
    Player.ExpectedRepertoire = max(0, Player.ExpectedRepertoire - 1)

def ApplyPitchPerfect2(Player, Enemy):
    Player.MaximumRepertoire = max(0, Player.MaximumRepertoire - 2)
    Player.ExpectedRepertoire = max(0, Player.ExpectedRepertoire - 2)

def ApplyPitchPerfect3(Player, Enemy):
    Player.MaximumRepertoire = max(0, Player.MaximumRepertoire - 3)
    Player.ExpectedRepertoire = max(0, Player.ExpectedRepertoire - 3)


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
    Player.WandererCoda = True #Adding Coda
    Player.WandererMinuetCD = 120
    Player.SongTimer = 45
    Enemy.WandererMinuet = True
    Player.EffectCDList.append(WandererCheck)
    Player.EffectList.append(WandererEffect)
    #Removing Current song
    Player.MageBallad = False
    Player.ArmyPaeon = False
    Player.WandererMinuet = True

def ApplyArmyPaeon(Player, Enemy):
    Player.ArmyCoda = True #Adding Coda
    Enemy.ArmyPaeon = True
    Player.ArmyPaeonCD = 120
    Player.SongTimer = 45
    Player.EffectCDList.append(ArmyPaeonCheck)
    Player.EffectList.append(ArmyPaeonEffect)
    #Have to remove current song
    Player.MageBallad = False
    Player.ArmyPaeon = True
    Player.WandererMinuet = False

def ApplyMageBallad(Player, Enemy):
    Player.MageCoda = True #Adding Coda
    Enemy.Bonus *= 1.01 #DPS Bonus
    Player.SongTimer = 45
    Player.MageBalladCD = 120
    Player.EffectCDList.append(MageBalladCheck)
    Player.EffectList.append(MageBalladEffect)
    #Have to remove current song
    Player.MageBallad = True
    Player.ArmyPaeon = False
    Player.WandererMinuet = False

def ApplyBarrage(Player, Enemy):
    Player.EffectList.append(BarrageEffect)
    Player.StraightShotReady = True #This one will always happen
    Player.ExpectedRefulgent += 1 #So we simply add 1 since ^
    Player.BarrageCD = 120

def ApplyRagingStrike(Player, Enemy):
    Player.MultDPSBonus *=1.15
    Player.RagingStrikeTimer = 20
    Player.EffectCDList.append(RagingStrikeCheck)

def ApplyRadiantFinale(Player, Enemy):
    #Will first have to find how many coda we have
    coda = 0
    if Player.MageCoda: coda += 1
    if Player.ArmyCoda: coda += 1
    if Player.WandererCoda: coda += 1
    Player.RadiantFinaleBonus = coda * 1.02
    Enemy.Bonus *= Player.RadiantFinaleBonus #Multiplying by the bonus
    Player.RadiantFinaleTimer = 15
    Player.EffectCDList.append(RadiantFinaleCheck)
    Player.MageCoda = False
    Player.ArmyCoda = False
    Player.Wanderer = False
    #We used all coda

def ApplyBlastArrow(Player, Enemy):
    Player.BlastArrowReady = False

def ApplyApexArrow20(Player, Enemy):
    Player.UsedSoulVoiceGauge += 20

def ApplyApexArrow80(Player, Enemy):
    Player.UsedSoulVoiceGauge += 80
    Player.BlastArrowReady = True

#Effect

def BarrageEffect(Player, Spell):
    if Spell.WeaponSkill:
        Spell.Potency *= 3 #Triples potency. Shouldn't be a problem since Bard has no combo
        Player.EffectToRemove.append(BarrageEffect)


def SongEffect(Player, Spell):
    #This effect is constantly on the player and will keep track of the expected number of expected SoulVoiceGauge
    if Player.SongTimer%3 == 0 and Player.SongTimer > 0 :
        Player.ExpectedSoulVoiceGauge += 5 * 0.8 #We have an expected of 5 voice each proc with a chance of 80%

def WandererEffect(Player, Spell):
    #This effect will keep track of how many repertoire we should be having
    if Player.SongTimer%3 == 0:
        Player.MaximumRepertoire = min(3, Player.MaximumRepertoire + 1) #Adding to MaximumRepertoire, this is to make sure a Pitch Perfect is at least possible
        Player.ExpectedRepertoire = min(3, Player.ExpectedRepertoire + 0.8)


def ArmyPaeonEffect(Player, Spell):
    #The effect will assume we get 4 procs in 5 GCD, since that is the expected number of proc it should take since we have 80% chance each GCD
    #We could change that as necessary
    #It will add 0.8 repertoire each proc since we have 80% chance for a max of 4 procs

    if Player.SongTimer%3 == 0 and not (Player.Repertoire == 4.0):
        Player.Repertoire += 0.8

    if Spell.GCD: #This if is after since a spell can affect its own GCD
        Spell.RecastTime *= (1 - 0.04 * Player.Repertoire) #Making GCD faster
        #Since CastTime is always Lock for Bard, only affecting RecastTime

def MageBalladEffect(Player, Spell):
    #This effect will assume that each GCD, the CD is reduced by 7.5 sec, but we will keep track of 
    #the Used CD and the expected CD reduction

    if Player.SongTimer%3 == 0: #The effect applies each 3 seconds, so we check each such interval 
        Player.BloodLetterCD = max(0, Player.BloodLetterCD - 7.5) #Reducing it
        Player.ExpectedBloodLetterReduction += 7.5 * 0.8 #Adding expected reduction


#Check

def RadiantFinaleCheck(Player, Enemy):
    if Player.RadiantFinaleTimer <= 0:
        Enemy.Bonus /= Player.RadiantFinaleBonus
        Player.EffectToRemove.append(RadiantFinaleCheck)

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
        Player.EffectList.remove(WandererEffect)

def ArmyPaeonCheck(Player, Enemy):
    if Player.SongTimer <= 0 or not (Player.ArmyPaeon):
        Enemy.ArmyPaeon = False
        Player.ArmyPaeon = False
        Player.EffectToRemove.append(ArmyPaeonCheck)
        Player.EffectList.remove(ArmyPaeonEffect)

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
ApexArrow20 = BardSpell(16, True, 2.5, 200, ApplyApexArrow20, [])
ApexArrow80 = BardSpell(17, True, 2.5, 500, ApplyApexArrow80, [])
BlastArrow = BardSpell(18, True, 2.5, 600, ApplyBlastArrow, [BlastArrowRequirement])

#Song
WandererMinuet = BardSpell(8, False, 0, 100, ApplyWandererMinuet, [WandererMinuetRequirement])
ArmyPaeon = BardSpell(11, False, 0, 100, ApplyArmyPaeon, [ArmyPaeonRequirement])
MageBallad = BardSpell(12, False, 0, 100, ApplyMageBallad, [MageBalladRequirement])
#oGCD
Sidewinder = BardSpell(4, False, 0, 300, ApplySidewinder, [SidewinderRequirement])
EmpyrealArrow = BardSpell(6, False, 0, 200, ApplyEmpyrealArrow, [EmpyrealArrowRequirement])
BattleVoice = BardSpell(9, False, 0, 0, ApplyBattleVoice, [BattleVoiceRequirement])
BloodLetter = BardSpell(10, False, 0, 110, ApplyBloodLetter, [BloodLetterRequirement])
Barrage = BardSpell(13, False, 0, 0, ApplyBarrage, [BarrageRequirement])
RagingStrike = BardSpell(14, False, 0, 0, ApplyRagingStrike, [RagingStrikeRequirement])
RadiantFinale = BardSpell(15, False, 0, 0, ApplyRadiantFinale, [RadiantFinaleRequirement])
#Each PitchPerfecti represents a PitchPerfect with i repertoire
PitchPerfect1 = BardSpell(7, False, 0, 100, ApplyPitchPerfect1, [PitchPerfect1Requirement])
PitchPerfect2 = BardSpell(7, False, 0, 220, ApplyPitchPerfect2, [PitchPerfect2Requirement])
PitchPerfect3 = BardSpell(7, False, 0, 360, ApplyPitchPerfect3, [PitchPerfect3Requirement])