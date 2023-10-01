#########################################
########## REDMAGE PLAYER ###############
#########################################
# Acc -> Dual -> Swift
from ffxivcalc.Jobs.Base_Spell import ManaRequirement, buff, empty, buffPercentHistory
from ffxivcalc.Jobs.Caster.Caster_Spell import RedmageSpell, SwiftcastEffect
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
    return Player.ManaStack == 3,-1

def ScorchRequirement(Player, Spell):
    return Player.Scorch,-1

def ResolutionRequirement(Player, Spell):
    return Player.Resolution,-1

def MagickBarrierRequirement(Player, Spell):
    return Player.MagickBarrierCD <= 0, Player.MagickBarrierCD

#Apply

def ApplyEnchantedMoulinet(Player, Enemy):
    Player.ManaStack = min(3, Player.ManaStack + 1) #Max of 3 stacks

def ApplyMagickBarrier(Player, Enemy):
    Player.MagickBarrierCD = 120

def ApplyImpact(Player, Enemy):
    Addmana(Player, 3, 3) #Add mana

def ApplyMoulinet(Player, Enemy):
    Removemana(Player, 20, 20)
    Player.ManaStack = min(3, Player.ManaStack + 1) #Max of 3 stacks

def ApplyJolt(Player, Enemy):
    Addmana(Player, 2, 2)

def ApplyVerfire(Player, Enemy):
    Player.UsedVerfireProc += 1
    Addmana(Player, 0, 5)

def ApplyVerstone(Player,Enemy):
    Player.UsedVerstoneProc += 1
    Addmana(Player, 5, 0)

def ApplyVerareao(Player, Enemy):
    Player.ExpectedVerstoneProc += 0.5
    Addmana(Player, 6, 0)

def ApplyVerthunder(Player, Enemy):
    Player.ExpectedVerfireProc += 0.5
    Addmana(Player, 0, 6)

def ApplyManafication(Player, Enemy):
    Player.ManaficationStack = 6
    Player.ManaficationCD = 110
    Player.EffectList.insert(0,ManaficationEffect)
    Player.EffectCDList.append(ManaficationCheck)
    Addmana(Player, 50, 50)

def ApplyEmbolden(Player, Enemy):
    Player.EmboldenTimer = 20
    Player.EmboldenCD = 120
    if not Player.CurrentFight.SavePreBakedAction:
        Player.EffectCDList.append(EmboldenCheck)
        Enemy.buffList.append(EmboldenBuff) #5% DPS boost for everyone. I put buff on Boss, but could put it on every other player
        
                                     # Only doing this if SavePreBakedAction is true
    if Player.CurrentFight.SavePreBakedAction:
        fight = Player.CurrentFight
        history = buffPercentHistory(fight.TimeStamp, fight.TimeStamp + 20 , EmboldenBuff.MultDPS)
        fight.PlayerList[fight.PlayerIDSavePreBakedAction].PercentBuffHistory.append(history)

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
    if not (Riposte in Player.EffectList) : Player.EffectList.append(RiposteCombo)

def ApplyEnchantedRiposte(Player, Enemy):
    Removemana(Player, 20, 20)
    Player.ManaStack = min(3, Player.ManaStack + 1) #Max of 3 stacks
    if not (Riposte in Player.EffectList) : Player.EffectList.append(RiposteCombo)
    if not (ManaStackEffect in Player.EffectList) : Player.EffectList.append(ManaStackEffect)
    #This effect is to make sure we only do melee actions, since otherwise we loose mana stacks

def ApplyZwerchhau(Player, Enemy):
    Removemana(Player, 15, 15)
    Player.ManaStack = min(3, Player.ManaStack + 1) #Max of 3 stacks
    if not (ManaStackEffect in Player.EffectList) : Player.EffectList.append(ManaStackEffect)
    #This effect is to make sure we only do melee actions, since otherwise we loose mana stacks

def ApplyRedoublement(Player, Enemy):
    Removemana(Player, 15, 15)
    Player.ManaStack = min(3, Player.ManaStack + 1) #Max of 3 stacks
    if not (ManaStackEffect in Player.EffectList) : Player.EffectList.append(ManaStackEffect)
    #This effect is to make sure we only do melee actions, since otherwise we loose mana stacks

def ApplyVerholy(Player, Enemy):
    Addmana(Player, 11, 0)
    Player.Scorch = True
    Player.ManaStack -= 1 #Removing one mana stack
    if Player.WhiteMana < Player.BlackMana:
        Player.ExpectedVerstoneProc += 1
    else : Player.ExpectedVerstoneProc += 0.2

