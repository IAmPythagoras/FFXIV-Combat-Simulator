from doctest import FAIL_FAST
from Jobs.Base_Spell import DOTSpell, ManaRequirement, empty
from Jobs.Caster.Caster_Spell import BLMSpell, SwiftCastEffect
import copy
Lock = 0.75
#Requirement

def EnochianRequirement(Player, Spell):
    return Player.EnochianTimer > 0

def FireRequirement(Player, Spell):
    return Player.ElementalGauge > 0

def IceRequirement(Player, Spell):
    return Player.ElementalGauge < 0

def ParadoxRequirement(Player, Spell):
    return Player.Paradox

def PolyglotRequirement(Player, Spell):
    return Player.PolyglotStack > 0

def TransposeRequirement(Player, Spell):
    return Player.TransposeCD <= 0

def AmplifierRequirement(Player, Spell):
    return Player.AmplifierCD <= 0

def LeyLinesRequirement(Player, Spell):
    return Player.LeyLinesCD <= 0

def TripleCastRequirement(Player, Spell):
    return Player.TripleCastUseStack > 0

def SharpCastRequirement(Player, Spell):
    return Player.SharpCastStack > 0

def ManafrontRequirement(Player, Spell):
    return Player.ManafrontCD <= 0

#Apply

def ApplyBlizzard1(Player, Enemy):
    Player.AddIce() #Add 1 Ice

def ApplyFire1(Player, Enemy):
    Player.AddFire() #Add 1 fire
    if Player.SharpCast: #If sharpcast
        Player.Fire3Proc = True
        Player.SharpCast = False

def ApplyFire3(Player, Enemy):

    #Will check if we unlock paradox
    if Player.ElementalGauge == -3 and Player.UmbralHearts == 3:
        Player.Paradox = True

    Player.ElementalGauge = 3
    Player.EnochianTimer = 15 #Reset Timer

def ApplyBlizzard3(Player, Enemy):

    #Check if we unlock paradox
    if Player.ElementalGauge == 3: Player.Paradox = True

    Player.ElementalGauge = 3
    Player.EnochianTimer = 15 #ResetTimer

def ApplyBlizzard4(Player, Enemy):
    Player.UmbralHearts = 3

def ApplyParadox(Player, Enemy):
    Player.Paradox = False

    Player.EnochianTimer = 15 #Reset Timer

    if Player.ElementalGauge > 0:
        Player.AddFire()
        if Player.SharpCast: #If sharpcast
            Player.Fire3Proc = True
            Player.SharpCast = False
    elif Player.ElementalGauge < 0:
        Player.AddIce()

def ApplyXenoglossy(Player, Spell):
    Player.PolyglotStack -= 1

def ApplyDespair(Player, Spell):
    Player.Mana = 0 #All mana is used
    Player.EnochianTimer = 15
    Player.ElementalGauge = 3

def ApplyThunder3(Player, Spell):

    if Player.Thunder3DOT == None: #If no dot already applied
        Player.Thunder3DOT = copy.deepcopy(Thunder3DOT)
        Player.DOTList.append(Player.Thunder3DOT)
        Player.EffectCDList.append(Thunder3DOTCheck)
    Player.Thunder3DOTTimer = 30

    if Player.SharpCast: #If we have SharpCast
        Player.EffectList.append(Thunder3ProcEffect)
        Player.SharpCast = False

def ApplyTranspose(Player, Spell):
    Player.TransposeCD = 4
    #Check if we unlock paradox

    if (Player.ElementalGauge == 3) or (Player.ElementalGauge == -3 and Player.UmbralHearts == 3): Player.Paradox = True #In fire phase with 3 Astral Fire

    if Player.ElementalGauge > 0: Player.ElementalGauge = -1 #Ice
    elif Player.ElementalGauge < 0 : Player.ElementalGauge = 1 #Fire

def ApplyAmplifier(Player, Enemy):
    Player.AmplifierCD = 120
    Player.PolyglotStack = min(2, Player.PolyglotStack + 1)

def ApplyLeyLines(Player, Enemy):
    Player.LeyLinesCD = 120
    Player.LeyLinesTimer = 30

    Player.EffectList.append(LeyLinesEffect)
    Player.EffectCDList.append(LeyLinesCheck)

