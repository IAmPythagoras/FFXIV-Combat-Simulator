#########################################
########## REDMAGE PLAYER ###############
#########################################
from Jobs.Base_Spell import buff
from Jobs.Caster.Caster_Spell import RedmageSpell, SwiftcastEffect
Lock = 0.75
#Special

def Addmana(Player, WhiteMana, BlackMana):
    Player.WhiteMana = min(100, Player.WhiteMana + WhiteMana)
    Player.BlackMana = min(100, Player.BlackMana + BlackMana)

def Removemana(Player, WhiteMana, BlackMana):
    Player.WhiteMana = max(0, Player.WhiteMana - WhiteMana)
    Player.BlackMana = max(0, Player.BlackMana - BlackMana)

#Requirement
def RDMManaRequirement(Player, Spell):
    return Spell.ManaCost <= Player.Mana and Spell.BlackCost <= Player.BlackMana and Spell.WhiteCost <= Player.WhiteMana, -1

def ManaficationRequirement(Player, Spell):
    return Player.ManaficationCD <= 0, Player.ManaficationCD

def EmboldenRequirement(Player, Spell):
    return Player.EmboldenCD <= 0, Player.EmboldenCD

def AccelerationRequirement(Player, Spell):
    return Player.AccelerationStack >= 1, Player.AccelerationCD

def FlecheRequirement(Player, Spell):
    return Player.FlecheCD <= 0, Player.FlecheCD

def ContreRequirement(Player, Spell):
    return Player.ContreCD <= 0, Player.ContreCD

def EngagementRequirement(Player, Spell):
    return Player.EngagementStack > 0, Player.EngagementCD

def CorpsRequirement(Player, Spell):
    return Player.CorpsStack > 0, Player.CorpsCD

#Combo Action Requirements

def ZwerchhauRequirement(Player, Spell):
    return Player.Zwerchhau,-1

def RedoublementRequirement(Player, Spell):
    return Player.Redoublement,-1

def VerholyRequirement(Player, Spell):
    return Player.Verholy,-1

def ScorchRequirement(Player, Spell):
    return Player.Scorch,-1

def ResolutionRequirement(Player, Spell):
    return Player.Resolution,-1



#Apply

def ApplyJolt(Player, Enemy):
    Addmana(Player, 2, 2)

def ApplyVerfire(Player, Enemy):
    Addmana(Player, 0, 5)

def ApplyVerstone(Player,Enemy):
    Addmana(Player, 5, 0)

def ApplyVerareao(Player, Enemy):
    Addmana(Player, 6, 0)

def ApplyVerthunder(Player, Enemy):
    Addmana(Player, 0, 6)

def ApplyManafication(Player, Enemy):
    Player.ManaficationStack = 6
    Player.ManaficationCD = 110
    Player.EffectList.insert(0,ManaficationEffect)
    Addmana(Player, 50, 50)

def ApplyEmbolden(Player, Enemy):
    Enemy.buffList.append(EmboldenBuff) #5% DPS boost for everyone. I put buff on Boss, but could put it on every other player
    Player.EmboldenTimer = 20
    Player.EmboldenCD = 120
    Player.EffectCDList.append(EmboldenCheck)

def ApplyAcceleration(Player, Enemy):
    if Player.AccelerationStack == 2:
         Player.AccelerationCD = 55
         Player.EffectCDList.append(AccelerationStackCheck)
    Player.EffectList.insert(0,AccelerationEffect)
    Player.AccelerationStack -= 1

def ApplyFleche(Player, Enemy):
    Player.FlecheCD = 25

def ApplyContre(Player, Enemy):
    Player.ContreCD = 35

def ApplyEngagement(Player, Enemy):
    if Player.EngagementStack == 2:
        Player.EngagementCD = 35
        Player.EffectCDList.append(EngagementStackCheck)
    Player.EngagementStack -= 1

def ApplyCorps(Player, Enemy):
    if Player.CorpsStack == 2:
        Player.CorpsCD = 35
        Player.EffectCDList.append(CorpsStackCheck)
    Player.CorpsStack -= 1




#Combo Action Apply

def ApplyRiposte(Player, Enemy):
    Removemana(Player, 20, 20)
    Player.Zwerchhau = True

def ApplyZwerchhau(Player, Enemy):
    Removemana(Player, 15, 15)
    Player.Redoublement = True
    Player.Zwerchhau = False

def ApplyRedoublement(Player, Enemy):
    Removemana(Player, 15, 15)
    Player.Verholy = True
    Player.Redoublement = False

def ApplyVerholy(Player, Enemy):
    Addmana(Player, 11, 0)
    Player.Scorch = True
    Player.Verholy = False

def ApplyScorch(Player, Enemy):
    Addmana(Player, 4, 4)
    Player.Resolution = True
    Player.Scorch = False

def ApplyResolution(Player, Enemy):
    Addmana(Player, 4, 4)
    Player.Resolution = False


#Effect

