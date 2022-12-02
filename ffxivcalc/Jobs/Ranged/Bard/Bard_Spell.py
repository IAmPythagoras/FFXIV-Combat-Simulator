from ffxivcalc.Jobs.Base_Spell import DOTSpell, buff, empty
from ffxivcalc.Jobs.Ranged.Ranged_Spell import BardSpell
import copy
Lock = 0.5

#Thanks for birdy for da help lol. Bitchiest bard I've ever known, much love

"""
Because of the inherent random nature of Bard, every spell that requires luck based proc
will be avaible at all time. However, the Player object will keep track of an expected amount of
procs and will compare it at the end to the number of actually done procs of that ability.
A check will be done notheless to make sure a rotation is at least possible given enough luck
"""


#Requirement

def RefulgentArrowRequirement(Player, Spell):
    return Player.StraightShotReady, -1

def SidewinderRequirement(Player, Spell):
    return Player.SidewinderCD <= 0, Player.SidewinderCD

def EmpyrealArrowRequirement(Player, Spell):
    return Player.EmpyrealArrowCD <= 0, Player.EmpyrealArrowCD
"""
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
"""
def PitchPerfect1Requirement(Player, Spell):
    if Player.MaximumRepertoire < 1:#It will not be possible to cast in any case
        return False, -1
    else:
        #We can cast it, and we have to check the chances
        need = max(0, 1 - Player.ExpectedRepertoire)#This represents how much we would be missing, compared to the expected value
        Player.UsedRepertoireAdd += need#This represents the total number of repertoire procs we have used through out the simulation
        return Player.WandererMinuet, -1

def PitchPerfect2Requirement(Player, Spell):
    if Player.MaximumRepertoire < 2:#It will not be possible to cast in any case
        return False, -1
    else:
        #We can cast it, and we have to check the chances
        need = max(0, 2 - Player.ExpectedRepertoire)#This represents how much we would be missing, compared to the expected value
        Player.UsedRepertoireAdd += need#This represents the total number of repertoire procs we have used through out the simulation
        return Player.WandererMinuet, -1

def PitchPerfect3Requirement(Player, Spell):
    if Player.MaximumRepertoire < 3:#It will not be possible to cast in any case
        return True, -1
    else:
        #We can cast it, and we have to check the chances
        need = max(0, 3 - Player.ExpectedRepertoire) #This represents how much we would be missing, compared to the expected value
        Player.UsedRepertoireAdd += need #This represents the total number of repertoire procs we have used through out the simulation
        return Player.WandererMinuet, -1

def WandererMinuetRequirement(Player, Spell):
    return Player.WandererMinuetCD <= 0, Player.WandererMinuetCD

def BattleVoiceRequirement(Player, Spell):
    return Player.BattleVoiceCD <= 0, Player.BattleVoiceCD

def BloodLetterRequirement(Player, Spell):
    #This requirement will check if the spell can be casted. If it cannot, it will cast it anyway, but will add to
    #the UsedBloodLetterReduction so we know by how much we go over it
    if Player.BloodLetterStack <= 0:# In which case we have to add to UsedBloodLetterReduction
        #We will look at the current cooldown on the ability, and add the rest of what it needs
        #Might want to check and make it more punishing if we are not in mage ballad



        #We will first check if a blood letter at this point is even possible by looking at the maximal possible reduction
        need = 15 - Player.BloodLetterCD #What reduction we need
        #input("maxblood : " + str(Player.MaximumBloodLetterReduction))
        if Player.MaximumBloodLetterReduction - need < -10 : 
            input("Bard rotation might not be feasible")
            #return False, -1 #If it is bigger, than this rotation is impossible


        Player.MaximumBloodLetterReduction -= need #Updating new MaximumBloodLetterReduction
        Player.UsedBloodLetterReduction += need

    return True, -1

def ArmyPaeonRequirement(Player, Spell):
    return Player.ArmyPaeonCD <= 0, Player.ArmyPaeonCD

def MageBalladRequirement(Player, Spell):
    return Player.MageBalladCD <= 0, Player.MageBalladCD

def BarrageRequirement(Player, Spell):
    return Player.BarrageCD <= 0, Player.BarrageCD

def RagingStrikeRequirement(Player, Spell):
    return Player.RagingStrikeCD <= 0, Player.RagingStrikeCD

def RadiantFinaleRequirement(Player, Spell):
    return Player.MageCoda or Player.ArmyCoda or Player.WandererCoda, -1

