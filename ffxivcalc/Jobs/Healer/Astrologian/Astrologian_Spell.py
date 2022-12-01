import copy

from ffxivcalc.Jobs.Base_Spell import DOTSpell, ManaRequirement, buff, empty
from ffxivcalc.Jobs.Healer.Healer_Spell import AstrologianSpell
Lock = 0

#Requirement

def DrawRequirement(Player, Spell):
    return Player.DrawStack > 0, Player.DrawCD

def RedrawRequirement(Player, Spell):
    return Player.Redraw, -1

def ArcanumRequirement(Player, Spell):
    return Player.HasCard, -1

def MinorArcanaRequirement(Player, Spell):
    return Player.MinorArcanaCD <= 0, Player.MinorArcanaCD

def LordOfCrownRequirement(Player, Spell):
    return Player.LordOfCrown, -1 #Will be assumed to be given by Minor Arcana

def DivinationRequirement(Player, Spell):
    return Player.DivinationCD <= 0, Player.DivinationCD

def LightspeedRequirement(Player, Spell):
    return Player.LightspeedCD <= 0, Player.LightspeedCD

def MacrocosmosRequirement(Player, Spell):
    return Player.MacrocosmosCD <= 0, Player.MacrocosmosCD

def MicrocosmosRequirement(Player, Spell):
    return Player.MacrocosmosCD > 165, -1 #Since Micro is only available after 15 sec

def ExaltationRequirement(Player, Spell):
    return Player.ExaltationCD <= 0, Player.ExaltationCD

def NeutralSectRequirement(Player, Spell):
    return Player.NeutralSectCD <= 0, Player.NeutralSectCD

def HoroscopeRequirement(Player, Spell):
    return Player.HoroscopeCD <= 0, Player.HoroscopeCD

def CelestialIntersectionRequirement(Player, Spell):
    return Player.CelestialIntersectionStack > 0, Player.CelestialIntersectionCD

def EarthlyStarRequirement(Player, Spell):
    return Player.EarthlyStarCD <= 0, Player.EarthlyStarCD

def StellarDetonationRequirement(Player, Spell):
    if Player.EarthlyStarCD > 50 : Spell.Potency = 205 #Changes potency with respect to how long the player has waited since doing EarthlyStar
    elif Player.EarthlyStarCD <= 50 and Player.EarthlyStarCD >= 40 : Spell.Potency = 310
    return Player.EarthlyStarCD > 40

def CelestialOppositionRequirement(Player, Spell):
    return Player.CelestialOppositionCD <= 0, Player.CelestialOppositionCD

def CollectiveRequirement(Player, Spell):
    return Player.CollectiveCD <= 0, Player.CollectiveCD

def SynastryRequirement(Player, Spell):
    return Player.SynastryCD <= 0, Player.SynastryCD

def EssentialDignityRequirement(Player, Spell):
    return Player.EssentialDignityStack >0, Player.EssentialDignityCD

#Apply

def ApplyEssentialDignity(Player, Enemy):
    if Player.EssentialDignityStack == 2:
        Player.EffectCDList.append(EssentialDignityStackCheck)
        Player.EssentialDignityCD = 40
    Player.EssentialDignityStack -= 1

def ApplySynastry(Player, Enemy):
    Player.SynastryCD = 120

def ApplyCollective(Player, Enemy):
    Player.CollectiveCD = 60

def ApplyCelestialOpposition(Player, Enemy):
    Player.CelestialOppositionCD = 60

def ApplyEarthlyStar(Player, Enemy):
    Player.EarthlyStarCD = 60

def ApplyCelestialIntersection(Player, Enemy):

    if Player.CelestialIntersectionStack == 2:
        Player.EffectCDList.append(CelestialIntersectionStackCheck)
        Player.CelestialIntersectionCD = 30
    
    Player.CelestialIntersectionStack -= 1


def ApplyHoroscope(Player, Enemy):
    Player.HoroscopeCD = 60

def ApplyNeutralSect(Player, Enemy):
    Player.NeutralSectCD = 120

def ApplyExaltation(Player, Enemy):
    Player.ExaltationCD = 60

def ApplyMacrocosmos(Player, Enemy):
    Player.MacrocosmosCD = 180

def ApplyAstrodyne(Player, Enemy):
    check = 0

    if Player.Lunar:
        check +=1
        Player.Lunar = False
    if Player.Solar:
        check +=1
        Player.Solar = False
    if Player.Celestial:
        check +=1
        Player.Celestial = False
    #Will only consider Body and Mind
    if check >= 2:
        Player.EffectList.append(BodyEffect)
        Player.EffectCDList.append(BodyCheck)#Only 1 check for both Body and Mind since same Timer
        Player.BodyTimer = 15
    if check == 3:
        Player.buffList.append(AstrodyneBuff)
        Player.EffectCDList.append(MindCheck)


def ApplyDraw(Player, Enemy):
    Player.HasCard = True
    Player.Redraw = True

    if Player.DrawStack == 2:
        Player.EffectCDList.append(DrawStackCheck)
        Player.DrawCD = 30
    Player.DrawStack -= 1

