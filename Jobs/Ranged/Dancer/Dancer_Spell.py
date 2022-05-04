from Jobs.Base_Spell import empty
from Jobs.Ranged.Ranged_Spell import DancerSpell

#Requirement

def StandardStepRequirement(Player, Spell):
    return Player.StandardStepCD <= 0

def DanceRequirement(Player, Spell):
    return Player.Dancing

def StandardFinishRequirement(Player, Spell):
    #Will check how many step we have
    #Not done in apply since we want to acces the spell easily

    Player.MultDPSBonus /= Player.StandardFinishDPSMult #Reset DPSBonus
    Player.DancePartner.MultDPSBonus /= Player.StandardFinishDPSMult #Reset DPSBonus

    step = 0
    if Player.Emboite : step +=1
    if Player.Entrechat : step +=1
    if Player.Jete : step +=1
    if Player.Pirouette : step +=1

    if step == 1:
        Spell.Potency += 180
        Player.StandardFinishDPSMult = 1.02
    elif step > 1:
        Spell.Potency += 360
        Player.StandardFinishDPSMult = 1.05

    return Player.StandardFinish
        

def TechnicalStepRequirement(Player, Spell):
    return Player.TechnicalStepCD <= 0

#Apply
def ApplyCascade(Player, Enemy):
    #Cascade has 50% chance to grant SikenSymettry, so we will keep track of the expected number we should have
    Player.ExpectedTotalSilkenSymettry += 0.5 #adding to expected
    Player.SilkenSymettry = True    #Assuming it is true

    #Adding Combo Action
    if not (CascadeComboEffect in Player.EffectList) : Player.EffectList.append(CascadeComboEffect)


def ApplyStandardStep(Player, Enemy):
    Player.Dancing = True
    Player.StandardStepCD = 30
    Player.StandardFinish = True #Ready StandardFinish

def ApplyStandardFinish(Player, Enemy):
    #The MultBonus has already been computed from Requirement, so we just apply it to the dancer
    #and the dance partner

    #The check will be done on the dancer only
    if Player.StandardFinishTimer == 0: Player.EffectCDList.append(StandardFinishCheck)
    Player.StandardFinishTimer = 60
    Player.MultDPSBonus *= Player.StandardFinishDPSMult #Bonus DPS
    Player.DancePartner.MultDPSBonus *= Player.StandardFinishDPSMult #Dance Partner Bonus

    Player.Emboite = False
    Player.Entrechat = False
    Player.Jete = False
    Player.Pirouette = False
    #Reseting Dance move

def ApplyTechnicalStep(Player, Enemy):
    Player.Dancing = True
    Player.TechnicalStepCD = 120
    Player.TechnicalFinish = True #Ready TechnicalFinish

def ApplyTechnicalFinish(Player, Enemy):
    #The MultBonus has already been computed from Requirement, so we just apply it to the dancer
    #and the dance partner

    #The check will be done on the dancer only
    Player.EffectCDList.append(TechnicalFinishCheck)

    Player.TechnicalFinishTimer = 20
    Player.MultDPSBonus *= Player.TechnicalFinishDPSMult #Bonus DPS
    Player.DancePartner.MultDPSBonus *= Player.TechnicalFinishDPSMult #Dance Partner Bonus

    Player.Emboite = False
    Player.Entrechat = False
    Player.Jete = False
    Player.Pirouette = False
    #Reseting Dance move

def ApplyEmboite(Player, Enemy):
    Player.Emboite = True

def ApplyEntrechat(Player, Enemy):
    Player.Entrechat = True

def ApplyJete(Player, Enemy):
    Player.Jete = True

def ApplyPirouette(Player, Enemy):
    Player.Pirouette = True

#Effect

def CascadeComboEffect(Player, Spell):
    if Spell.id == Fountain.id:
        Spell.Potency += 180
        
        Player.ExpectedTotalSilkenFlow += 0.5
        Player.SilkenFlow = True
        Player.EffectToRemove.append(CascadeComboEffect)

#Check

def StandardFinishCheck(Player, Enemy):
    if Player.StandardFinishTimer <= 0:
        Player.MultDPSBonus /= Player.StandardFinishDPSMult
        Player.DancePartner.MultDPSBonus /= Player.StandardFinishDPSMult
        Player.EffectToRemove.append(StandardFinishCheck)

def TechnicalFinishCheck(Player, Enemy):
    if Player.TechnicalFinishTimer <= 0:
        Player.MultDPSBonus /= Player.TechnicalFinishDPSMult
        Player.DancePartner.MultDPSBonus /= Player.TechnicalFinishDPSMult
        Player.EffectToRemove.append(TechnicalFinishCheck)


#GCD
#ComboAction
Cascade = DancerSpell(0, True, 2.5, 220,ApplyCascade, [], True)
Fountain = DancerSpell(1, True, 2.5, 100, empty, [], True)

#Dance
StandardStep = DancerSpell(2, True, 1.5, 0, ApplyStandardStep, [StandardStepRequirement], True)
StandardFinish = DancerSpell(3, True, 1.5, 360, ApplyStandardFinish, [StandardFinishRequirement], True)

TechnicalStep = DancerSpell(8, True, 1.5, 0, ApplyTechnicalStep, [TechnicalStepRequirement], True)

#Dance Move
Emboite = DancerSpell(4, True, 1, 0, ApplyEmboite, [DanceRequirement], True)
Entrechat = DancerSpell(5, True, 1, 0, ApplyEntrechat, [DanceRequirement], True)
Jete = DancerSpell(6, True, 1, 0, ApplyJete, [DanceRequirement], True)
Pirouette = DancerSpell(7, True, 1, 0, ApplyPirouette, [DanceRequirement], True)