def ApplyVerflare(Player, Enemy):
    Addmana(Player, 0, 11)
    Player.Scorch = True
    Player.ManaStack -= 1 #Removing one mana stack
    if Player.WhiteMana > Player.BlackMana:
        Player.ExpectedVerfireProc += 1
    else : Player.ExpectedVerfireProc += 0.2

def ApplyScorch(Player, Enemy):
    Addmana(Player, 4, 4)
    Player.Resolution = True
    Player.Scorch = False
    Player.ManaStack -= 1 #Removing one mana stack

def ApplyResolution(Player, Enemy):
    Addmana(Player, 4, 4)
    Player.Resolution = False
    Player.ManaStack -= 1 #Removing one mana stack


#Effect

def ManaStackEffect(Player, Spell):
    if Spell.id == Verholy.id or Spell.id == Verflare.id:
        #Then we remove this effect
        Player.EffectToRemove.append(ManaStackEffect)
    elif Spell.GCD and not (Spell.id == EnchantedRiposte.id or Spell.id == EnchantedZwerchhau.id or Spell.id == EnchantedRedoublement.id):
        #If not any of these, we loose mana stacks
        Player.ManaStack = 0
        Player.EffectToRemove.append(ManaStackEffect)

def RiposteCombo(Player, Spell):
    if Spell.id == EnchantedZwerchhau.id:
        Spell.Potency += 190
        Player.EffectToRemove.append(RiposteCombo)
        Player.EffectList.append(ZwerchhauCombo)
    elif Spell.id == Zwerchhau.id:
        Spell.Potency += 50
        Player.EffectToRemove.append(RiposteCombo)
        Player.EffectList.append(ZwerchhauCombo)

def ZwerchhauCombo(Player, Spell):
    if Spell.id == EnchantedRedoublement.id:
        Spell.Potency += 370
        Player.EffectToRemove.append(ZwerchhauCombo)
    elif Spell.id == Redoublement.id:
        Spell.Potency += 130
        Player.EffectToRemove.append(ZwerchhauCombo)

def DualCastEffect(Player, Spell):
    if Spell.CastTime != 0 and  Spell.GCD and Spell.id != -1:   #Want to make sure the spell will affect Dualcast, id != -1 is to make sure this is not WaitAbility
        if Player.DualCast:
            Spell.CastTime = 0 #Insta cast half of the spells, will be put by default for RedMage
            Player.DualCast = False #Remove Dualcast
        else: Player.DualCast = True    #Give Dual cast

def ManaficationEffect(Player, Spell):
    if Spell.GCD : #Only affect if GCD
        Player.ManaficationStack -= 1
        Spell.DPSBonus *= 1.05 #5% boost on magic damage

def AccelerationEffect(Player, Spell):
    if (Spell.id == Verthunder.id or Spell.id == Verareo.id or Spell.id == Impact.id):
        Spell.CastTime = 0 
        Player.EffectToRemove.append(AccelerationEffect)
        if Spell.id == Impact.id : Spell.Potency += 50 #Impact has high potency when used with Acceleration

        # Adding to Expected proc value

        match Spell.id:
            case Verthunder.id:
                Player.ExpectedVerfireProc += 1
            case Verareo.id:
                Player.ExpectedVerstoneProc += 1

#Check

def ManaficationCheck(Player, Enemy):
    if Player.ManaficationStack == 0: 
        Player.EffectList.remove(ManaficationEffect)#If no stack remove it
        Player.EffectToRemove.append(ManaficationCheck)

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


#GCD    