def ApplyRedraw(Player, Enemy):
    Player.Redraw = False

def ApplyMinorArcana(Player, Enemy):
    Player.LordOfCrown = True
    Player.MinorArcanaCD = 60

def ApplyLordOfCrown(Player, Enemy):
    Player.LordOfCrown = False

def ApplyDivination(Player, Enemy):
    Enemy.buffList.append(DivinatonBuff) #Just give DPS bonus on Enemy instead of raid wide buff
    Player.DivinationCD = 120
    Player.DivinationTimer = 15
    Player.EffectCDList.append(DivinationCheck)

def ApplyLightspeed(Player, Enemy):
    Player.LightspeedTimer = 15
    Player.LightspeedCD = 90
    Player.EffectList.append(LightspeedEffect)
    Player.EffectCDList.append(LightspeedCheck)

def ApplyCombust(Player, Enemy):
    if Player.CumbustDOT == None:
        Player.CumbustDOT = copy.deepcopy(CumbustDOT)
        Player.CumbustDOTTimer = 30
        Player.DOTList.append(Player.CumbustDOT)
        Player.EffectCDList.append(CumbustDOTCheck)
    Player.CumbustTimer = 30

#Effect

def BodyEffect(Player, Spell):
    if Spell.id == Malefic.id or Spell.id == Combust.id : #Only two affected spells for now
        Spell.CastTime *= 0.9
        Spell.RecastTime *= 0.9

def LightspeedEffect(Player, Spell):
    if Spell.GCD: Spell.CastTime = max(Lock, Spell.CastTime - 2.5)

#Check

def EssentialDignityStackCheck(Player, Enemy):
    if Player.EssentialDignityCD <= 0:
        if Player.EssentialDignityStack == 1:
            Player.EffectToRemove.append(EssentialDignityStackCheck)
        else:
            Player.EssentialDignityCD = 40
        Player.EssentialDignityStack += 1

def BodyCheck(Player, Enemy):
    if Player.BodyTimer <= 0:
        Player.EffectList.remove(BodyEffect)
        Player.EffectToRemove.append(BodyCheck)

def MindCheck(Player, Enemy):
    if Player.BodyTimer <= 0:
        Player.buffList.remove(AstrodyneBuff)
        Player.EffectToRemove.append(MindCheck)

def DrawStackCheck(Player, Enemy):
    if Player.DrawCD <= 0:
        if Player.DrawStack == 1:
            Player.EffectToRemove.append(DrawStackCheck)
        else:
            Player.DrawCD = 30
        Player.DrawStack += 1

def DivinationCheck(Player, Enemy):
    if Player.DivinationTimer <= 0:
        Enemy.buffList.remove(DivinatonBuff)
        Player.EffectToRemove.append(DivinationCheck)

def LightspeedCheck(Player, Enemy):
    if Player.LightspeedTimer <= 0:
        Player.EffectList.remove(LightspeedEffect)
        Player.EffectToRemove.append(LightspeedCheck)


def CumbustDOTCheck(Player, Enemy):
    if Player.CumbustDOTTimer <= 0:
        Player.DOTList.remove(Player.CumbustDOT)
        Player.CumbustDOT = None
        Player.EffectToRemove.append(CumbustDOTCheck)

def CelestialIntersectionStackCheck(Player, Enemy):
    if Player.CelestialIntersectionCD <= 0:
        if Player.CelestialIntersectionStack == 1:
            Player.EffectToRemove.append(CelestialIntersectionStackCheck)
        else:
            Player.CelestialIntersectionCD = 30
        Player.CelestialIntersectionStack += 1

