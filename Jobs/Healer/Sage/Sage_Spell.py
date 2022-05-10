from Jobs.Base_Spell import DOTSpell, ManaRequirement, empty
from Jobs.Healer.Healer_Spell import SageSpell
from Jobs.Healer.Sage.Sage_Spell import SageSpell
import copy
Lock = 0.75


#Requirement

def EukrasianDosisRequirement(Player, Spell):
    return Player.Eukrasia

def PneumaRequirement(Player, Spell):
    return Player.PneumaCD <= 0

def PhlegmaRequirement(Player, Spell):
    return Player.PhlegmaStack > 0

#Apply

def ApplyEukrasia(Player, Enemy):
    Player.Eukrasia = True

def ApplyPneuma(Player, Enemy):
    Player.PneumaCD = 120

def ApplyPhlegma(Player, Enemy):
    if Player.PhlegmaStack == 2:
        Player.EffectCDList.append(PhlegmaStackCheck)
        Player.FlegmaCD = 45
    Player.PhlegmaStack -= 1

def ApplyEukrasian(Player, Enemy):
    Player.Eukrasia = False
    if Player.Eukrasian == None:
        Player.Eukrasian = copy.deepcopy(EukrasianDOT)
        Player.EffectCDList.append(EukrasianDOTCheck)
    Player.EukrasianTimer = 30



#Check

def PhlegmaStackCheck(Player, Enemy):
    if Player.PhlegmaTimer <= 0:
        if Player.PhlegmaStack == 1:
            Player.EffectToRemove.append(PhlegmaStackCheck)
        else:
            Player.PhlegmaTimer = 45
        Player.PhlegmaStack +=1



def EukrasianDOTCheck(Player, Enemy):
    if Player.EukrasianTimer <= 0:
        Player.EffectToRemove.append(EukrasianDOTCheck)
        Player.DOTList.remove(Player.Eukrasian)
        Player.Eukrasian = None


#GCD
Dosis = SageSpell(1, True, 1.5, 2.5, 330, 400, empty, [ManaRequirement])
EukrasianDosis = SageSpell(2, True, Lock, 1.5, 0, 400, ApplyEukrasian, [ManaRequirement, EukrasianDosisRequirement])
EukrasianDOT = DOTSpell(-12, 70, False)
Phlegma = SageSpell(3, True, Lock, 2.5, 510, 400, ApplyPhlegma, [PhlegmaRequirement])
Pneuma = SageSpell(4, True, 1.5, 2.5, 330, 700, ApplyPneuma, [ManaRequirement, PneumaRequirement])

#oGCD
Eukrasia = SageSpell(5, False, Lock, 0, 0, 0, ApplyEukrasia, []) #Since only 1 sec CD, no real need to put a requirement