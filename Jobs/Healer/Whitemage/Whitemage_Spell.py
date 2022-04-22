#########################################
########## WHITEMAGE PLAYER #############
#########################################
from Jobs.Base_Spell import DOTSpell, empty, ManaRequirement
from Jobs.Healer.Healer_Spell import WhitemageSpell
import copy
Lock = 0.75

#Requirement

def PresenceOfMindRequirement(Player, Spell):
    return Player.PresenceOfMindCD <= 0

def AssizeRequirement(Player, Spell):
    return Player.AssizeCD <= 0

def ThinAirRequirement(Player, Spell):
    return Player.ThinAirCD <= 0

#Apply

def ApplyDia(Player, Enemy):
    Player.DiaTimer = 30

    if (Player.Dia == None) : 
        Player.Dia = copy.deepcopy(DiaDOT)
        Player.EffectCDList.append(CheckDia)
        Player.DOTList.append(Player.Dia)

def ApplyAssize(Player, Enemy):
    Player.Mana = min(10000, Player.Mana + 500)
    Player.AssizeCD = 45

def ApplyThinAir(Player, Enemy):
    Player.ThinAirCD = 60
    Player.EffectList.append(ThinAirEffect)

def ApplyPresenceOfMind(Player, Enemy):
    Player.PresenceOfMindCD = 120
    Player.PresenceOfMindTimer = 15
    Player.EffectList.append(PresenceOfMindEffect)
    Player.EffectCDList.append(CheckPresenceOfMind)

#Effect

def ThinAirEffect(Player, Spell):
    Spell.ManaCost = 0
    Player.EffectList.remove(ThinAirEffect)

def PresenceOfMindEffect(Player, Spell):
    Spell.CastTime *= 0.8
    Spell.RecastTime *= 0.8

#Check

def CheckDia(Player, Enemy):
    if Player.DiaTimer <= 0:
        Player.DOTList.remove(Player.Dia)
        Player.Dia = None
        Player.EffectToRemove.append(CheckDia)

def CheckPresenceOfMind(Player, Enemy):
    if Player.PresenceOfMindTimer <= 0:
        Player.EffectList.remove(PresenceOfMindEffect)
        Player.EffectToRemove.append(CheckPresenceOfMind)



#GCD
Glare = WhitemageSpell(0, True, 1.5, 2.5, 310, 400, empty, [ManaRequirement])
Dia = WhitemageSpell(1, True, Lock, 2.5, 0, 400, ApplyDia, [ManaRequirement])
DiaDOT = DOTSpell(5, 60)

#OGCD
Assize = WhitemageSpell(2, False, Lock, Lock, 400, 0, ApplyAssize, [AssizeRequirement])
ThinAir = WhitemageSpell(3, False, Lock, Lock, 0, 0, ApplyThinAir, [ThinAirRequirement])
PresenceOfMind = WhitemageSpell(4, False, Lock, Lock, 0, 0, ApplyPresenceOfMind, [PresenceOfMindRequirement])