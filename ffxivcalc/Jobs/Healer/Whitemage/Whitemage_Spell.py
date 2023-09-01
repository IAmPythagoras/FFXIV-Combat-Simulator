#########################################
########## WHITEMAGE PLAYER #############
#########################################
from ffxivcalc.Jobs.Base_Spell import DOTSpell, empty, ManaRequirement
from ffxivcalc.Jobs.Healer.Healer_Spell import WhitemageSpell
import copy

#Requirement

def PresenceOfMindRequirement(Player, Spell):
    return Player.PresenceOfMindCD <= 0, Player.PresenceOfMindCD

def AssizeRequirement(Player, Spell):
    return Player.AssizeCD <= 0, Player.AssizeCD

def ThinAirRequirement(Player, Spell):
    return Player.ThinAirCD <= 0, Player.ThinAirCD

def BellRequirement(Player, Spell):
    return Player.BellCD <= 0, Player.BellCD

def AquaveilRequirement(Player, Spell):
    return Player.AquaveilCD <= 0, Player.AquaveilCD

def TemperanceRequirement(Player, Spell):
    return Player.TemperanceCD <= 0, Player.TemperanceCD

def PlenaryIndulgenceRequirement(Player, Spell):
    return Player.PlenaryIndulgenceCD <= 0, Player.PlenaryIndulgenceCD

def DivineBenisonRequirement(Player, Spell):
    return Player.DivineBenisonCD <= 0, Player.DivineBenisonCD

def TetragrammatonRequirement(Player, Spell):
    return Player.TetragrammatonCD <= 0, Player.TetragrammatonCD

def BenedictionRequirement(Player, Spell):
    return Player.BenedictionCD <= 0, Player.BenedictionCD

def AsylumRequirement(Player, Spell):
    return Player.AsylumCD <= 0, Player.AsylumCD

def BloodLilyRequirement(Player, Spell):
    return Player.LilyStack > 0, Player.LilyTimer

def BloomLilyRequirement(Player, Spell):
    return Player.BloomLily, -1



#Apply

def ApplyAfflatusMisery(Player, Enemy):
    Player.BloomLily = False
    Player.UsedLily = 0 #Reset counter

def ApplyLily(Player, Enemy):
    if not Player.BloomLily : Player.UsedLily = min(3, Player.UsedLily + 1)
    Player.LilyStack -= 1

    if Player.UsedLily == 3: Player.BloomLily = True

def Apply(Player, Enemy):
    Player.CD = 0

def ApplyBell(Player, Enemy):
    Player.BellCD = 180

def ApplyAquaveil(Player, Enemy):
    Player.AquaveilCD = 60

def ApplyTemperance(Player, Enemy):
    Player.TemperanceCD = 120

def ApplyPlenaryIndulgence(Player, Enemy):
    Player.PlenaryIndulgenceCD = 60

def ApplyDivineBenison(Player, Enemy):
    Player.DivineBenisonCD = 30

def ApplyTetragrammaton(Player, Enemy):
    Player.TetragrammatonCD = 60

def ApplyAsylum(Player, Enemy):
    Player.AsylumCD = 90

def ApplyBenediction(Player, Enemy):
    Player.BenedictionCD = 180

def ApplyDia(Player, Enemy):
    Player.DiaTimer = 30

    if (Player.Dia == None) : 
        Player.Dia = copy.deepcopy(DiaDOT)
        Player.EffectCDList.append(CheckDia)
        Player.DOTList.append(Player.Dia)

def ApplyAssize(Player, Enemy):
    Player.Mana = min(10000, Player.Mana + 500)
    Player.AssizeCD = 40

def ApplyThinAir(Player, Enemy):
    Player.ThinAirCD = 60
    Player.EffectList.append(ThinAirEffect)

def ApplyPresenceOfMind(Player, Enemy):
    Player.PresenceOfMindCD = 120
    Player.PresenceOfMindTimer = 15
    Player.EffectList.append(PresenceOfMindEffect)
    Player.Haste += 20
    Player.EffectCDList.append(CheckPresenceOfMind)

#Effect

def ThinAirEffect(Player, Spell):
    Spell.ManaCost = 0
    Player.EffectList.remove(ThinAirEffect)

def PresenceOfMindEffect(Player, Spell):
    pass
    #Spell.CastTime *= 0.8
    #Spell.RecastTime *= 0.8

#Check

def CheckDia(Player, Enemy):
    if Player.DiaTimer <= 0:
        Player.DOTList.remove(Player.Dia)
        Player.Dia = None
        Player.EffectToRemove.append(CheckDia)

