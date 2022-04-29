from Jobs.Base_Spell import DOTSpell, ManaRequirement, empty
from Jobs.Caster.Caster_Spell import SummonerSpell
import copy
Lock = 0.75

#Requirement

def Ruin4Requirement(Player, Spell):
    return Player.FurtherRuin

def TitanRequirement(Player, Spell):
    return Player.TitanGem

def IfritRequirement(Player, Spell):
    return Player.IfritGem

def GarudaRequirement(Player, Spell):
    return Player.GarudaGem

def TopazRequirement(Player, Spell):
    return Player.TitanStack > 0

def MountainRequirement(Player, Spell):
    return Player.TitanSpecial

def RubyRequirement(Player, Spell):
    return Player.IfritStack > 0

def CycloneRequirement(Player, Spell):
    return Player.IfritSpecial

def StrikeRequirement(Player, Spell):
    return Player.IfritSpecialCombo

def EmeraldRequirement(Player, Spell):
    return Player.GarudaStack > 0

def SlipstreamRequirement(Player, Spell):
    return Player.GarudaSpecial

def SummonRequirement(Player, Spell):
    return Player.SummonCD <= 0

def FoFRequirement(Player, Spell):
    return Player.FirebirdTrance

def AstralImpulseRequirement(Player, Spell):
    return Player.BahamutTrance

def EnkindleRequirement(Player, Spell):
    return Player.Enkindle

def DeathflareRequirement(Player, Spell):
    return Player.Deathflare

def EnergyDrainRequirement(Player, Spell):
    return Player.EnergyDrainCD <= 0

def FesterRequirement(Player, Spell):
    return Player.AetherflowGauge > 0

def SearingLightRequirement(Player, Spell):
    return Player.SearingLightCD <= 0

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


    Player.TitanGem = True
    Player.GarudaGem = True
    Player.IfritGem = True


    if not Player.LastTranceBahamut:
        #Then we summon bahamut
        Player.Deathflare = True
        Player.LastTranceBahamut = True
        Player.SummonDOT = copy.deepcopy(BahamutDOT)
        Player.BahamutTrance = True
    else:
        #Then we summon birdy
        Player.LastTranceBahamut = False
        Player.SummonDOT = copy.deepcopy(PhoenixDOT)
        Player.PhoenixTrance = True
    Player.DOTList.append(Player.SummonDOT)
    Player.EffectCDList.append(SummonDOTCheck)
    Player.SummonDOTTimer = 15

def ApplyEnkindle(Player, Enemy):
    Player.Enkindle = False

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

    Enemy.Bonus *= 1.03 #3% dps bonus
    Player.EffectCDList.append(SearingLightCheck)

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
        Player.DOTList.remove(Player.SummonDOT)
        Player.SummonDOT = None
        Player.EffectToRemove.append(SummonDOTCheck)
        Player.PhoenixTrance = False
        Player.BahamutTrance = False
        Player.Deathflare = False

def SearingLightCheck(Player, Enemy):
    if Player.SearingLightTimer <= 0:
        Enemy.Bonus /= 1.03
        Player.EffectToRemove.append(SearingLightCheck)


#GCD
Ruin3 = SummonerSpell(1, True, 1.5, 2.5, 310, 300, empty, [ManaRequirement])
Ruin4 = SummonerSpell(2, True, Lock, 2.5, 430, 400, ApplyRuin4, [ManaRequirement, Ruin4Requirement])
FoF = SummonerSpell(15, True, Lock, 2.5, 540, 300, empty, [FoFRequirement, ManaRequirement])
AstralImpulse = SummonerSpell(16, True, Lock, 2.5, 440, 300, empty, [AstralImpulseRequirement, ManaRequirement])
#Primal
Titan = SummonerSpell(3, True, Lock, 2.5, 700, 0, ApplyTitan, [TitanRequirement])
Garuda = SummonerSpell(4, True, Lock, 2.5, 700, 0, ApplyGaruda, [GarudaRequirement])
Ifrit = SummonerSpell(5, True, Lock, 2.5, 700, 0, ApplyIfrit, [IfritRequirement])

#Titan Ability
Topaz = SummonerSpell(6, True, Lock, 2.5, 140, 330, ApplyTopaz, [ManaRequirement, TopazRequirement])
Mountain = SummonerSpell(7, False, Lock, 0, 150, 0, ApplyMountain, [MountainRequirement])

#IfritAbility
Ruby = SummonerSpell(8, True, 2.8, 3, 510, 300, ApplyRuby, [RubyRequirement, ManaRequirement] )
Cyclone = SummonerSpell(9, True, Lock, 2.5, 430, 0, ApplyCyclone, [CycloneRequirement])
Strike = SummonerSpell(10, True, Lock, 2.5, 430, 0, ApplyStrike, [StrikeRequirement])

#GarudaAbility
Emerald = SummonerSpell(11, True, Lock, 1.5, 230, 300, ApplyEmerald, [EmeraldRequirement, ManaRequirement])
Slipstream = SummonerSpell(12, True, 3, 3.5, 430, 0, ApplySlipstream, [SlipstreamRequirement])
SlipstreamDOT = DOTSpell(-13, 30)

#Summon
Summon = SummonerSpell(14, True, Lock, 2.5, 0, 0, ApplySummon, [SummonRequirement])
#Bahamut and Phoenix damage will simply be a dot
BahamutDOT = DOTSpell(-14, 180)
PhoenixDOT = DOTSpell(-15, 240)
#autos of summon seems to be faster if uses Enkindle, but always max 5

#oGCD
Enkindle = SummonerSpell(17, False, 0.25, 0, 1300, 0, ApplyEnkindle, [EnkindleRequirement]) #Smaller lock since executed by pet, might have to reconsider... >.>
Deathflare = SummonerSpell(18, False, Lock, 0, 500, 0, ApplyDeathflare, [DeathflareRequirement])
EnergyDrainSMN = SummonerSpell(19, False, Lock, 0, 200, 0, ApplyEnergyDrain, [EnergyDrainRequirement])
Fester = SummonerSpell(21, False, Lock, 0, 300, 0, ApplyFester, [FesterRequirement])
SearingLight = SummonerSpell(20, False, Lock, 0, 0, 0, ApplySearingLight, [SearingLightRequirement])