import copy

from Jobs.Base_Spell import DOTSpell, ManaRequirement, buff, empty
from Jobs.Healer.Healer_Spell import AstrologianSpell
Lock = 0.75

#Requirement

def DrawRequirement(Player, Spell):
    return Player.DrawStack > 0

def ArcanumRequirement(Player, Spell):
    return Player.HasCard

def MinorArcanaRequirement(Player, Spell):
    return Player.MinorArcanaCD <= 0

def LordOfCrownRequirement(Player, Spell):
    return Player.LordOfCrown #Will be assumed to be given by Minor Arcana

def DivinationRequirement(Player, Spell):
    return Player.DivinationCD <= 0

def LightspeedRequirement(Player, Spell):
    return Player.LightspeedCD <= 0

#Apply

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
        Player.MultDPSBonus *= 1.05
        Player.EffectCDList.append(MindCheck)


def ApplyDraw(Player, Enemy):
    Player.HasCard = True

    if Player.DrawStack == 2:
        Player.EffectCDList.append(DrawStackCheck)
        Player.DrawCD = 30
    Player.DrawStack -= 1

def ApplyMinorArcana(Player, Enemy):
    Player.LordOfCrown = True
    Player.MinorArcanaCD = 60

def ApplyLordOfCrown(Player, Enemy):
    Player.LordOfCrown = False

def ApplyDivination(Player, Enemy):
    Enemy.Bonus *= 1.06 #Just give DPS bonus on Enemy instead of raid wide buff
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

def BodyCheck(Player, Enemy):
    if Player.BodyTimer <= 0:
        Player.EffectList.remove(BodyEffect)
        Player.EffectToRemove.append(BodyCheck)

def MindCheck(Player, Enemy):
    if Player.BodyTimer <= 0:
        Player.MultDPSBonus /= 1.05
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
        Enemy.Bonus /= 1.06
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

#GCD
Malefic = AstrologianSpell(1, True, 1.5, 2.5, 250, 400, empty, [ManaRequirement])
Combust = AstrologianSpell(2, True, Lock, 2.5, 0, 400, ApplyCombust, [ManaRequirement])
LordOfCrown = AstrologianSpell(5, True, Lock, 1, 250, 0,  ApplyLordOfCrown, [LordOfCrownRequirement])
CumbustDOT = DOTSpell(-12, 55)


#oGCD
Lightspeed = AstrologianSpell(3, False, Lock, 0, 0, 0, ApplyLightspeed, [LightspeedRequirement])
Divination = AstrologianSpell(4, False, Lock, 0, 0, 0, ApplyDivination, [DivinationRequirement])
MinorArcana = AstrologianSpell(5, False, Lock, 0, 0, 0, ApplyMinorArcana, [MinorArcanaRequirement])
Draw = AstrologianSpell(6, False, Lock,0, 0, 0, ApplyDraw, [DrawRequirement])
Astrodyne = AstrologianSpell(7, False, Lock, 0, 0, 0, ApplyAstrodyne, [])

#Arcanum require a target within the team, so it will be a function that will return a spell that
#will target the given player. It is also assumed that the bonus is 6%
ArcanumBuff = buff(1.06)



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
            #input("Will affect target with Arcana :" + str(Target))
            Target.buffList.append(ArcanumBuff)
            Target.EffectCDList.append(ArcanumCheck)

        Target.ArcanumTimer = 15

        if Type == "Lunar" : Player.Lunar = True
        elif Type == "Solar" : Player.Solar = True
        elif Type == "Celestial" : Player.Celestial = True


    return AstrologianSpell(0, False, Lock, 0, 0, 0, ApplyArcanum, [ArcanumRequirement])

        