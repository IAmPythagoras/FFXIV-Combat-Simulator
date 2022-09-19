from Jobs.Base_Spell import DOTSpell, ManaRequirement, buff, empty
from Jobs.Caster.Caster_Spell import BLMSpell, SwiftcastEffect
import copy
import math

from Jobs.Tank.Paladin.Paladin_Spell import ApplyFastBlade
Lock = 0
#Requirement

def ManawardRequirement(Player, Spell):
    return Player.ManawardCD <= 0, Player.ManawardCD

def EnochianRequirement(Player, Spell):
    return Player.EnochianTimer > 0, -1

def FireRequirement(Player, Spell):
    return Player.ElementalGauge > 0, -1

def IceRequirement(Player, Spell):
    return Player.ElementalGauge < 0, -1

def ParadoxRequirement(Player, Spell):
    return Player.Paradox, -1

def PolyglotRequirement(Player, Spell):
    return Player.PolyglotStack > 0, Player.PolyglotTimer

def TransposeRequirement(Player, Spell):
    return Player.TransposeCD <= 0, Player.TransposeCD

def AmplifierRequirement(Player, Spell):
    return Player.AmplifierCD <= 0, Player.AmplifierCD

def LeyLinesRequirement(Player, Spell):
    return Player.LeyLinesCD <= 0, Player.LeyLinesCD

def TripleCastRequirement(Player, Spell):
    return Player.TripleCastUseStack > 0, Player.TripleCastCD

def SharpCastRequirement(Player, Spell):
    return Player.SharpCastStack > 0, Player.SharpCastCD

def ManafrontRequirement(Player, Spell):
    return Player.ManafrontCD <= 0, Player.ManafrontCD

#Apply

def ApplyManaward(Player, Enemy):
    Player.ManawardCD = 120

def ApplyFlare(Player, Enemy):
    manaback = 0
    #input(Player.UmbralHearts)
    if Player.UmbralHearts > 0:
        Player.UmbralHearts -= 1
        manaback = math.floor(Player.Mana/3)
    ApplyDespair(Player, Enemy)
    Player.Mana += manaback #we get 1/3rd of our mana back if with UmbralHearts stack

def ApplyHighFire(Player, Enemy):
    ApplyFire3(Player, Enemy)
    Player.EffectList.append(HighFireEffect)
    Player.EffectCDList.append(HighFireCheck)

def ApplyThunder4(Player, Enemy):
    if Player.Thunder4DOT == None:
        Player.Thunder4DOT = copy.deepcopy(Thunder4DOT)
        Player.DOTList.append(Player.Thunder4DOT)
        Player.EffectList.append(Thunder4DOTCheck)
    Player.Thunder4DOTTimer = 18

    if Player.SharpCast: #If we have SharpCast
        Player.EffectList.append(Thunder3ProcEffect)
        Player.SharpCast = False

    #We now have to check if Thunder 3 is already applied, in which case we will remove it
    if Player.Thunder3DOT != None : Player.Thunder3DOTTimer = 0

def ApplyUmbralSoul(Player, Enemy):
    Player.AddIce() #Add 1 Ice
    Player.UmbralHearts = min(3, Player.UmbralHearts + 1)

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

    Player.ElementalGauge = -3
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

    #We now have to check if Thunder 4 is already applied, in which case we will remove it
    if Player.Thunder4DOT != None : Player.Thunder4DOTTimer = 0

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

def HighFireEffect(Player, Spell):
    if Spell.id == Flare.id:
        Spell.Potency += 60
        Player.EffectToRemove.append(HighFireEffect)
        Player.EffectCDList.remove(HighFireCheck)

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
    elif Spell.id == Thunder4.id:
        Spell.Potency += 120
        Spell.ManaCost = 0
        Spell.CastTime = Lock
        Player.EffectToRemove.append(Thunder3ProcEffect)