def ApplyTripleCast(Player, Enemy):
    #Check if we need to add stack check
    if Player.TripleCastUseStack == 2:
        Player.EffectCDList.append(TripleCastUseStackCheck)
        Player.TripleCastCD = 60
    Player.TripleCastUseStack -= 1

    if Player.TripleCastStack == 0: #If not stack of insta-cast
        Player.EffectList.append(TripleCastEffect)
        Player.EffectCDList.append(TripleCastCheck)
    Player.TripleCastStack = 3

def ApplySharpCast(Player, Enemy):
    #Check if we needto add stack check
    if Player.SharpCastStack == 2:
        Player.EffectCDList.append(SharpCastStackCheck)
        Player.SharpCastCD = 30
    Player.SharpCastStack -= 1

    Player.SharpCast = True

def ApplyManafront(Player, Enemy):
    Player.ManafrontCD = 120
    Player.Mana = min(10000, Player.Mana + 3000)

#Effect

def Fire3ProcEffect(Player, Spell):
    if Spell.id == Fire3.id:
        Spell.ManaCost = 0
        Spell.CastTime = Lock
        Player.EffectToRemove.append(Fire3ProcEffect)

def Thunder3ProcEffect(Player, Spell):
    if Spell.id == Thunder3.id:
        Spell.Potency += 350
        Spell.ManaCost = 0
        Spell.CastTime = Lock
        Player.EffectToRemove.append(Thunder3ProcEffect)

def TripleCastEffect(Player, Spell): 
    if not (SwiftCastEffect in Player.EffectList) and Spell.GCD and Spell.CastTime > Lock: #If GCD and not already insta cast, also Swift will go before
        Spell.CastTime = Lock
        Player.TripleCastStack -= 1

def LeyLinesEffect(Player, Spell):
    if Spell.GCD:
        Spell.CastTime = min(Lock, Spell.CastTime * 0.85)
        Spell.RecastTime *= 0.85

def EnochianEffect(Player, Spell):
    if Player.ElementalGauge != 0:
        #If elementalGauge is not 0
        Player.MultDPSBonus *= 1.2
        Player.EffectToRemove.append(EnochianEffect)
        Player.EffectCDList.append(EnochianEffectCheck)
        Player.Enochian = True

def ElementalEffect(Player, Spell):
    #Will affect Spell depending on fire and ice

    if isinstance(Spell, BLMSpell) and Spell.IsFire:
        #Fire Spell
        #First check if fire phase and apply Effect
        if Player.ElementalGauge > 0: #Fire Phase
            if Player.ElementalGauge == 1: Spell.Potency *= 1.4
            elif Player.ElementalGauge == 2 : Spell.Potency *= 1.6
            elif Player.ElementalGauge == 3 : Spell.Potency *= 1.8

            if (Player.UmbralHearts > 0) : #If we have UmbralHearts, then no mana cost increase
                Player.UmbralHearts -= 1
            else : Spell.ManaCost *= 2 #Double mana cost
        #Check if ice phase
        elif Player.ElementalGauge < 0 : #Ice Phase
            if Player.ElementalGauge == -1: 
                Spell.Potency *= 0.9
                Spell.ManaCost *= 0.75
            elif Player.ElementalGauge == -2 : 
                Spell.Potency *= 0.8
                Spell.ManaCost *= 0.5
            elif Player.ElementalGauge == -3 : 
                Spell.Potency *= 0.7
                Spell.ManaCost = 0
                Spell.CastTime *= 0.5

    elif isinstance(Spell, BLMSpell) and Spell.IsIce:
        #Ice Spell
        #First check if fire phase
        if Player.ElementalGauge > 0: #Fire Phase
            Spell.ManaCost = 0
            if Player.ElementalGauge == 1: Spell.Potency *= 0.9
            elif Player.ElementalGauge == 2 : Spell.Potency *= 0.8
            elif Player.ElementalGauge == 3 : 
                Spell.Potency *= 0.7
                Spell.CastTime *= 0.5
        elif Player.ElementalGauge < 0 : #Ice Phase
            if Player.ElementalGauge == -1: Spell.ManaCost *= 0.75
            elif Player.ElementalGauge == -2 : Spell.ManaCost *= 0.5
            elif Player.ElementalGauge == -3 : Spell.ManaCost = 0

    elif Spell.id == Paradox.id:
        #If we are casting Paradox

        if Player.ElementalGauge < 0 : #Ice Phase
            Spell.ManaCost = 0
            Spell.CastingTime = Lock

#Check