def BlastArrowRequirement(Player, Spell):
    return Player.BlastArrowReady, -1

def ShadowbiteRequirement(Player, Spell):
    return Player.ShadowbiteReady, -1

def TroubadourRequirement(Player, Spell):
    return Player.TroubadourCD <= 0, Player.TroubadourCD

def WardenPaeanRequirement(Player, Spell):
    return Player.WardenPaeanCD <= 0, Player.WardenPaeanCD

def NatureMinneRequirement(Player, Spell):
    return Player.NatureMinneCD <= 0, Player.NatureMinneCD

#Apply

def ApplyNatureMinne(Player, Enemy):
    Player.NatureMinneCD = 90

def ApplyWardenPaean(Player, Enemy):
    Player.WardenPaeanCD = 45

def ApplyTroubadour(Player, Enemy):
    Player.TroubadourCD = 90

def ApplyLadonsbite(Player, Enemy):
    Player.ShadowbiteReady = True
    Player.ExpectedShadowbite += 0.35

def ApplyShadowbite(Player, Enemy):
    Player.ShadowbiteReady = False
    Player.UsedShadowbite += 1

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
    Player.CausticbiteDOTTimer = 45

def ApplySidewinder(Player, Enemy):
    Player.SidewinderCD = 60

def ApplyIronJaws(Player, Enemy):
    Player.StraightShotReady = True #We assume it will be true, in reality it has 35% chance
    Player.ExpectedRefulgent += 0.35

    if Player.StormbiteDOT != None : Player.StormbiteDOTTimer = 45
    if Player.CausticbiteDOT != None : Player.CausticbiteDOTTimer = 45

def ApplyEmpyrealArrow(Player, Enemy):
    Player.EmpyrealArrowCD = 15

def ApplyPitchPerfect1(Player, Enemy):
    Player.MaximumRepertoire = max(0, Player.MaximumRepertoire - 1)
    Player.ExpectedRepertoire = max(0, Player.ExpectedRepertoire - 1)
    Player.UsedTotalWandererRepertoire += 1

def ApplyPitchPerfect2(Player, Enemy):
    Player.MaximumRepertoire = max(0, Player.MaximumRepertoire - 2)
    Player.ExpectedRepertoire = max(0, Player.ExpectedRepertoire - 2)
    Player.UsedTotalWandererRepertoire += 2

def ApplyPitchPerfect3(Player, Enemy):
    Player.MaximumRepertoire = max(0, Player.MaximumRepertoire - 3)
    Player.ExpectedRepertoire = max(0, Player.ExpectedRepertoire - 3)
    Player.UsedTotalWandererRepertoire += 3
    #input("Using PitchPerfect 3, max is : " + str(Player.MaximumRepertoire))


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
    Enemy.buffList.append(MageBalladBuff)
    Player.SongTimer = 45
    Player.MageBalladCD = 120
    Player.EffectCDList.append(MageBalladCheck)
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
    Player.buffList.append(RagingStrikeBuff)
    Player.RagingStrikeTimer = 20
    Player.EffectCDList.append(RagingStrikeCheck)

def ApplyRadiantFinale(Player, Enemy):
    #Will first have to find how many coda we have
    coda = 0
    if Player.MageCoda: coda += 1
    if Player.ArmyCoda: coda += 1
    if Player.WandererCoda: coda += 1
    Player.RadiantFinalBuff = copy.deepcopy(RadiantFinaleBuff)
    Player.RadiantFinalBuff.MultDPS *= coda
    Player.RadiantFinalBuff.MultDPS = round(1 + Player.RadiantFinalBuff.MultDPS%1, 2)
    Enemy.buffList.append(Player.RadiantFinalBuff)
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
    if not isinstance(Spell, DOTSpell) and Spell.Weaponskill:
        if Spell.id == Shadowbite.id: Spell.Potency += 100
        else : Spell.Potency *= 3 #Triples potency. Shouldn't be a problem since Bard has no combo
        Player.EffectToRemove.append(BarrageEffect)


def SongEffect(Player, Spell):
    Player.EffectCDList.append(SongEffectCheck)
    Player.EffectToRemove.append(SongEffect)
"""
def WandererEffect(Player, Spell):
    #This effect will keep track of how many repertoire we should be having
    input("increasing repertoire")
    if Player.SongTimer%3 == 0 and Player.SongTimer != 45:
        input("increasing repertoire")
        Player.MaximumRepertoire = min(3, Player.MaximumRepertoire + 1) #Adding to MaximumRepertoire, this is to make sure a Pitch Perfect is at least possible
        Player.ExpectedRepertoire = min(3, Player.ExpectedRepertoire + 0.8)
"""

