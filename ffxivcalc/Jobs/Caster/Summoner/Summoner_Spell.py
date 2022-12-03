from ffxivcalc.Jobs.Base_Spell import DOTSpell, ManaRequirement, WaitAbility, buff, empty
from ffxivcalc.Jobs.Caster.Caster_Spell import SummonerSpell
import copy

from ffxivcalc.Jobs.Player import Pet

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
    Player.SummonCD = 60 * Player.SpellReduction
    Player.Enkindle = True

    #Will check if we already have a summon object
    if Player.Pet == None:
        Pet(Player) # Summoning a pet for this player
        Player.Pet.ActionSet.append(WaitAbility(0.01)) #So program doesn't crash >.>
    else: Player.Pet.ResetStat() # Reseting stat on the summon

    # Can summon primals
    Player.TitanGem = True
    Player.GarudaGem = True
    Player.IfritGem = True



    Player.Pet.TrueLock = False #Delocking bahamut
    if not Player.LastTranceBahamut:
        #Then we summon bahamut
        Player.Deathflare = True
        Player.LastTranceBahamut = True
        Player.BahamutTrance = True
        Player.Pet.TrueLock = False
        Player.Pet.ActionSet.insert(Player.Pet.NextSpell + 1, BahamutAA) #Applying AA
    else:
        #Then we summon birdy
        Player.LastTranceBahamut = False
        Player.SummonDOT = copy.deepcopy(PhoenixDOT)
        Player.FirebirdTrance = True
        Player.Pet.TrueLock = False
        Player.Pet.ActionSet.insert(Player.Pet.NextSpell + 1, PhoenixAA)#Applying AA
    Player.EffectCDList.append(SummonDOTCheck)
    Player.SummonDOTTimer = 15

def ApplyEnkindle(Player, Enemy):
    Player.Enkindle = False
    Player.Pet.TrueLock = False
    Player.Pet.ActionSet.insert(Player.Pet.NextSpell + 1, EnkindleSummon)

def ApplyDeathflare(Player, Enemy):
    Player.Deathflare = False

def ApplyEnergyDrain(Player, Enemy):
    Player.AetherflowGauge = 2
    Player.AetherflowCD = 60
    Player.FurtherRuin = True

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
        Player.DOTList.remove(Player.SlipstreamDOT)
        Player.EffectToRemove.append(SlipstreamDOTCheck)
        Player.SlipstreamDOT = None

def SummonDOTCheck(Player, Enemy):
    if Player.SummonDOTTimer <= 0:

        Player.Pet.DOTList = [] #Reseting DOTList

        Player.EffectToRemove.append(SummonDOTCheck)
        Player.FirebirdTrance = False
        Player.BahamutTrance = False
        Player.Deathflare = False

def SearingLightCheck(Player, Enemy):
    if Player.SearingLightTimer <= 0:
        Enemy.buffList.remove(SearingLightbuff)
        Player.EffectToRemove.append(SearingLightCheck)


#GCD
Ruin3 = SummonerSpell(3579, True, 1.5, 2.5, 310, 300, empty, [ManaRequirement], type = 1)
Ruin4 = SummonerSpell(7426, True, Lock, 2.5, 430, 400, ApplyRuin4, [ManaRequirement, Ruin4Requirement], type = 1)
FoF = SummonerSpell(16514, True, Lock, 2.5, 540, 300, empty, [FoFRequirement, ManaRequirement], type = 1)
AstralImpulse = SummonerSpell(25820, True, Lock, 2.5, 440, 300, empty, [AstralImpulseRequirement, ManaRequirement], type = 1)
TryDisaster = SummonerSpell(25826, True, 1.5, 2.5, 120, 300, empty, [ManaRequirement], type = 1)
#Primal
Titan = SummonerSpell(25839, True, Lock, 2.5, 750, 0, ApplyTitan, [TitanRequirement], type = 1)
Garuda = SummonerSpell(25840, True, Lock, 2.5, 750, 0, ApplyGaruda, [GarudaRequirement], type = 1)
Ifrit = SummonerSpell(25838, True, Lock, 2.5, 750, 0, ApplyIfrit, [IfritRequirement], type = 1)

#Titan Ability
Topaz = SummonerSpell(25824, True, Lock, 2.5, 330, 0, ApplyTopaz, [ManaRequirement, TopazRequirement], type = 1)
Mountain = SummonerSpell(25836, False, Lock, 0, 150, 0, ApplyMountain, [MountainRequirement])
TopazCatastrophe = SummonerSpell(25833, True, 0, 2.5, 140, 300, ApplyTopaz, [ManaRequirement, TopazRequirement] , type = 1) #same effect and requirement as Topaz

