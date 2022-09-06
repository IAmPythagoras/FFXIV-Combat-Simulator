from Jobs.Base_Spell import buff, empty
from Jobs.Melee.Melee_Spell import MonkSpell
Lock = 0.75 #skill animation lock - simulating 75ms ping

#Requirements

#Apply

def ApplyRaptor(Player, Enemy):
    Player.CurrentForm = 2 #Into Raptor
    AddChangeFormCheck(Player)


#Check

def ChangeFormCheck(Player, Enemy):
    if Player.CurrentForm == 1: #Opo-Opo
        Player.EffectList.append(OpoOpoCombo)
    elif Player.CurrentForm == 2: #Raptor
        Player.EffectList.append(RaptorCombo)
    elif Player.CurrentForm == 3: #Opo-Opo
        Player.EffectList.append(CoeurlCombo)
    elif Player.CurrentForm == 4: #Formless
        pass

#Combo Effect

def OpoOpoCombo(Player, Spell):
    if Spell.id == Bootshine.id:
        Player.GuaranteedCrit = True
    elif Spell.id == 

def RaptorCombo(Player, Spell):
    pass

def CoeurlCombo(Player, Spell):
    pass

#Other relevant functions

def AddChangeFormCheck(Player):


#Opo-opo form  -> Raptor Form
Bootshine = MonkSpell(0, True, 2, 210, ApplyRaptor )
DragonKick = MonkSpell(1, True)
ShadowOfTheDestroyer = MonkSpell(2, True,)
ArmOfTheDestroyer = MonkSpell(3, True) #AOE of ShadowOfTheDestroyer

#Raptor form combo -> Coeurl form
TrueStrike = MonkSpell(4, True,)
TwinSnakes = MonkSpell(5, True)
FourpointFurry = MonkSpell(6, True)

#Coeurl form combo -> Opo-opo form
Demolish = MonkSpell(7, True)
SnapPunch = MonkSpell(8, True)
Rockbreaker = MonkSpell(9, True)

#MonkAbility = {}