def TripleCastEffect(Player, Spell): 
    if not (SwiftcastEffect in Player.EffectList) and Spell.GCD and Spell.CastTime > Lock: #If GCD and not already insta cast, also Swift will go before
        Spell.CastTime = Lock
        Player.TripleCastStack -= 1

def LeyLinesEffect(Player, Spell):
    if Spell.GCD:
        Spell.CastTime *= 0.85
        Spell.RecastTime *= 0.85

def EnochianEffect(Player, Spell):
    if Player.ElementalGauge != 0:
        #If elementalGauge is not 0
        Player.buffList.append(Enochian)
        Player.EffectToRemove.append(EnochianEffect)
        Player.EffectCDList.append(EnochianEffectCheck)
        Player.Enochian = True

def ElementalEffect(Player, Spell):
    #Will affect Spell depending on fire and ice
    #input("UmbrealHearts : " + str(Player.UmbralHearts))
    if isinstance(Spell, BLMSpell) and Spell.IsFire:
        #Fire Spell
        #First check if fire phase and apply Effect
        if Player.ElementalGauge > 0: #Fire Phase
            #input('we in : ' + str(Spell.id))
            if Player.ElementalGauge == 1: Spell.Potency *= 1.4
            elif Player.ElementalGauge == 2 : Spell.Potency *= 1.6
            elif Player.ElementalGauge == 3 : Spell.Potency *= 1.8

            if (Player.UmbralHearts > 0) and Spell.id!= Flare.id: #If we have UmbralHearts, then no mana cost increase. We also have to make sure
                #it isn't Flare, since Flare has its own way of dealing with UmbrealHearts
                Player.UmbralHearts -= 1
            else : 
                if Spell.id != Despair.id and Spell.id != Flare.id: Spell.ManaCost *= 2 #Double mana cost, only if not despair
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
            Spell.CastTime = 0

#Check

def HighFireCheck(Player, Enemy):
    if Player.ElementalGauge <= 0: #If loose astralFire
        Player.EffectList.remove(HighFireEffect)
        Player.EffectToRemove.append(HighFireCheck)

def EnochianEffectCheck(Player, Enemy):
    if Player.ElementalGauge == 0: #If we loose Enochian
        Player.Enochian = False
        Player.buffList.remove(Enochian)
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

def Thunder4DOTCheck(Player, Enemy):
    if Player.Thunder4DOTTimer <= 0:
        Player.DOTList.remove(Player.Thunder4DOT)
        Player.Thunder4DOT = None
        Player.EffectToRemove.append(Thunder4DOTCheck)

#GCD

def ApplyFire4(Player, Enemy):
    input("Applying fire4 at : " + str(Player.CurrentFight.TimeStamp))

#Fire Spell
Fire1 = BLMSpell(141, True, 2.5, 2.5, 180, 800, True, False, ApplyFire1, [ManaRequirement])
Fire2 = BLMSpell(147, True, 3, 2.5, 100, 1500, True, False, ApplyFire3, [ManaRequirement]) #Same effect as Fire 3
Fire3 = BLMSpell(152, True, 3.5, 2.5, 260, 2000, True, False, ApplyFire3, [ManaRequirement])
Fire4 = BLMSpell(3577, True, 2.8, 2.5, 310, 800, True, False, empty, [EnochianRequirement, FireRequirement, ManaRequirement]) #BIG PP DAMAGE LETS GOOOOOOOOOOOOOo
Despair = BLMSpell(16505, True, 3, 2.5, 340, 800, True, False, ApplyDespair, [FireRequirement, ManaRequirement])
Flare = BLMSpell(162, True, 4, 2.5, 220, 800, True, False, ApplyFlare, [ManaRequirement, FireRequirement])
HighFire = BLMSpell(25794, True, 3, 2.5, 140, 1500, True, False, ApplyHighFire, [ManaRequirement])