def ArmyPaeonEffect(Player, Spell):
    if Spell.GCD: #This if is after since a spell can affect its own GCD
        Spell.RecastTime *= (1 - 0.04 * Player.Repertoire) #Making GCD faster
        #Since CastTime is always Lock for Bard, only affecting RecastTime

#Check

def RadiantFinaleCheck(Player, Enemy):
    if Player.RadiantFinaleTimer <= 0:
        Enemy.buffList.remove(Player.RadiantFinalBuff)
        Player.EffectToRemove.append(RadiantFinaleCheck)

def RagingStrikeCheck(Player, Enemy):
    if Player.RagingStrikeTimer <= 0:
        Player.buffList.remove(RagingStrikeBuff)
        Player.EffectToRemove.append(RagingStrikeCheck)

def StormbiteDOTCheck(Player, Enemy):
    if Player.StormbiteDOTTimer <= 0:
        Player.DOTList.remove(Player.StormbiteDOT)
        Player.StormbitDOT = None
        Player.EffectToRemove.append(StormbiteDOTCheck)

def CausticbiteDOTCheck(Player, Enemy):
    if Player.CausticbiteDOTTimer <= 0:
        Player.DOTList.remove(Player.CausticbiteDOT)
        Player.CausticbiteDOT = None
        Player.EffectToRemove.append(CausticbiteDOTCheck)

def WandererCheck(Player, Enemy):


    #This effect is in the check since we want it to be called each frames
    if (int(Player.SongTimer*100)/100)%3 == 0 and Player.SongTimer != 45:
        Player.MaximumRepertoire = min(3, Player.MaximumRepertoire + 1) #Adding to MaximumRepertoire, this is to make sure a Pitch Perfect is at least possible
        Player.ExpectedRepertoire = min(3, Player.ExpectedRepertoire + 0.8)
        Player.ExpectedTotalWandererRepertoire += 0.8

    if Player.SongTimer <= 0 or not (Player.WandererMinuet): #We check if timer, or if it becomes false because another song has begun
        Enemy.WandererMinuet = False
        Player.WandererMinuet = True
        Player.EffectToRemove.append(WandererCheck)

def ArmyPaeonCheck(Player, Enemy):

    #The effect will assume we get 4 procs in 5 GCD, since that is the expected number of proc it should take since we have 80% chance each GCD
    #We could change that as necessary
    #It will add 0.8 repertoire each proc since we have 80% chance for a max of 4 procs

    if Player.SongTimer != 45 and (int(Player.SongTimer*100)/100)%3 == 0 and not (Player.Repertoire == 4.0):
        Player.Repertoire += 0.8

    if Player.SongTimer <= 0 or not (Player.ArmyPaeon):
        Enemy.ArmyPaeon = False
        Player.ArmyPaeon = False
        Player.EffectToRemove.append(ArmyPaeonCheck)
        Player.EffectList.remove(ArmyPaeonEffect)

def MageBalladCheck(Player, Enemy):

    if Player.SongTimer != 45 and (int(Player.SongTimer*100)/100)%3 == 0: #The effect applies each 3 seconds, so we check each such interval 
        Player.ExpectedBloodLetterReduction += 7.5 * 0.8 #Adding expected reduction
        Player.MaximumBloodLetterReduction += 7.5

    if Player.SongTimer <= 0 or not (Player.MageBallad):
        Enemy.buffList.remove(MageBalladBuff) #Remove DPSBonus
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


def SongEffectCheck(Player, Enemy):
    #This effect is constantly on the player and will keep track of the expected number of expected SoulVoiceGauge
    #This effect is in check since we want it to be called each frame
    if Player.SongTimer != 45 and (int(Player.SongTimer*100)/100)%3 == 0 and Player.SongTimer > 0 :
        Player.ExpectedSoulVoiceGauge += 5 * 0.8 #We have an expected of 5 voice each proc with a chance of 80%


