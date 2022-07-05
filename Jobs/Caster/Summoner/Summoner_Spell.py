from Jobs.Base_Spell import DOTSpell, ManaRequirement, WaitAbility, buff, empty
from Jobs.Caster.Caster_Spell import SummonerSpell
import copy

from Jobs.Caster.Summoner.Summoner_Player import BigSummon
Lock = 0.75

#Requirement

def Ruin4Requirement(Player, Spell):
    return Player.FurtherRuin, -1

def TitanRequirement(Player, Spell):
    return Player.TitanGem, -1

def IfritRequirement(Player, Spell):
    return Player.IfritGem, -1

def GarudaRequirement(Player, Spell):
    return Player.GarudaGem, -1

def TopazRequirement(Player, Spell):
    return Player.TitanStack > 0, -1

def MountainRequirement(Player, Spell):
    return Player.TitanSpecial, -1

def RubyRequirement(Player, Spell):
    return Player.IfritStack > 0, -1

def CycloneRequirement(Player, Spell):
    return Player.IfritSpecial, -1

def StrikeRequirement(Player, Spell):
    return Player.IfritSpecialCombo, -1

def EmeraldRequirement(Player, Spell):
    return Player.GarudaStack > 0, -1

def SlipstreamRequirement(Player, Spell):
    return Player.GarudaSpecial, -1

def SummonRequirement(Player, Spell):
    return Player.SummonCD <= 0, Player.SummonCD

def FoFRequirement(Player, Spell):
    return Player.FirebirdTrance, -1

def AstralImpulseRequirement(Player, Spell):
    return Player.BahamutTrance, -1

def EnkindleRequirement(Player, Spell):
    return Player.Enkindle, -1

def DeathflareRequirement(Player, Spell):
    return Player.Deathflare, -1

def EnergyDrainRequirement(Player, Spell):
    return Player.EnergyDrainCD <= 0, Player.EnergyDrainCD

def FesterRequirement(Player, Spell):
    return Player.AetherflowGauge > 0, -1

def SearingLightRequirement(Player, Spell):
    return Player.SearingLightCD <= 0, Player.SearingLightCD

#Apply

def ApplyRuin4(Player, Enemy):
    Player.FurtherRuin = False

def ApplyTitan(Player, Enemy):
    Player.TitanGem = False
    Player.TitanStack = 4

def ApplyIfrit(Player, Enemy):
    Player.IfritGem = False
    Player.IfritStack = 2
    Player.IfritSpecial = True

def ApplyGaruda(Player, Enemy):
    Player.GarudaGem = False
    Player.GarudaStack = 4
    Player.GarudaSpecial = True

def ApplyTopaz(Player, Enemy):
    Player.TitanStack -= 1
    Player.TitanSpecial = True

def ApplyMountain(Player, Enemy):
    Player.TitanSpecial = False

def ApplyRuby(Player, Enemy):
    Player.IfritStack -= 1

def ApplyCyclone(Player, Enemy):
    Player.IfritSpecial = False
    Player.IfritSpecialCombo = True
    Player.EffectList.append(IfritCombo)

def ApplyStrike(Player, Enemy):
    Player.IfritSpecialCombo = False

def ApplyEmerald(Player, Enemy):
    Player.GarudaStack -= 1

def ApplySlipstream(Player, Enemy):
    Player.GarudaSpecial = False

    Player.SlipstreamDOT = copy.deepcopy(SlipstreamDOT)
    Player.DOTList.append(Player.SlipstreamDOT)
    Player.SlipstreamDOTTimer = 15
    Player.EffectCDList.append(SlipstreamDOTCheck)

def ApplySummon(Player, Enemy):
    Player.SummonCD = 60
    Player.Enkindle = True

    #Will check if we already have a summon object
    if Player.Summon == None:
        Player.Summon = BigSummon(Player)
        Player.Summon.ActionSet.append(WaitAbility(0.01)) #So program doesn't crash >.>
    Player.TitanGem = True
    Player.GarudaGem = True
    Player.IfritGem = True


    Player.Summon.TrueLock = False #Delocking bahamut
    if not Player.LastTranceBahamut:
        #Then we summon bahamut
        Player.Deathflare = True
        Player.LastTranceBahamut = True
        Player.BahamutTrance = True

        Player.Summon.ActionSet.insert(Player.Summon.NextSpell + 1, BahamutAA) #Applying AA

    else:
        #Then we summon birdy
        Player.LastTranceBahamut = False
        Player.SummonDOT = copy.deepcopy(PhoenixDOT)
        Player.PhoenixTrance = True
        Player.Summon.ActionSet.insert(Player.Summon.NextSpell + 1, PhoenixAA)#Applying AA
    Player.EffectCDList.append(SummonDOTCheck)
    Player.SummonDOTTimer = 15

def ApplyEnkindle(Player, Enemy):
    Player.Enkindle = False
    Player.Summon.ActionSet.insert(Player.Summon.NextSpell + 1, EnkindleSummon)

def ApplyDeathflare(Player, Enemy):
    Player.Deathflare = False

def ApplyEnergyDrain(Player, Enemy):
    Player.AetherflowGauge = 2
    Player.AetherflowCD = 60

def ApplyFester(Player, Enemy):
    Player.AetherflowGauge -= 1

def ApplySearingLight(Player, Enemy):
    Player.SearingLightTimer = 30
    Player.SearingLightCD = 120

    Enemy.buffList.append(SearingLightbuff)
    Player.EffectCDList.append(SearingLightCheck)


def ApplyBahamutAA(Player, Enemy):
    Player.DOTList.append(copy.deepcopy(BahamutDOT))