#GCD
Malefic = AstrologianSpell(25871, True, 1.5, 2.5, 250, 400, empty, [ManaRequirement], type = 1)
Combust = AstrologianSpell(16554, True, Lock, 2.5, 0, 400, ApplyCombust, [ManaRequirement], type = 1)
LordOfCrown = AstrologianSpell(7444, True, Lock, 1, 250, 0,  ApplyLordOfCrown, [LordOfCrownRequirement], type = 1)
CumbustDOT = DOTSpell(-12, 55, False)
Gravity = AstrologianSpell(25872, True, 1.5, 2.5, 130, 400, empty, [ManaRequirement], type = 1)
#Heal GCD
AspectedHelios = AstrologianSpell(3601, True, 1.5, 2.5, 0, 800, empty, [ManaRequirement], type = 1)
AspectedBenific = AstrologianSpell(2595, True, 0, 2.5, 0, 400, empty, [ManaRequirement], type = 1)
Benefic2 = AstrologianSpell(3610, True, 1.5, 2.5, 0, 700, empty, [ManaRequirement], type = 1)
Benefic = AstrologianSpell(3594, True, 1.5, 2.5, 0, 400, empty, [ManaRequirement], type = 1)
Helios = AstrologianSpell(3600, True, 1.5, 2.5, 0, 700, empty, [ManaRequirement], type = 1)
EssentialDignity = AstrologianSpell(10, False, 0, 0, 0, 0, ApplyEssentialDignity, [EssentialDignityRequirement, type = 1])
Macrocosmos = AstrologianSpell(25874, True, 0, 0, 250, 600, ApplyMacrocosmos, [MacrocosmosRequirement, ManaRequirement], type = 1)
Microcosmos = AstrologianSpell(17, True, 0, 0, 0, 0, empty, [MicrocosmosRequirement], type = 1)
LadyOfCrown = AstrologianSpell(7445, True, 0, 1, 0, 0, empty, [], type = 1)
#oGCD
Lightspeed = AstrologianSpell(11, False, Lock, 0, 0, 0, ApplyLightspeed, [LightspeedRequirement])
Divination = AstrologianSpell(16552, False, Lock, 0, 0, 0, ApplyDivination, [DivinationRequirement])
MinorArcana = AstrologianSpell(7443, False, Lock, 0, 0, 0, ApplyMinorArcana, [MinorArcanaRequirement])
Draw = AstrologianSpell(3590, False, Lock,0, 0, 0, ApplyDraw, [DrawRequirement])
Redraw = AstrologianSpell(3593, False, Lock, 0, 0, 0, ApplyRedraw, [RedrawRequirement])
Astrodyne = AstrologianSpell(25870, False, Lock, 0, 0, 0, ApplyAstrodyne, [])
#Heal oGCD
Exaltation = AstrologianSpell(18, False, 0, 0, 0, 0, ApplyExaltation, [ExaltationRequirement])
NeutralSect = AstrologianSpell(16559, False, 0, 0, 0, 0, ApplyNeutralSect, [NeutralSectRequirement])
Horoscope = AstrologianSpell(16557, False, 0, 0, 0, 0, ApplyHoroscope, [HoroscopeRequirement])
CelestialIntersection = AstrologianSpell(16556, False, 0, 0, 0, 0, ApplyCelestialIntersection, [CelestialIntersectionRequirement])
EarthlyStar = AstrologianSpell(7439, False, 0, 0, 0, 0, ApplyEarthlyStar, [EarthlyStarRequirement])
StellarDetonation = AstrologianSpell(23, False, 0, 0, 0, 0, empty, [StellarDetonationRequirement])
CelestialOpposition = AstrologianSpell(16553, False, 0, 0, 0, 0, ApplyCelestialOpposition, [CelestialOppositionRequirement])
Collective = AstrologianSpell(3613, False, 0, 0, 0, 0, ApplyCollective, [CollectiveRequirement])
Synastry = AstrologianSpell(3612, False, 0, 0, 0, 0, ApplySynastry, [SynastryRequirement])

#Arcanum require a target within the team, so it will be a function that will return a spell that
#will target the given player. It is also assumed that the bonus is 6%
ArcanumBuff = buff(1.06)
AstrodyneBuff = buff(1.05)
DivinatonBuff = buff(1.06)


def Arcanum(Target, Type):
    #Target is the player object to which we will apply the buff
    #Type will specify which Astrosign

    def ArcanumCheck(Player, Enemy):
        if Player.ArcanumTimer <= 0:
            #input("Effect has been removed on : " + str(Player))
            Player.EffectToRemove.append(ArcanumCheck)
            Player.buffList.remove(ArcanumBuff)
        pass #This function is just to know if the Target has already been given a buff

    def ApplyArcanum(Player, Spell):
        Player.HasCard = False
        if Target.ArcanumTimer == 0 : #Can only have 1 buff at a time
            Target.buffList.append(ArcanumBuff)
            Target.EffectCDList.append(ArcanumCheck)

        Target.ArcanumTimer = 15

        if Type == "Lunar" : Player.Lunar = True
        elif Type == "Solar" : Player.Solar = True
        elif Type == "Celestial" : Player.Celestial = True

    ArcanumSpell = AstrologianSpell(0, False, Lock, 0, 0, 0, ApplyArcanum, [ArcanumRequirement])
    ArcanumSpell.TargetID = Target.playerID 
    return ArcanumSpell

def LunarArcanum(target):
    returnSpell = Arcanum(target,"Lunar")
    returnSpell.id = 4402
    return returnSpell

def SolarArcanum(target):
    returnSpell = Arcanum(target,"Solar")
    returnSpell.id = 4401
    return returnSpell

def CelestialArcanum(target):
    returnSpell = Arcanum(target,"Celestial")
    returnSpell.id = 4403
    return returnSpell

AstrologianAbility = {
25871 : Malefic,
16554 : Combust,
25872 : Gravity,
3590 : Draw,
3593 : Redraw, 
7443 : MinorArcana,
4401 : SolarArcanum,
4404 : SolarArcanum,
4402 : LunarArcanum,
4405 : LunarArcanum,
4403 : CelestialArcanum,
4406 : CelestialArcanum,
7444 : LordOfCrown,
7445 : LadyOfCrown,
25870 : Astrodyne,
16552 : Divination,
16559 : NeutralSect,
7439 : EarthlyStar,
3594 : Benefic,
3610 : Benefic2,
2595 : AspectedBenific,
3600 : Helios,
3601 : AspectedHelios,
3612 : Synastry,
3613 : Collective,
16553 : CelestialOpposition,
16556 : CelestialIntersection,
16557 : Horoscope,
25873 : Exaltation,
25874 : Macrocosmos
}