from Jobs.Base_Spell import empty
from Jobs.Ranged.Ranged_Spell import DancerSpell

#Requirement

def StandardStepRequirement(Player, Spell):
    return Player.StandardStepCD <= 0

def DanceRequirement(Player, Spell):
    return Player.Dancing

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

#GCD
#ComboAction
Cascade = DancerSpell(0, True, 2.5, 220,ApplyCascade, [], True)
Fountain = DancerSpell(1, True, 2.5, 100, empty, [], True)

#Dance
StandardStep = DancerSpell(2, True, 1.5, 0, ApplyStandardStep, [StandardStepRequirement], True)
StandardFinish = DancerSpell(3, True, 1.5, 360, ApplyStandardFinish, [StandardFinishRequirement], True)

#Dance Move
Emboite = DancerSpell(4, True, 1, 0, ApplyEmboite, [DanceRequirement], True)
Entrechat = DancerSpell(4, True, 1, 0, ApplyEntrechat, [DanceRequirement], True)
Jete = DancerSpell(4, True, 1, 0, ApplyJete, [DanceRequirement], True)
Pirouette = DancerSpell(4, True, 1, 0, ApplyPirouette, [DanceRequirement], True)


