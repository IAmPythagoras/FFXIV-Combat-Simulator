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

def AddersgallRequirement(Player, Enemy):
    return Player.AddersgallStack > 0, -1

def KrasisRequirement(Player, Spell):
    return Player.KrasisCD <= 0, Player.KrasisCD

def PanhaimaRequirement(Player, Spell):
    return Player.PanhaimaCD <= 0, Player.PanhaimaCD

def HolosRequirement(Player, Spell):
    return Player.HolosCD <= 0, Player.HolosCD

def RhizomataRequirement(Player, Spell):
    return Player.RhizomataCD <= 0, Player.RhizomataCD

def HaimaRequirement(Player, Spell):
    return Player.HaimaCD <= 0, Player.HaimaCD

def TaurocholeRequirement(Player, Spell):
    return Player.TaurocholeCD <= 0, Player.TaurocholeCD

def PepsiRequirement(Player, Spell):
    return Player.PepsiCD <= 0, Player.PepsiCD

def ZoeRequirement(Player, Spell):
    return Player.ZoeCD <= 0, Player.ZoeCD

def IxocholeRequirement(Player, Spell):
    return Player.IxocholeCD <= 0, Player.IxocholeCD

def KeracholeRequirement(Player, Spell):
    return Player.KeracholeCD <= 0, Player.KeracholeCD

def IcarusRequirement(Player, Spell):
    return Player.IcarusCD <= 0, Player.IcarusCD

def SoteriaRequirement(Player, Spell):
    return Player.SoteriaCD <= 0, Player.SoteriaCD

#Apply

def ApplyDiagnosis(Player, Enemy):
    Player.AdderstingStack = min(3, Player.AdderstingStack + 1) #Will be assumed each time we do it gives a stack

def ApplyKrasis(Player, Enemy):
    Player.KrasisCD = 60

def ApplyPanhaima(Player, Enemy):
    Player.PanhaimaCD = 120

def ApplyHolos(Player, Enemy):
    Player.HolosCD = 120

def ApplyRhizomata(Player, Enemy):
    Player.RhizomataCD = 90
    Player.AddersgallStack = min(3, Player.AddersgallStack + 1)

def Apply(Player, Enemy):
    Player.CD = 0

def ApplyHaima(Player, Enemy):
    Player.HaimaCD = 120

def ApplyTaurochole(Player, Enemy):
    Player.TaurocholeCD = 45
    Player.AddersgallStack -= 1

def ApplyPepsi(Player, Enemy):
    Player.PepsiCD = 30

def ApplyZoe(Player, Enemy):
    Player.ZoeCD = 90

def ApplyKerachole(Player, Enemy):
    Player.KeracholeCD = 30
    Player.AddersgallStack -= 1

def ApplyIxochole(Player, Enemy):
    Player.IxocholeCD = 30
    Player.AddersgallStack -= 1

def ApplyIcarus(Player, Enemy):
    Player.IcarusCD = 45

def ApplySoteria(Player, Enemy):
    Player.SoteriaCD = 90

def ApplyDruochole(Player, Enemy):
    Player.AddersgallStack -= 1

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
Egeiro = SageSpell(5, True, 8, 2.5, 0, 2400, empty, [ManaRequirement])
Prognosis = SageSpell(6, True, 2, 2.5, 0, 800, empty, [ManaRequirement])
Diagnosis = SageSpell(7, True, 1.5, 2.5, 0, 400, ApplyDiagnosis, [ManaRequirement])
#Damage oGCD
Eukrasia = SageSpell(8, False, Lock, 0, 0, 0, ApplyEukrasia, []) #Since only 1 sec CD, no real need to put a requirement

#Healing oGCD
Krasis = SageSpell(9, False, 0, 0, 0, 0, ApplyKrasis, [KrasisRequirement])
Panhaima = SageSpell(10, False, 0, 0, 0, 0, ApplyPanhaima, [PanhaimaRequirement])
Holos = SageSpell(11, False, 0, 0, 0, 0, ApplyHolos, [HolosRequirement])
Rhizomata = SageSpell(12, False, 0, 0, 0, 0, ApplyRhizomata, [RhizomataRequirement])
Haima = SageSpell(13, False, 0, 0, 0, 0, ApplyHaima, [HaimaRequirement])
Taurochole = SageSpell(14, False, 0, 0, 0, 0, ApplyTaurochole, [TaurocholeRequirement,AddersgallRequirement])
Pepsi = SageSpell(15, False, 0, 0, 0, 0, ApplyPepsi, [PepsiRequirement])
Zoe = SageSpell(16, False, 0, 0, 0, 0, ApplyZoe, [ZoeRequirement]) #https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.leagueoflegends.com%2Fen-pl%2Fchampions%2Fzoe%2F&psig=AOvVaw2X9QcnXQ_CGp3xMY8MLua9&ust=1654295724885000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCJjl4oPqj_gCFQAAAAAdAAAAABAD
Ixochole = SageSpell(17, False, 0, 0, 0, 0, ApplyIxochole, [IxocholeRequirement,AddersgallRequirement])
Kerachole = SageSpell(18, False, 0, 0, 0, 0, ApplyKerachole, [KeracholeRequirement,AddersgallRequirement])
Icarus = SageSpell(19, False, 0, 0, 0, 0, ApplyIcarus, [IcarusRequirement])
Soteria = SageSpell(20, False, 0, 0, 0, 0, ApplySoteria, [SoteriaRequirement])
Druochole = SageSpell(21, False, 0, 0, 0, 0, ApplyDruochole, [AddersgallRequirement])

SageAbility = {}