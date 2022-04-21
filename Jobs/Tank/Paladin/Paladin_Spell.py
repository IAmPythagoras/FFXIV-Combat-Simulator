from Jobs.Base_Spell import empty, DOTSpell, ManaRequirement
from Jobs.Tank.Paladin.Paladin_Player import Paladin
from Jobs.Tank.Tank_Spell import PaladinSpell
import copy
Lock = 0.75


#Requirement

def FightOrFlightRequirement(Player, Spell):
    return Player.FightOrFlightCD <= 0

def ExpiacionRequirement(Player, Spell):
    return Player.ExpiacionCD <= 0

def InterveneRequirement(Player, Spell):
    return Player.InterveneStack > 0

def AtonementRequirement(Player, Spell):
    return Player.SwordOathStack > 0

def CircleScornRequirement(Player, Spell):
    return Player.CircleScornCD <= 0

def BladeFaithRequirement(Player, Spell):
    return Player.BladeFaith

def BladeTruthRequirement(Player, Spell):
    return Player.BladeTruth

def BladeValorRequirement(Player, Spell):
    return Player.BladeValor

def ConfettiRequirement(Player, Spell):
    return Player.RequestACat

def RequestACatRequirement(Player, Spell):
    return Player.RequestACatCD <= 0

#Apply

def ApplyFightOrFlight(Player, Enemy):
    Player.FightOrFlightTimer = 25
    Player.FightOrFlightCD = 60
    Player.MultDPSBonus *= 1.25
    Player.EffectCDList.append(FightOrFlightCheck)

def ApplyExpiacion(Player, Enemy):
    Player.Mana += 10000 #Will have to double check that lol >.>
    Player.ExpacionCD = 30

def ApplyIntervene(Player, Enemy):
    if Player.InterveneStack == 2:
        Player.EffectCDList.append(InterveneStackCheck)
        Player.InterveneCD = 30
    Player.InterveneStack -= 1

def ApplyAtonement(Player, Enemy):
    Player.SwordOathStack -= 1

def ApplyCircleScorn(Player, Enemy):
    #Since DOT has 30 sec CD and 15 sec duration, we don't have to check
    Player.CircleScornDOT = copy.deepcopy(CircleScornDOT)
    Player.DOTList.append(Player.CircleScornDOT)
    Player.CircleScornTimer = 15
    Player.EffectCDList.append(CircleScornDOTCheck)

def ApplyFastBlade(Player, Enemy):
    if not (FastBladeCombo in Player.EffectList) : Player.EffectList.append(FastBladeCombo)

def ApplyRequestACat(Player, Enemy):
    Player.RequestACatCD = 60
    Player.RequestACat = True
    Player.RequestACatStack = 5
    Player.EffectList.append(RequestACatEffect)

def ApplyBladeFaith(Player, Enemy):
    Player.BladeFaith = False
    Player.BladeTruth = True

def ApplyBladeTruth(Player, Enemy):
    Player.BladeTruth = False
    Player.BladeValor = True

def ApplyBladeValor(Player, Enemy):
    Player.BladeValor = False

def ApplyConfetti(Player, Enemy):
    Player.RequestACatStack = 0
    Player.RequestACatStack = False
    Player.EffectList.remove(RequestACatEffect)
    Player.BladeFaith = True

#Effect

def RequestACatEffect(Player, Spell):
    if Spell.id == HolySpirit.id:
        Spell.Potency += 270
        Player.RequestACatStack -= 1

        if Player.RequestACatStack == 0:
            Player.RequestACat = False
            Player.EffectList.remove(RequestACatEffect)
            Player.BladeFaith = True


#Combo Action

def FastBladeCombo(Player, Spell):
    if Spell.id == RiotBlade.id:
        Spell.Potency += 130
        Player.EffectList.remove(FastBladeCombo)
        Player.EffectList.append(RiotBladeCombo)

def RiotBladeCombo(Player, Spell):
    if Spell.id == RoyalAuthority.id:
        Spell.Potency += 290
        Player.SwordOathStack += 3
        Player.EffectList.remove(RiotBladeCombo)
    elif Spell.id == GoringBlade.id:
        #Apply dot
        if Player.GoringDOT != None:
            Player.GoringDOT = copy.deepcopy(GoringDOT)
            Player.EffectCDList.append(GoringDOTCheck)
            Player.DOTList.append(Player.GoringDOT)
        Player.GoringDOTTimer = 21
        Player.EffectList.remove(RiotBladeCombo)
        Spell.Potency += 150


#Check

def FightOrFlightCheck(Player, Enemy):
    if Player.FightOrFlighTimer <= 0:
        Player.MultDPSBonus /= 1.25
        Player.EffectCDList.remove(FightOrFlightCheck)

def InterveneStackCheck(Player, Enemy):
    if Player.InterveneCD <= 0:
        if Player.InterveneStack == 1:
            Player.EffectCDList.remove(InterveneStackCheck)
        else:
            Player.InterveneCD = 30
        Player.InterveneStack += 1

def CircleScornDOTCheck(Player, Enemy):
    if Player.CircleScornTimer <= 0:
        Player.DOTList.remove(Player.CircleScornDOT)
        Player.CircleScornDOT = None
        Player.EffectCDList.remove(CircleScornDOTCheck)

def GoringDOTCheck(Player, Enemy):
    if Player.GoringDOTTimer <= 0:
        Player.DOTList.remove(Player.GoringDOT)
        Player.EffectCDList.remove(GoringDOTCheck)
        Player.GoringDOT = None



#Combo action

FastBlade = PaladinSpell(1, True, Lock, 2.5, 200, 0, ApplyFastBlade, [])
RiotBlade = PaladinSpell(2, True, Lock, 2.5, 170, 0, empty, [])
RoyalAuthority = PaladinSpell(3, True, Lock, 2.5, 130,0, empty, [])
GoringBlade = PaladinSpell(4, True, Lock, 2.5, 100, 0, empty, [])
GoringDOT = DOTSpell(-5, 65)

#Confiteor Combo Action

Confetti = PaladinSpell(5, True, Lock, 2.5, 900, 1000, ApplyConfetti, [ManaRequirement, ConfettiRequirement]) # >.>
BladeFaith = PaladinSpell(8, True, Lock, 2.5, 420, 0, ApplyBladeFaith, [BladeFaithRequirement])
BladeTruth = PaladinSpell(9, True, Lock, 2.5, 500, 0, ApplyBladeTruth, [BladeTruthRequirement])
BladeValor = PaladinSpell(10, True, Lock, 2.5, 580, 0, ApplyBladeValor, [BladeValorRequirement])
#GCD
HolySpirit = PaladinSpell(7, True, 1.5, 2.5, 270, 1000, empty, [ManaRequirement])
Atonement = PaladinSpell(12, True, Lock, 2.5, 420, 0, ApplyAtonement, [AtonementRequirement])

#oGCD
RequestACat = PaladinSpell(6, False, 0, Lock, 400, 0, ApplyRequestACat, [RequestACatRequirement]) #I NEED ONE RIGHT NOW :x
CircleScorn = PaladinSpell(11, False, 0, Lock, 100, 0, ApplyCircleScorn, [CircleScornRequirement])
CircleScornDOT = DOTSpell(-6, 30)
Intervene = PaladinSpell(13, False, 0, Lock, 150, 0, ApplyIntervene, [InterveneRequirement])
Expiacion = PaladinSpell(14, False, 0, Lock, 340, 0, ApplyExpiacion, [ExpiacionRequirement])
FightOrFlight = PaladinSpell(15, False, 0, Lock, 0, 0, ApplyFightOrFlight, [FightOrFlightRequirement])