def DualCastEffect(Player, Spell):
    if Spell.CastTime != 0 and  Spell.GCD and Spell.id != -1:   #Want to make sure the spell will affect Dualcast, id != -1 is to make sure this is not WaitAbility
        #print("Spell satisfies DualCast")
        #print("Spell is : " + str(Spell.id))
        #print("CastTime : " + str(Spell.CastTime))
        if Player.DualCast:
            Spell.CastTime = 0 #Insta cast half of the spells, will be put by default for RedMage
            Player.DualCast = False #Remove Dualcast
        else: Player.DualCast = True    #Give Dual cast

def ManaficationEffect(Player, Spell):
    if Spell.GCD : #Only affect if GCD
        Player.ManaficationStack -= 1
        Spell.DPSBonus *= 1.05 #5% boost on magic damage

def AccelerationEffect(Player, Spell):
    if Spell.id == 3 and not (SwiftcastEffect in Player.EffectList): 
        Spell.CastTime = 0    #Will have to cast how this interacts with Dual cast
        Player.EffectToRemove.append(AccelerationEffect)

#Check

def ManaficationCheck(Player, Enemy):
    if Player.ManaficationStack == 0: Player.EffectList.remove(ManaficationEffect)#If no stack remove it

def EmboldenCheck(Player, Enemy):
    if Player.EmboldenTimer <= 0:
        Player.EmboldenTimer = 0
        Enemy.buffList.remove(EmboldenBuff) #Removing 5% dps increase
        Player.EffectToRemove.append(EmboldenCheck)

def AccelerationStackCheck(Player, Enemy):
    if Player.AccelerationCD <= 0:
        Player.AccelerationStack += 1

        if Player.AccelerationStack == 2:
            Player.EffectToRemove.append(AccelerationStackCheck)
        else:
            Player.AccelerationCD = 55

def EngagementStackCheck(Player, Enemy):
    if Player.EngagementCD <= 0:
        Player.EngagementStack += 1

        if Player.EngagementStack == 2:
            Player.EffectToRemove.append(EngagementStackCheck)
        else:
            Player.EngagementCD = 35

def CorpsStackCheck(Player, Enemy):
    if Player.CorpsCD <= 0:
        Player.CorpsStack += 1

        if Player.CorpsStack == 2:
            Player.EffectToRemove.append(CorpsStackCheck)
        else:
            Player.CorpsCD = 35

Jolt = RedmageSpell(0, True, 2, 2.5,310, 200, ApplyJolt, [RDMManaRequirement], 0, 0 )
Verfire = RedmageSpell(1, True, 2, 2.5, 330, 200, ApplyVerfire, [RDMManaRequirement], 0, 0)
Verstone = RedmageSpell(2, True, 2, 2.5, 330, 200, ApplyVerstone, [RDMManaRequirement], 0, 0)
Verthunder = RedmageSpell(3, True, 5, 2.5, 380, 300, ApplyVerthunder, [RDMManaRequirement], 0, 0)
Verareo = RedmageSpell(3, True, 5, 2.5, 380, 300, ApplyVerareao, [RDMManaRequirement], 0, 0)

#All melee actions are assumed to be enchanted
#Combo actions
Riposte = RedmageSpell(4, True, 0, 1.5, 220, 0, ApplyRiposte, [RDMManaRequirement], 20,20)
Zwerchhau = RedmageSpell(5, True, 0, 1.5, 290, 0, ApplyZwerchhau, [RDMManaRequirement, ZwerchhauRequirement], 15, 15)
Redoublement = RedmageSpell(6, True, 0, 2.5, 470, 0, ApplyRedoublement, [RDMManaRequirement, RedoublementRequirement], 15, 15)
Verholy = RedmageSpell(7, True, 0, 2.5, 580, 400, ApplyVerholy, [RDMManaRequirement, VerholyRequirement], 0, 0)
Scorch = RedmageSpell(8, True, 0, 2.5, 680, 400, ApplyScorch, [RDMManaRequirement, ScorchRequirement], 0, 0)
Resolution = RedmageSpell(9, True, 0, 2.5, 750, 400, ApplyResolution, [RDMManaRequirement, ResolutionRequirement], 0, 0)

#For now combo action cannot be cancelled by doing something else

Manafication = RedmageSpell(10, False, 0, Lock, 0, 0, ApplyManafication, [ManaficationRequirement], 0, 0)
Embolden = RedmageSpell(11, False, 0, Lock, 0, 0, ApplyEmbolden, [EmboldenRequirement], 0, 0)
Acceleration = RedmageSpell(12, False, 0, Lock, 0, 0, ApplyAcceleration, [AccelerationRequirement], 0, 0)

Fleche = RedmageSpell(13, False, 0, Lock, 460, 0, ApplyFleche, [FlecheRequirement], 0, 0)
Contre = RedmageSpell(14, False, 0, Lock, 360, 0, ApplyContre, [ContreRequirement], 0, 0)
Engagement = RedmageSpell(15, False, 0, Lock, 180, 0, ApplyEngagement, [EngagementRequirement], 0, 0)
Corps = RedmageSpell(16, False, 0, Lock, 130, 0, ApplyCorps, [CorpsRequirement], 0, 0)

#buff
EmboldenBuff = buff(1.05)
