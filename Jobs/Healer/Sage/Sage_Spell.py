from Jobs.Base_Spell import DOTSpell, ManaRequirement, empty
from Jobs.Healer.Healer_Spell import SageSpell
from Jobs.Healer.Sage.Sage_Spell import SageSpell
import copy
Lock = 0.75


#Requirement

def EukrasianDosisRequirement(Player, Spell):
    return Player.Eukrasia, -1

def PneumaRequirement(Player, Spell):
    return Player.PneumaCD <= 0, Player.PneumaCD

def PhlegmaRequirement(Player, Spell):
    return Player.PhlegmaStack > 0, Player.PhlegmaCD

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


#Damage GCD
Dosis = SageSpell(1, True, 1.5, 2.5, 330, 400, empty, [ManaRequirement])
EukrasianDosis = SageSpell(2, True, Lock, 1.5, 0, 400, ApplyEukrasian, [ManaRequirement, EukrasianDosisRequirement])
EukrasianDOT = DOTSpell(-12, 70, False)
Phlegma = SageSpell(3, True, Lock, 2.5, 510, 400, ApplyPhlegma, [PhlegmaRequirement])
Pneuma = SageSpell(4, True, 1.5, 2.5, 330, 700, ApplyPneuma, [ManaRequirement, PneumaRequirement])

#Healing GCD
Egeiro = SageSpell(1, True, 8, 2.5, 0, 2400, empty, [ManaRequirement])
Prognosis = SageSpell(1, True, 2, 2.5, 0, 800, empty, [ManaRequirement])
Diagnosis = SageSpell(1, True, 1.5, 2.5, 0, 400, empty, [ManaRequirement])
#Damage oGCD
Eukrasia = SageSpell(5, False, Lock, 0, 0, 0, ApplyEukrasia, []) #Since only 1 sec CD, no real need to put a requirement

#Healing oGCD
Krasis = SageSpell(1, False, 0, 0, 0, 0, ApplyKrasis, [KrasisRequirement])
Panhaima = SageSpell(1, False, 0, 0, 0, 0, ApplyPanhaima, [PanhaimaRequirement])
Holos = SageSpell(1, False, 0, 0, 0, 0, ApplyHolos, [HolosRequirement])
Rhizomata = SageSpell(1, False, 0, 0, 0, 0, ApplyRhizomata, [RhizomataRequirement])
Haimi = SageSpell(1, False, 0, 0, 0, 0, ApplyHaima, [HaimaRequirement])
Taurochole = SageSpell(1, False, 0, 0, 0, 0, ApplyTaurochole, [TaurocholeRequirement])
Pepsi = SageSpell(1, False, 0, 0, 0, 0, ApplyPepsi, [PepsiRequirement])
Zoe = SageSpell(1, False, 0, 0, 0, 0, ApplyZoe, [ZoeRequirement]) #https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.leagueoflegends.com%2Fen-pl%2Fchampions%2Fzoe%2F&psig=AOvVaw2X9QcnXQ_CGp3xMY8MLua9&ust=1654295724885000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCJjl4oPqj_gCFQAAAAAdAAAAABAD
Ixochole = SageSpell(1, False, 0, 0, 0, 0, ApplyIxochole, [IxocholeRequirement])
Kerachole = SageSpell(1, False, 0, 0, 0, 0, ApplyKerachole, [KeracholeRequirement])
Icarus = SageSpell(1, False, 0, 0, 0, 0, ApplyIcarus, [IcarusRequirement])
Soteria = SageSpell(1, False, 0, 0, 0, 0, ApplySoteria, [SoteriaRequirement])