Jolt = RedmageSpell(7524, True, 2, 2.5,310, 200, ApplyJolt, [ManaRequirement], 0, 0, type = 1)
Verfire = RedmageSpell(7510, True, 2, 2.5, 330, 200, ApplyVerfire, [ManaRequirement], 0, 0, type = 1)
Verstone = RedmageSpell(7511, True, 2, 2.5, 330, 200, ApplyVerstone, [ManaRequirement], 0, 0, type = 1)
Verthunder = RedmageSpell(25855, True, 5, 2.5, 380, 300, ApplyVerthunder, [ManaRequirement], 0, 0, type = 1)
Verareo = RedmageSpell(25856, True, 5, 2.5, 380, 300, ApplyVerareao, [ManaRequirement], 0, 0, type = 1)
#AoEs
Impact = RedmageSpell(16526, True, 5, 2.5, 210, 400, ApplyImpact, [ManaRequirement], 0, 0, type = 1)
#Combo actions
#NonEnchanted
Riposte = RedmageSpell(7504, True, 0, 2.5, 130, 0, ApplyRiposte, [], 0, 0, type = 2)
Zwerchhau = RedmageSpell(7512, True, 0, 2.5, 100, 0, empty, [], 0, 0, type = 2)
Redoublement = RedmageSpell(7516, True, 0, 2.5, 100, 0, empty, [], 0, 0, type = 2)
Reprise = RedmageSpell(16529, True, 0, 2.5, 100, 0, empty, [], 0, 0, type = 2)
#Enchanted
EnchantedRiposte = RedmageSpell(7527, True, 0, 1.5, 280, 0, ApplyEnchantedRiposte, [RDMManaRequirement], 20,20, type = 2)
EnchantedZwerchhau = RedmageSpell(7528, True, 0, 1.5, 150, 0, ApplyZwerchhau, [RDMManaRequirement], 15, 15, type = 2)
EnchantedRedoublement = RedmageSpell(7529, True, 0, 2.2, 130, 0, ApplyRedoublement, [RDMManaRequirement], 15, 15, type = 2)
EnchantedReprise = RedmageSpell(16528, True, 0, 2.5, 330, 0, empty, [RDMManaRequirement], 5, 5, type = 2)
Verholy = RedmageSpell(7526, True, 0, 2.5, 580, 400, ApplyVerholy, [ManaRequirement, VerholyRequirement], 0, 0, type = 1)
Verflare = RedmageSpell(7525, True, 0, 2.5, 580, 400, ApplyVerflare, [ManaRequirement, VerholyRequirement], 0, 0, type = 1) #Same Requirement as Verholy, just need 3 Mana stacks
Scorch = RedmageSpell(16530, True, 0, 2.5, 680, 400, ApplyScorch, [ManaRequirement, ScorchRequirement], 0, 0, type = 1)
Resolution = RedmageSpell(25858, True, 0, 2.5, 750, 400, ApplyResolution, [ManaRequirement, ResolutionRequirement], 0, 0, type = 1)
#AOE Melee Action
Moulinet = RedmageSpell(7513, True, 0, 1.5, 130, 0, ApplyMoulinet, [RDMManaRequirement], 20, 20, type = 2)
EnchantedMoulinet = RedmageSpell(7530, True, 0, 1.5, 130, 0, ApplyEnchantedMoulinet, [RDMManaRequirement], 20, 20, type = 2)
#For now combo action cannot be cancelled by doing something else
Manafication = RedmageSpell(7521, False, 0, Lock, 0, 0, ApplyManafication, [ManaficationRequirement], 0, 0)
Embolden = RedmageSpell(7520, False, 0, Lock, 0, 0, ApplyEmbolden, [EmboldenRequirement], 0, 0)
Acceleration = RedmageSpell(7518, False, 0, Lock, 0, 0, ApplyAcceleration, [AccelerationRequirement], 0, 0)
Fleche = RedmageSpell(7517, False, 0, Lock, 460, 0, ApplyFleche, [FlecheRequirement], 0, 0)
Contre = RedmageSpell(7519, False, 0, Lock, 360, 0, ApplyContre, [ContreRequirement], 0, 0)
Engagement = RedmageSpell(16527, False, 0, Lock, 180, 0, ApplyEngagement, [EngagementRequirement], 0, 0)
Corps = RedmageSpell(7506, False, 0, Lock, 130, 0, ApplyCorps, [CorpsRequirement], 0, 0)

#Other GCD/oGCD with no DPS goal
MagickBarrier = RedmageSpell(25857, False, 0, 0, 0, 0, ApplyMagickBarrier, [MagickBarrierRequirement], 0, 0)
Verraise = RedmageSpell(7523, True,10, 2.5, 0,2400, empty, [RDMManaRequirement], 0, 0, type = 1)
Vercure = RedmageSpell(7514, True, 2, 2.5, 0, 500, empty, [RDMManaRequirement], 0, 0, type = 1)



#buff
EmboldenBuff = buff(1.05)

#ActionList
RedMageAbility = {
7530 : EnchantedMoulinet,
7504 : Riposte, 
7506 : Corps, 
7507 : Verareo, 
7510 : Verfire, 
7511 : Verstone, 
7512 : Zwerchhau, 
7513 : Moulinet, 
7514 : Vercure, 
7515 : Engagement,
7516 : Redoublement, 
7517 : Fleche, 
7518 : Acceleration, 
7519 : Contre,
7520 : Embolden, 
7521 : Manafication , 
7523 : Verraise, 
7524 : Jolt, 
25855 : Verthunder, 
25856 : Verareo, 
16526 : Impact, 
16527 : Engagement, 
16529 : Reprise,  
25857 : MagickBarrier, 
7527 : EnchantedRiposte, 
7528 : EnchantedZwerchhau,
7529 : EnchantedRedoublement,  
7530 : EnchantedMoulinet, 
16528 : EnchantedReprise,
25858 : Resolution, 
7526 : Verholy, 
7525 : Verflare, 
16530 : Scorch
}