def EnochianEffectCheck(Player, Enemy):
    if Player.ElementalGauge == 0: #If we loose Enochian
        Player.Enochian = False
        Player.MultDPSBonus /= 1.2
        Player.EffectList.append(EnochianEffect)
        Player.EffectToRemove.append(EnochianEffectCheck)
        Player.PolyglotTimer = 30

    if Player.PolyglotTimer <= 0:
        #Add new stack
        Player.PolyglotStack = min(2, Player.PolyglotStack + 1)
        Player.PolyglotTimer = 30


def SharpCastStackCheck(Player, Enemy):
    if Player.SharpCastCD <= 0:
        if Player.SharpCastStack == 1:
            Player.EffectToRemove.append(SharpCastStackCheck)
        else:
            Player.SharpCastCD = 30
        Player.SharpCastStack += 1

def TripleCastUseStackCheck(Player, Enemy):
    if Player.TripleCastCD <= 0:
        if Player.TripleCastUseStack == 1:
            Player.EffectToRemove.append(TripleCastUseStackCheck)
        else:
            Player.TripleCastCD = 60
        Player.TripleCastUseStack += 1

def TripleCastCheck(Player, Enemy):
    if Player.TripleCastStack == 0 :
        Player.EffectList.remove(TripleCastEffect)
        Player.EffectToRemove.append(TripleCastCheck)

def LeyLinesCheck(Player, Enemy):
    if Player.LeyLinesTimer <= 0:
        Player.EffectList.remove(LeyLinesEffect)
        Player.EffectToRemove.append(LeyLinesCheck)

def Thunder3DOTCheck(Player, Enemy):
    if Player.Thunder3DOTTimer <= 0:
        Player.DOTList.remove(Player.Thunder3DOT)
        Player.Thunder3DOT = None
        Player.EffectToRemove.append(Thunder3DOTCheck)

#GCD

#Fire Spell
Fire1 = BLMSpell(1, True, 2.5, 2.5, 180, 800, True, False, ApplyFire1, [ManaRequirement])
#Fire2 AOE
Fire3 = BLMSpell(2, True, 3.5, 2.5, 260, 2000, True, False, ApplyFire3, [ManaRequirement])
Fire4 = BLMSpell(3, True, 2.8, 2.5, 310, 800, True, False, empty, [EnochianRequirement, FireRequirement, ManaRequirement]) #BIG PP DAMAGE LETS GOOOOOOOOOOOOOo
Despair = BLMSpell(9, True, 3, 2.5, 340, 800, True, False, ApplyDespair, [FireRequirement, ManaRequirement])
#Ice Spell
Blizzard1 = BLMSpell(4, True, 2.5, 2.5, 180, 400, False, True, ApplyBlizzard1, [ManaRequirement])
Blizzard3 = BLMSpell(5, True, 3.5, 2.5, 260, 800, False, True, ApplyBlizzard3, [ManaRequirement])
Blizzard4 = BLMSpell(6, True, 2.5, 2.5, 310, 800, False, True, ApplyBlizzard4, [EnochianRequirement, IceRequirement, ManaRequirement])
#Unaspected Spell
Paradox = BLMSpell(7, True, 2.5, 2.5, 500, 1600, False, False, ApplyParadox, [ParadoxRequirement, ManaRequirement])
Xenoglossy = BLMSpell(8, True, Lock, 2.5, 760, 0, False, False, ApplyXenoglossy, [PolyglotRequirement])
Thunder3 = BLMSpell(10, True, 2.5, 2.5, 50, 400, False, False, ApplyThunder3, [ManaRequirement])
Thunder3DOT = DOTSpell(-21, 35)


#oGCD
Transpose = BLMSpell(11, False, Lock, 0, 0, 0, False, False, ApplyTranspose, [TransposeRequirement])
Amplifier = BLMSpell(12, False, Lock, 0, 0, 0, False, False, ApplyAmplifier, [AmplifierRequirement])
LeyLines = BLMSpell(13, False, Lock, 0, 0, 0, False, False, ApplyLeyLines, [LeyLinesRequirement])
Triplecast = BLMSpell(14, False, Lock, 0, 0, 0, False, False, ApplyTripleCast, [TripleCastRequirement])
SharpCast = BLMSpell(15, False, Lock, 0, 0, 0, False, False, ApplySharpCast, [SharpCastRequirement])
Manafront = BLMSpell(16, False, Lock, 0, 0, 0, False, False, ApplyManafront, [ManafrontRequirement])