#GCD
BurstShot = BardSpell(16495, True, 2.5, 220, ApplyBurstShot, [], True, type = 2)
RefulgentArrow = BardSpell(7409, True, 2.5, 280, ApplyRefulgentArrow, [RefulgentArrowRequirement], True, type = 2)
Stormbite = BardSpell(7407, True, 2.5, 100, ApplyStormbite, [], True, type = 2)
Causticbite = BardSpell(7406, True, 2.5, 150, ApplyCausticbite, [], True, type = 2)
StormbiteDOT = DOTSpell(-20, 25, True) #25
CausticbiteDOT = DOTSpell(-21, 20, True) #20
IronJaws = BardSpell(3560, True, 2.5, 100, ApplyIronJaws, [], True, type = 2)
ApexArrow20 = BardSpell(6, True, 2.5, 200, ApplyApexArrow20, [], True, type = 2)
ApexArrow80 = BardSpell(16496, True, 2.5, 500, ApplyApexArrow80, [], True, type = 2)
BlastArrow = BardSpell(25784, True, 2.5, 600, ApplyBlastArrow, [BlastArrowRequirement],True, type = 2)

#AOE GCD
Ladonsbite = BardSpell(25783, True, 0, 2.5, ApplyLadonsbite, [], True, type = 2)
Shadowbite = BardSpell(16494, True, 2.5, 170, ApplyShadowbite, [ShadowbiteRequirement], True, type = 2)


#Song
WandererMinuet = BardSpell(3559, False, 0, 100, ApplyWandererMinuet, [WandererMinuetRequirement], False)
ArmyPaeon = BardSpell(116, False, 0, 100, ApplyArmyPaeon, [ArmyPaeonRequirement],False)
MageBallad = BardSpell(114, False, 0, 100, ApplyMageBallad, [MageBalladRequirement],False)
#oGCD
Sidewinder = BardSpell(3562, False, 0, 300, ApplySidewinder, [SidewinderRequirement],False)
EmpyrealArrow = BardSpell(3558, False, 0, 230, ApplyEmpyrealArrow, [EmpyrealArrowRequirement],False)
BattleVoice = BardSpell(118, False, 0, 0, ApplyBattleVoice, [BattleVoiceRequirement],False)
BloodLetter = BardSpell(110, False, 0, 110, ApplyBloodLetter, [BloodLetterRequirement],False)
RainOfDeath = BardSpell(117, False, 0, 110, ApplyBloodLetter, [BloodLetterRequirement],False) #AOE Version of BloodLetter
Barrage = BardSpell(107, False, 0, 0, ApplyBarrage, [BarrageRequirement],False)
RagingStrike = BardSpell(101, False, 0, 0, ApplyRagingStrike, [RagingStrikeRequirement],False)
RadiantFinale = BardSpell(25785, False, 0, 0, ApplyRadiantFinale, [RadiantFinaleRequirement],False)
Troubadour = BardSpell(7405, False, 0, 0, ApplyTroubadour, [TroubadourRequirement], False)
RepellingShot = BardSpell(112, False, 0, 0, empty, [], False) #No requirement, do that shit forever
WardenPaean = BardSpell(3561, False, 0, 0, ApplyWardenPaean, [WardenPaeanRequirement], False)
#Each PitchPerfecti represents a PitchPerfect with i repertoire
PitchPerfect1 = BardSpell(24, False, 0, 100, ApplyPitchPerfect1, [PitchPerfect1Requirement],False)
PitchPerfect2 = BardSpell(25, False, 0, 220, ApplyPitchPerfect2, [PitchPerfect2Requirement],False)
PitchPerfect3 = BardSpell(7404, False, 0, 360, ApplyPitchPerfect3, [PitchPerfect3Requirement],False)

#buff
RadiantFinaleBuff = buff(1.02)
RagingStrikeBuff = buff(1.15)
MageBalladBuff = buff(1.01)

def NatureMinne(target):
    Nature = BardSpell(7408, False, 0, 0, ApplyNatureMinne, [NatureMinneRequirement], False)
    Nature.TargetID = target.playerID
    return Nature

BardAbility = {
101 : RagingStrike, 
107 : Barrage, 
114 : MageBallad, 
116 : ArmyPaeon, 
117 : RainOfDeath, 
118 : BattleVoice, 
3558 : EmpyrealArrow, 
3559 : WandererMinuet, 
3560 : IronJaws, 
3561 : WardenPaean, 
3562 : Sidewinder ,
7404 : PitchPerfect3, 
7405 : Troubadour, 
7406 : Causticbite, 
7407 : Stormbite, 
7408 : NatureMinne, 
7409 : RefulgentArrow, 
16494 : Shadowbite, 
16495 : BurstShot, 
16496 : ApexArrow80, 
25783 : Ladonsbite, 
25785 : RadiantFinale, 
112 : RepellingShot, 
110 : BloodLetter,
25784 : BlastArrow
}