def CheckPresenceOfMind(Player, Enemy):
    if Player.PresenceOfMindTimer <= 0:
        Player.EffectList.remove(PresenceOfMindEffect)
        Player.Haste -= 20
        Player.EffectToRemove.append(CheckPresenceOfMind)



#Damage GCD
Glare = WhitemageSpell(25859, True, 1.5, 2.5, 310, 400, empty, [ManaRequirement], type = 1)
Dia = WhitemageSpell(16532, True, 0, 2.5, 60, 400, ApplyDia, [ManaRequirement], type = 1)
DiaDOT = DOTSpell(-5, 60, False)
AfflatusMisery = WhitemageSpell(16535, True, 0, 2.5, 1240, 0, ApplyAfflatusMisery, [BloomLilyRequirement], type = 1)
Holy = WhitemageSpell(25860, True, 2.5, 2.5, 150, 400, empty, [ManaRequirement], type = 1)
#Healing GCD
AfflatusRapture = WhitemageSpell(16534, True, 0, 2.5, 0, 0, ApplyLily, [BloodLilyRequirement], type = 1)
AfflatusSolace = WhitemageSpell(16531, True, 0, 0, 0, 0, ApplyLily, [BloodLilyRequirement], type = 1)
Regen = WhitemageSpell(137, True, 0, 2.5, 0, 400, empty, [ManaRequirement], type = 1)
Cure = WhitemageSpell(120, True, 1.5, 2.5, 0, 400, empty, [ManaRequirement], type = 1)
Cure2 = WhitemageSpell(135, True, 2, 2.5, 0, 1000, empty, [ManaRequirement], type = 1)
Cure3 = WhitemageSpell(131, True, 2, 2.5, 0, 1500, empty, [ManaRequirement], type = 1)
Medica = WhitemageSpell(124, True, 2, 2.5, 0, 900, empty, [ManaRequirement], type = 1)
Medica2 = WhitemageSpell(133, True, 2, 2.5, 0, 1000, empty, [ManaRequirement], type = 1)
Raise = WhitemageSpell(125, True, 8, 2.5, 0, 2400, empty, [ManaRequirement])

#Damage oGCD
Assize = WhitemageSpell(3571, False, 0, 0, 400, 0, ApplyAssize, [AssizeRequirement])
ThinAir = WhitemageSpell(7430, False, 0, 0, 0, 0, ApplyThinAir, [ThinAirRequirement])
PresenceOfMind = WhitemageSpell(136, False, 0, 0, 0, 0, ApplyPresenceOfMind, [PresenceOfMindRequirement])

#Healing oGCD
Bell = WhitemageSpell(25862, False, 0, 0, 0, 0, ApplyBell, [BellRequirement]) #Litturgy of the bell
Aquaveil = WhitemageSpell(25861, False, 0, 0, 0, 0, ApplyAquaveil, [AquaveilRequirement])
Temperance = WhitemageSpell(16536, False, 0, 0, 0, 0, ApplyTemperance, [TemperanceRequirement])
PlenaryIndulgence = WhitemageSpell(19, False, 0, 0, 0, 0, ApplyPlenaryIndulgence, [PlenaryIndulgenceRequirement])
DivineBenison =WhitemageSpell(7432, False, 0, 0, 0, 0, ApplyDivineBenison, [DivineBenisonRequirement])
Tetragrammaton = WhitemageSpell(3570, False, 0, 0, 0, 0, ApplyTetragrammaton, [TetragrammatonRequirement])
Asylum = WhitemageSpell(3569, False, 0, 0, 0, 0, ApplyAsylum, [AsylumRequirement])
Benediction = WhitemageSpell(140, False, 0, 0, 0, 0, ApplyBenediction, [BenedictionRequirement])

WhiteMageAbility = {
25859 : Glare,
16532 : Dia,
25860 : Holy,
16535 : AfflatusMisery,
3571 : Assize,
120 : Cure,
135 : Cure2,
131 : Cure3,
124 : Medica,
133 : Medica2,
137 : Regen,
3570 : Tetragrammaton,
3569 : Asylum,
7432 : DivineBenison,
140 : Benediction,
16531 : AfflatusSolace,
16534 : AfflatusRapture,
136 : PresenceOfMind,
7430 : ThinAir,
16536 : Temperance,
25861 : Aquaveil,
25862 : Bell,
19 : PlenaryIndulgence,
125 : Raise
}