def ApplyPhoenixAA(Player, Enemy):
    Player.DOTList.append(copy.deepcopy(PhoenixDOT))

#Effect

def IfritCombo(Player, Spell):
    #Simply to make sure we loose the combo if we do another GCD
    if Spell.GCD:
        if Spell.id != Strike.id:
            Player.IfritSpecialCombo = False
        Player.EffectToRemove.append(IfritCombo)

#Check

def SlipstreamDOTCheck(Player, Enemy):
    if Player.SlipstreamDOTTimer <= 0:
        Player.DOTList.remove(Player.SlipStreamDOT)
        Player.EffectToRemove.append(SlipstreamDOTCheck)
        Player.SlipstreamDOT = None

def SummonDOTCheck(Player, Enemy):
    if Player.SummonDOTTimer <= 0:

        Player.Summon.DOTList = [] #Reseting DOTList

        Player.EffectToRemove.append(SummonDOTCheck)
        Player.PhoenixTrance = False
        Player.BahamutTrance = False
        Player.Deathflare = False

def SearingLightCheck(Player, Enemy):
    if Player.SearingLightTimer <= 0:
        Enemy.buffList.remove(SearingLightbuff)
        Player.EffectToRemove.append(SearingLightCheck)


#GCD
Ruin3 = SummonerSpell(1, True, 1.5, 2.5, 310, 300, empty, [ManaRequirement])
Ruin4 = SummonerSpell(2, True, Lock, 2.5, 430, 400, ApplyRuin4, [ManaRequirement, Ruin4Requirement])
FoF = SummonerSpell(15, True, Lock, 2.5, 540, 300, empty, [FoFRequirement, ManaRequirement])
AstralImpulse = SummonerSpell(16, True, Lock, 2.5, 440, 300, empty, [AstralImpulseRequirement, ManaRequirement])
TryDisaster = SummonerSpell(17, True, 1.5, 2.5, 120, 300, empty, [ManaRequirement])
#Primal
Titan = SummonerSpell(3, True, Lock, 2.5, 700, 0, ApplyTitan, [TitanRequirement])
Garuda = SummonerSpell(4, True, Lock, 2.5, 700, 0, ApplyGaruda, [GarudaRequirement])
Ifrit = SummonerSpell(5, True, Lock, 2.5, 700, 0, ApplyIfrit, [IfritRequirement])

#Titan Ability
Topaz = SummonerSpell(6, True, Lock, 2.5, 140, 330, ApplyTopaz, [ManaRequirement, TopazRequirement])
Mountain = SummonerSpell(7, False, Lock, 0, 150, 0, ApplyMountain, [MountainRequirement])
TopazCatastrophe = SummonerSpell(8, True, 0, 2.5, 140, 300, ApplyTopaz, [ManaRequirement, TopazRequirement] ) #same effect and requirement as Topaz

#IfritAbility
Ruby = SummonerSpell(8, True, 2.8, 3, 510, 300, ApplyRuby, [RubyRequirement, ManaRequirement] )
Cyclone = SummonerSpell(9, True, Lock, 2.5, 430, 0, ApplyCyclone, [CycloneRequirement])
Strike = SummonerSpell(10, True, Lock, 2.5, 430, 0, ApplyStrike, [StrikeRequirement])
RubyCatastrophe = SummonerSpell(11, True, 2.8, 2.5, 210, 300, ApplyRuby, [RubyRequirement, ManaRequirement]) #Same as Ruby
#GarudaAbility
Emerald = SummonerSpell(11, True, Lock, 1.5, 230, 300, ApplyEmerald, [EmeraldRequirement, ManaRequirement])
EmeraldCatastrophe = SummonerSpell(12, True, 0, 1.5, 100, 300, ApplyEmerald, [ManaRequirement, EmeraldRequirement])
Slipstream = SummonerSpell(12, True, 3, 3.5, 430, 0, ApplySlipstream, [SlipstreamRequirement])
SlipstreamDOT = DOTSpell(-13, 30, False)

#Summon
Summon = SummonerSpell(14, True, Lock, 2.5, 0, 0, ApplySummon, [SummonRequirement])
#Bahamut and Phoenix damage will simply be a dot
BahamutAA = SummonerSpell(15, False, 0, 0, 0, 0, ApplyBahamutAA, [])
PhoenixAA = SummonerSpell(15, False, 0, 0, 0, 0, ApplyPhoenixAA, [])
BahamutDOT = DOTSpell(-14, 180, False)
PhoenixDOT = DOTSpell(-15, 240, False)
EnkindleSummon = SummonerSpell(17, False, 0, 0, 1300, 0, empty, []) #Enkindle done by pet
#autos of summon seems to be faster if uses Enkindle, but always max 5

#oGCD
Enkindle = SummonerSpell(17, False, 0, 0, 0, 0, ApplyEnkindle, [EnkindleRequirement]) #Smaller lock since executed by pet, might have to reconsider... >.>
Deathflare = SummonerSpell(18, False, Lock, 0, 500, 0, ApplyDeathflare, [DeathflareRequirement])
EnergyDrainSMN = SummonerSpell(19, False, Lock, 0, 200, 0, ApplyEnergyDrain, [EnergyDrainRequirement])
Fester = SummonerSpell(21, False, Lock, 0, 300, 0, ApplyFester, [FesterRequirement])
PainFlare = SummonerSpell(22, False, 0, 0, 150, 0, ApplyFester, [FesterRequirement]) #AOE version of Fester
SearingLight = SummonerSpell(20, False, Lock, 0, 0, 0, ApplySearingLight, [SearingLightRequirement])

#buff
SearingLightbuff = buff(1.03)

SummonerAbility = {}