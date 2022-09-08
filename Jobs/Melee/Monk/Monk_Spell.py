from copy import deepcopy
from Jobs.Base_Spell import DOTSpell, buff, empty
from Jobs.Melee.Melee_Spell import MonkSpell
Lock = 0.75 #skill animation lock - simulating 75ms ping

#Requirements

def RaptorFormRequirement(Player, Spell):
    return Player.CurrentForm == 2, -1

def CoeurlFormRequirement(Player, Spell):
    return Player.CurrentForm == 3 , -1

def ThunderclapRequirement(Player, Spell):
    return Player.ThunderclapStack > 0, Player.ThunderclapCD

def MantraRequirement(Player, Spell):
    return Player.MantraCD <= 0, Player.MantraCD

def PerfectBalanceRequirement(Player, Spell):
    return Player.PerfectBalanceStack > 0, Player.PerfectBalanceCD

#Apply

def ApplyThunderclap(Player, Spell):
    if Player.ThunderclapStack == 3:
        Player.EffectCDList.append(ThunderclapStackCheck)
        Player.ThunderclapCD = 30
    Player.ThunderclapStack -= 1


def ApplyOpoOpo(Player, Enemy):
    Player.CurrentForm = 1
    AddChangeFormCheck(Player)

def ApplyRaptor(Player, Enemy):
    Player.CurrentForm = 2 #Into Raptor
    AddChangeFormCheck(Player)

def ApplyCoeurl(Player, Enemy):
    Player.CurrentForm = 3 #Into Coeurl
    AddChangeFormCheck(Player)

def ApplyMantra(Player, Enemy):
    Player.MantraCD = 90

def ApplyPerfectBalance(Player, Enemy):
    if Player.PerfectBalanceStack == 2:
        Player.EffectCDList.append(PerfectBalanceStackCheck)
        Player.PerfectBalanceCD = 40
    Player.PerfectBalanceStack -= 1

#Effect

def LeadenFistEffect(Player, Spell):
    if Spell.id == Bootshine.id: Spell.Potency += 100

#Check

def PerfectBalanceStackCheck(Player, Enemy):
    if Player.PerfectBalanceCD <= 0:
        if Player.PerfectBalanceStack == 1:
            Player.EffectToRemove.append(PerfectBalanceStackCheck)
        else:
            Player.PerfectBalanceTimer = 40
        Player.PerfectBalanceStack += 1

def ThunderclapStackCheck(Player, Enemy):
    if Player.ThunderclapCD <= 0:
        if Player.ThunderclapStack == 2:
            Player.EffectToRemove.append(ThunderclapStackCheck)
        else:
            Player.ThunderclapTimer = 30
        Player.ThunderclapStack += 1

def DemolishDOTCheck(Player, Enemy):
    if Player.DemolishDOTTimer <= 0:
        Player.DOTList.remove(Player.DemolishDOT)
        Player.DemolishDOT = None
        Player.EffectToRemove.append(DemolishDOTCheck)

def DisciplinedFistCheck(Player, Enemy):
    if Player.DisciplinedFistTimer <= 0:
        Player.buffList.remove(DisciplinedFistBuff)
        Player.EffectToRemove.append(DisciplinedFistCheck)

def ChangeFormCheck(Player, Enemy):
    if Player.CurrentForm == 1: #Opo-Opo
        Player.EffectList.append(OpoOpoCombo)
    elif Player.CurrentForm == 2: #Raptor
        Player.EffectList.append(RaptorCombo)
    elif Player.CurrentForm == 3: #Coeurl
        Player.EffectList.append(CoeurlCombo)
    elif Player.CurrentForm == 4: #Formless
        pass

    Player.EffectToRemove.append(ChangeFormCheck) #Removing itself

def LeadenFistCheck(Player, Enemy):
    if Player.LeadenFistTimer <= 0:
        Player.EffectList.remove(LeadenFistEffect)
        Player.EffectToRemove.append(LeadenFistCheck)

#Combo Effect

def OpoOpoCombo(Player, Spell):
    if Spell.GCD:
        if Spell.id == Bootshine.id or Spell.id == ShadowOfTheDestroyer.id:
            Player.GuaranteedCrit = True
        elif Spell.id == DragonKick.id:
            #Grants Leaden Fist
            if Player.LeadenFistTimer == 0: #If not already applied
                Player.EffectList.append(LeadenFistEffect)
                Player.EffectCDList.append(LeadenFistCheck)
            Player.LeadenFistTimer = 30
        
        Player.EffectToRemove.append(OpoOpoCombo) #Removing itself

        

def RaptorCombo(Player, Spell):
    if Spell.GCD:
        if Spell.id == TrueStrike.id: #Nothing happens
            pass
        elif Spell.id == TwinSnakes.id or Spell.id == FourpointFurry.id:
            if Player.DisciplinedFistTimer == 0:
                Player.buffList.append(DisciplinedFistBuff)
                Player.EffectCDList.append(DisciplinedFistCheck)
            Player.DisciplinedFistTimer = 15

        Player.EffectToRemove.append(RaptorCombo)
        

def CoeurlCombo(Player, Spell):
    if Spell.GCD:
        if Spell.id == Demolish.id:
            if Player.DemolishDOT == None:
                Player.DemolishDOT = deepcopy(DemolishDOT)
                Player.EffectCDList.append(DemolishDOTCheck)
                Player.DOTList.append(Player.DemolishDOT)
            Player.DemolishDOTTimer = 18
        elif Spell.id == SnapPunch.id or Spell.id == Rockbreaker.id:
            pass #Nothing happens
        Player.EffectToRemove.append(CoeurlCombo)

#Other relevant functions

def AddChangeFormCheck(Player):
    Player.EffectCDList.append(ChangeFormCheck)


#Opo-opo form  -> Raptor Form
Bootshine = MonkSpell(0, True, 2, 210, ApplyRaptor, [], True, False)
DragonKick = MonkSpell(1, True, 2, 320, ApplyRaptor, [], True, False)
ShadowOfTheDestroyer = MonkSpell(2, True,2, 110, ApplyRaptor, [], True, False) #AOE of Bootshine

#Raptor form combo -> Coeurl form
TrueStrike = MonkSpell(4, True, 2, 300, ApplyCoeurl, [RaptorFormRequirement], True, False)
TwinSnakes = MonkSpell(5, True, 2, 280, ApplyCoeurl, [RaptorFormRequirement], True, False)
FourpointFurry = MonkSpell(6, True, 2, 120, ApplyCoeurl, [RaptorFormRequirement], True, False) #AOE of Twinsnakes

#Coeurl form combo -> Opo-opo form
Demolish = MonkSpell(7, True, 2, 130, ApplyOpoOpo, [CoeurlFormRequirement], True, False)
DemolishDOT = DOTSpell(10, 70, True)
SnapPunch = MonkSpell(8, True,2 ,310, ApplyOpoOpo, [CoeurlFormRequirement], True, False)
Rockbreaker = MonkSpell(9, True, 2, 130, ApplyOpoOpo, [CoeurlFormRequirement], True, False)

#oGCD
PerfectBalance = MonkSpell(13, False, 0, 0, ApplyPerfectBalance, [PerfectBalanceRequirement], False, False)

#non Damage oGCD
Thunderclap = MonkSpell(11, False, 0, 0, ApplyThunderclap, [ThunderclapRequirement],False, False)
Mantra = MonkSpell(12, False, 0, 0, ApplyMantra, [MantraRequirement], False, False)
#Buff
DisciplinedFistBuff = buff(1.15)

#MonkAbility = {}