#Ice Spell
UmbralSoul = BLMSpell(16506, True, 0, 2.5, 0, 0, False, True, ApplyUmbralSoul, [IceRequirement])
Blizzard1 = BLMSpell(142, True, 2.5, 2.5, 180, 400, False, True, ApplyBlizzard1, [ManaRequirement])
Blizzard3 = BLMSpell(154, True, 3.5, 2.5, 260, 800, False, True, ApplyBlizzard3, [ManaRequirement])
Blizzard4 = BLMSpell(3576, True, 2.5, 2.5, 310, 800, False, True, ApplyBlizzard4, [EnochianRequirement, IceRequirement, ManaRequirement])
Freeze = BLMSpell(159, True, 2.8, 2.5, 120, 1000, False, True, ApplyBlizzard4, [EnochianRequirement, IceRequirement, ManaRequirement]) #Same as B4
HighBlizzard = BLMSpell(25795, True, 3, 2.5, 140, 800, False, True, ApplyBlizzard3, [ManaRequirement])

#Unaspected Spell
Scathe = BLMSpell(156, True, Lock, 2.5, 100, 800, False, False, empty, [ManaRequirement])
Paradox = BLMSpell(25797, True, 2.5, 2.5, 500, 1600, False, False, ApplyParadox, [ParadoxRequirement, ManaRequirement]) 
Xenoglossy = BLMSpell(16507, True, Lock, 2.5, 760, 0, False, False, ApplyXenoglossy, [PolyglotRequirement])
Foul = BLMSpell(7422, True, Lock, 2.5, 560, 0, False, False, ApplyXenoglossy, [PolyglotRequirement]) #Same effect as Xeno
Thunder3 = BLMSpell(153, True, 2.5, 2.5, 50, 400, False, False, ApplyThunder3, [ManaRequirement])
Thunder3DOT = DOTSpell(-21, 35, False)
Thunder4 = BLMSpell(7420, True, 2.5, 2.5, 50, 400, False, False, ApplyThunder4, [ManaRequirement])
Thunder4DOT = DOTSpell(-40, 20, False)


#oGCD
Transpose = BLMSpell(149, False, Lock, 0, 0, 0, False, False, ApplyTranspose, [TransposeRequirement])
Amplifier = BLMSpell(25796, False, Lock, 0, 0, 0, False, False, ApplyAmplifier, [AmplifierRequirement])
LeyLines = BLMSpell(3573, False, Lock, 0, 0, 0, False, False, ApplyLeyLines, [LeyLinesRequirement])
Triplecast = BLMSpell(7421, False, Lock, 0, 0, 0, False, False, ApplyTripleCast, [TripleCastRequirement])
SharpCast = BLMSpell(3574, False, Lock, 0, 0, 0, False, False, ApplySharpCast, [SharpCastRequirement])
Manafront = BLMSpell(158, False, Lock, 0, 0, 0, False, False, ApplyManafront, [ManafrontRequirement])
BetweenTheLine = BLMSpell(7419, False, 0, 0, 0, 0, False, False, empty, [])
AetherialManipulation = BLMSpell(155, False, 0, 0, 0, 0, False, False, empty, [])
Manaward = BLMSpell(157, False, 0, 0, 0, 0, False, False, ApplyManaward, [ManawardRequirement])


#buff
Enochian = buff(1.2)


#All BlackMage abilities with their id in a dictionnary

BlackMageAbility = {
141 : Fire1, 
142 : Blizzard1, 
147 : Fire2, 
149 : Transpose, 
152 : Fire3,
155 :  AetherialManipulation, 
156 :  Scathe,
157 : Manaward, 
153 : Thunder3, 
154 : Blizzard3, 
158 : Manafront, 
159 : Freeze, 
162 : Flare, 
3573 : LeyLines, 
3574 : SharpCast, 
3576 : Blizzard4, 
3577 : Fire4, 
7419 : BetweenTheLine, 
7420 : Thunder4, 
7421 : Triplecast, 
7422 : Foul, 
16505 : Despair, 
16506 : UmbralSoul, 
16507 : Xenoglossy, 
25794 : HighFire, 
25795 : HighBlizzard, 
25796 : Amplifier, 
25797 : Paradox
}