#IfritAbility
Ruby = SummonerSpell(25823, True, 2.8, 3, 510, 300, ApplyRuby, [RubyRequirement, ManaRequirement] , type = 1)
Cyclone = SummonerSpell(25835, True, Lock, 2.5, 430, 0, ApplyCyclone, [CycloneRequirement], type = 1)
Strike = SummonerSpell(25885, True, Lock, 2.5, 430, 0, ApplyStrike, [StrikeRequirement], type = 1)
RubyCatastrophe = SummonerSpell(25832, True, 2.8, 2.5, 210, 300, ApplyRuby, [RubyRequirement, ManaRequirement], type = 1) #Same as Ruby
#GarudaAbility
Emerald = SummonerSpell(25825, True, Lock, 1.5, 230, 300, ApplyEmerald, [EmeraldRequirement, ManaRequirement], type = 1)
EmeraldCatastrophe = SummonerSpell(25834, True, 0, 1.5, 100, 300, ApplyEmerald, [ManaRequirement, EmeraldRequirement], type = 1)
Slipstream = SummonerSpell(25837, True, 3, 3.5, 430, 0, ApplySlipstream, [SlipstreamRequirement], type = 1)
SlipstreamDOT = DOTSpell(-13, 30, False)

#Summon
Summon = SummonerSpell(7427, True, Lock, 2.5, 0, 0, ApplySummon, [SummonRequirement], type = 1)
#Bahamut and Phoenix damage will simply be a dot
BahamutAA = SummonerSpell(115, False, 0, 0, 0, 0, ApplyBahamutAA, [])
PhoenixAA = SummonerSpell(115, False, 0, 0, 0, 0, ApplyPhoenixAA, [])
BahamutDOT = DOTSpell(-14, 180, False) #AA of bahamut and phoenix
PhoenixDOT = DOTSpell(-15, 240, False)
EnkindleSummon = SummonerSpell(17, False, 0, 0, 1300, 0, empty, []) #Enkindle done by pet
#autos of summon seems to be faster if uses Enkindle, but always max 5

#oGCD
Enkindle = SummonerSpell(7429, False, 0, 0, 0, 0, ApplyEnkindle, [EnkindleRequirement]) #Smaller lock since executed by pet, might have to reconsider... >.>
Deathflare = SummonerSpell(3582, False, Lock, 0, 500, 0, ApplyDeathflare, [DeathflareRequirement])
EnergyDrainSMN = SummonerSpell(16508, False, Lock, 0, 200, 0, ApplyEnergyDrain, [EnergyDrainRequirement])
Fester = SummonerSpell(181, False, Lock, 0, 340, 0, ApplyFester, [FesterRequirement])
PainFlare = SummonerSpell(3578, False, 0, 0, 150, 0, ApplyFester, [FesterRequirement]) #AOE version of Fester
SearingLight = SummonerSpell(25801, False, Lock, 0, 0, 0, ApplySearingLight, [SearingLightRequirement])
PhysickSMN = SummonerSpell(16230, True, 1.5, 2.5, 0, 0, empty, [ManaRequirement])
Resurrection = SummonerSpell(173, True, 8, 2.5, 0, 2400, empty, [ManaRequirement])
#buff
SearingLightbuff = buff(1.03)

SummonerAbility = {
3579 : Ruin3,
7426 : Ruin4,
25826 : TryDisaster,
25801 : SearingLight,
#25789 : Carbunle,
7427 : Summon, #Bahamut
25820 : AstralImpulse,
25821 : AstralImpulse, #Astral Flare
3582 : Deathflare,
7429 : Enkindle, #Enkindle Bahamut
#7428 : Wyrmwave, #Bahamut Autos
25831 : Summon, #Summon Phoenix
16514 : FoF, #Fountain Of Fire
16515 : FoF, #AOE of FoF
16516 : Enkindle, #Phoenix Enkindle
#16519 : ScarletFlame, #Pheonix AA
25838 : Ifrit,
25823 : Ruby,
25832 : RubyCatastrophe,
25835 : Cyclone,
25885 : Strike,
25839 : Titan,
25824 : Topaz,
25833 : TopazCatastrophe,
25836 : Mountain,
25840 : Garuda,
25825 : Emerald,
25834 : EmeraldCatastrophe,
25837 : Slipstream,
16508 : EnergyDrainSMN,
16510 : EnergyDrainSMN, #Energy Syphon
181 : Fester,
3578 : PainFlare,
#25799 : RadiantAegis,
16230 : PhysickSMN,
173 : Resurrection
}