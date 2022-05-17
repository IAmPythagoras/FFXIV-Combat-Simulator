from Jobs.Base_Spell import buff, empty
from Jobs.Melee.Melee_Spell import ReaperSpell
Lock = 0.75

#Requirement

def HarvestMoonRequirement(Player, Spell):
    return Player.Soulsow, -1

def SoulSliceRequirement(Player, Spell):
    return Player.SoulSliceStack > 0, Player.SoulSliceCD

def ArcaneCircleRequirement(Player, Spell):
    return Player.ArcaneCircleCD <= 0, Player.ArcaneCircleCD

def GluttonyRequirement(Player, Spell):
    return Player.GluttonyCD <= 0 and Player.SoulGauge >= 50, Player.GluttonyCD

def BloodStalkRequirement(Player, Spell):
    return Player.SoulGauge >= 50, -1

def GibbetRequirement(Player, Spell):
    return Player.SoulReaverStack > 0 and Player.AvatarTimer == 0, -1

def PlentifulHarvestRequirement(Player, Spell):

    #Will modify Spell's potency depending on ImmortalStack, will add 35 potency for each stack, for a max of 800

    Spell.Potency += Player.ImmortalSacrificeStack * 35

    return Player.ImmortalSacrificeStack > 0 and Player.BloodsownTimer == 0, Player.BloodsownTimer

def EnshroudRequirement(Player, Spell):
    return Player.EnshroudCD <= 0 and Player.ShroudGauge >= 50, Player.EnshroudCD


def VoidReapingRequirement(Player, Spell):
    return Player.AvatarTimer > 0 and Player.LemureGauge > 0, -1

def LemureSliceRequirement(Player, Spell):
    return Player.VoidShroudGauge > 1, -1

def CommunioRequirement(Player, Spell):
    return Player.LemureGauge > 0, -1

def UnveiledGibbetRequirement(Player, Spell):
    return Player.EnhancedGibbet, -1

def UnveiledGallows(Player, Spell):
    return Player.EnhancedGallows, -1

#Apply

def ApplyUnveiledGibbet(Player, Enemy):
    Player.AddGauge(-50) #Removing 50 Soul gauge
    Player.SoulReaverStack = 1

def ApplySlice(Player, Enemy):
    if not (SliceCombo in Player.EffectList) : Player.EffectList.append(SliceCombo)
    Player.AddGauge(10) #add 10 Soul Gauge

def ApplyCommunio(Player, Enemy):
    #Ends Enshroud effect
    Player.AvatarTimer = 0
    Player.LemureGauge = 0
    Player.VoidShroudGauge = 0
    #Removing all Gauge related to Enshroud

def ApplyLemureSlice(Player, Enemy):
    Player.VoidShroudGauge -= 2 #Removing 2

def ApplyVoidReaping(Player, Enemy):
    if not (VoidReapingEffect in Player.EffectList) : 
        Player.EffectList.append(VoidReapingEffect)
        Player.EffectCDList.append(VoidReapingCheck)
    Player.LemureGauge -= 1
    Player.VoidShroudGauge = min(5, Player.VoidShroudGauge + 1) #Each Lemure used, we get a void shroud
    Player.VoidReapingTimer = 30

def ApplyCrossReaping(Player, Enemy):
    if not (CrossReapingEffect in Player.EffectList) : 
        Player.EffectList.append(CrossReapingEffect)
        Player.EffectCDList.append(CrossReapingCheck)
    Player.LemureGauge -= 1
    Player.VoidShroudGauge = min(5, Player.VoidShroudGauge + 1)
    Player.CrossReapingTimer = 30

def ApplyEnshroud(Player, Enemy):
    Player.AddShroud(-50) #Removing 50Shroud Gauge
    Player.EnshroudCD = 15
    Player.AvatarTimer = 30 #Avatar Timer
    Player.LemureGauge = 5 #Max Lemure


def ApplyPlentifulHarvest(Player, Enemy):
    Player.AddShroud(50)
    Player.ImmortalStack = 0


def ApplyGibbet(Player, Enemy):
    if not (GibbetEffect in Player.EffectList) : 
        Player.EffectList.append(GibbetEffect) #Buffs next Gallows
        Player.EffectCDList.append(GibbetCheck)
    Player.AddShroud(10) #Add 10 ShroudGauge
    Player.GibbetEffectTimer = 60

def ApplyGallows(Player, Enemy):
    if not (GallowsEffect in Player.EffectList) : 
        Player.EffetList.append(GallowsEffect) #Buff next Gibbet
        Player.EffectCDList.append(GallowsCheck)
    Player.AddShroud(10) #Add 10 Shroud Gauge
    Player.GallowsEffectTimer = 60

def ApplyBloodStalk(Player, Enemy):
    Player.Addgauge(-50) #Removing 50 Soul Gauge
    Player.SoulReaverStack = 1 #Reset to 1


def ApplyGluttony(Player, Enemy):
    Player.AddGauge(-50) #Removing 50 Soul Gauge
    Player.GluttonyCD = 60
    Player.SoulReaverStack += 2


def ApplyArcaneCircle(Player, Enemy):
    if not (ArcaneCircleBuff in Enemy.buffList) : Enemy.buffList.append(ArcaneCircleBuff) #If not already in by another reaper
    #Will have to worry about if multiple reaper
    Player.ArcaneCircleCD = 120
    Player.ArcaneCircleTimer = 20
    Player.CircleOfSacrificeTimer = 5
    Player.BloodsownTimer = 6 #Cannot cast Plentiful harvest in that time

    #Here target is any player with the effect on, and Player is the Reaper casting it
    def CircleOfSacrificeEffet(Target, Spell):
        #This effect will be given to all players
        if Spell.GCD: #We will assume that the GCD will be either a Weaposkill or a spell
            Player.ImmortalStack = min(8, Player.ImmortalStack + 1)#Giving one stack

    def CircleOfSacrificeCheck(Target, Enemy):
        if Player.CircleOfSacrificeTimer <= 0: #If no more time, we remove
            Target.EffectList.remove(CircleOfSacrificeEffet)
            Target.EffectToRemove.append(CircleOfSacrificeCheck)

    for player in Player.CurrentFight.PlayerList:
        player.EffectList.append(CircleOfSacrificeEffet) #Giving the effect to all players in the fight
        Player.EffectCDList.append(CircleOfSacrificeCheck)

    

def ApplySoulSlice(Player, Enemy):
    if Player.SoulSliceStack == 2: #If max stack, we add check
        Player.EffectCDList.append(SoulSliceStackCheck)
        Player.SoulSliceCD = 30
    Player.SoulSliceStack -= 1

def ApplyShadowOfDeath(Player, Enemy):

    Player.AddGauge(50) #Adding 50 SoulGauge

    if Player.DeathDesignTimer <= 0:
        #If not already applied
        Player.buffList.append(DeathDesignBuff) #10% bonus
        Player.EffectCDList.append(DeathDesignCheck)
    Player.DeathDesignTimer = min(60, Player.DeathDesignTimer + 30) #max of 60


def ApplyHarvestMoon(Player, Enemy):
    Player.Soulsow = False #Uses SoulSow

def ApplySoulsow(Player, Enemy):
    Player.Soulsow = True

#Effect

def SliceCombo(Player, Spell):
    if Spell.id == WaxingSlice.id:
        if not (WaxingSliceCombo in Player.EffectList) : 
            Player.EffectList.append(WaxingSliceCombo)
        Player.EffectToRemove.append(SliceCombo)
        Spell.Potency += 240
        Player.AddGauge(10) #add 10 soul gauge

def WaxingSliceCombo(Player, Spell):
    if Spell.id == InfernalSlice.id:
        Spell.Potency += 320
        Player.EffectToRemove.append(WaxingSliceCombo)
        Player.AddGauge(10) #Add 10 soul gauge


def VoidReapingEffect(Player, Spell):
    if Spell.id == CrossReaping.id:
        Spell.Potency += 60
        Player.VoidReapingTimer = 0

def CrossReapingEffect(Player, Spell):
    if Spell.id == VoidReaping.id:
        Spell.Potency += 60
        Player.CrossReapingTimer = 0

def GibbetEffect(Player, Spell):
    if Spell.id == Gallows.id:
        Spell.Potency += 60
        Player.GibbetEffectTimer = 0

def GallowsEffect(Player, Spell):
    if Spell.id == Gibbet.id:
        Spell.Potency += 60
        Player.GallowsEffectTimer = 0

#check

def VoidReapingCheck(Player, Enemy):
    if Player.VoidReapingTimer <= 0:
        Player.EffectList.remove(VoidReapingEffect)
        Player.EffectToRemove.append(VoidReapingCheck)

def CrossReapingCheck(Player, Enemy):
    if Player.CrossReapingTimer <= 0:
        Player.EffectList.remove(CrossReapingEffect)
        Player.EffectToRemove.append(CrossReapingCheck)

def GibbetCheck(Player, Enemy):
    if Player.GibbetEffectTimer <= 0:
        Player.EffectList.remove(GibbetEffect)
        Player.EffectToRemove.append(GibbetCheck)

def GallowsCheck(Player, Enemy):
    if Player.GallowsEffectTimer <= 0:
        Player.EffectList.remove(GallowsEffect)
        Player.EffectCDList.append(GallowsCheck)

def SoulSliceStackCheck(Player, Enemy):
    if Player.SoulSliceCD <= 0:
        if Player.SoulSliceStack == 1:
            Player.EffectToRemove.append(SoulSliceStackCheck)
        else:
            Player.SoulSliceCD = 30
        Player.SoulSliceStack += 1

def DeathDesignCheck(Player, Enemy):
    if Player.DeathDesignTimer <= 0:
        Player.buffList.remove(DeathDesignBuff)
        Player.EffectToRemove.append(DeathDesignCheck)

#GCD

#Combo Actions
Slice = ReaperSpell(15, True, Lock, 2.5, 300, ApplySlice, [], True)
WaxingSlice = ReaperSpell(16, True, Lock, 2.5, 140, empty, [], True)
InfernalSlice = ReaperSpell(17, True, Lock, 2.5, 140, empty, [], True)

#Other GCD
Soulsow = ReaperSpell(1, True, 5, 2.5, 0, ApplySoulsow, [], False)
HarvestMoon = ReaperSpell(2, True, Lock, 2.5, 600, ApplyHarvestMoon, [HarvestMoonRequirement], False)
Harpe = ReaperSpell(3, True, 1.3, 2.5, 2.5, empty, [], False)
ShadowOfDeath = ReaperSpell(4, True, Lock, 2.5, 300, ApplyShadowOfDeath, [], True)
SoulSlice = ReaperSpell(5, True, Lock, 2.5, 460, ApplySoulSlice, [SoulSliceRequirement], True)
Gibbet = ReaperSpell(8, True, Lock, 2.5, 460, ApplyGibbet, [GibbetRequirement], True)
Gallows = ReaperSpell(9, True, Lock, 2.5, 460, ApplyGallows, [GibbetRequirement], True) #shares same requirement as Gibbet
PlentifulHarvest = ReaperSpell(10, True, Lock, 2.5, 520, ApplyPlentifulHarvest, [PlentifulHarvestRequirement], True)
VoidReaping = ReaperSpell(12, True, Lock, 1.5, 460, ApplyVoidReaping, [VoidReapingRequirement], True)
CrossReaping = ReaperSpell(13, True, Lock, 1.5, 460, ApplyCrossReaping, [VoidReapingRequirement], True) #Same Requriement as VoidReaping
Communio = ReaperSpell(14, True, 1.3, 2.5, 1000, ApplyCommunio, [CommunioRequirement], False)
#oGCD
ArcaneCircle = ReaperSpell(6, False, Lock, 0, 0, ApplyArcaneCircle, [ArcaneCircleRequirement], False)
Gluttony = ReaperSpell(7, False, Lock, 0, 500, ApplyGluttony, [GluttonyRequirement], False)
Enshroud = ReaperSpell(11, False, Lock, 0, 0, ApplyEnshroud, [EnshroudRequirement], False)
LemureSlice = ReaperSpell(14, False, Lock, 0, 200, ApplyLemureSlice, [LemureSliceRequirement], False)
BloodStalk = ReaperSpell(18, False, Lock, 0, 340, ApplyBloodStalk, [BloodStalkRequirement], False)
UnveiledGibbet = ReaperSpell(19, False, Lock, 0, 400, ApplyUnveiledGibbed, [UnveiledGibbetRequirment], False)
UnveiledGallows = ReaperSpell(20, False, Lock, 0, 400, ApplyUnveiledGibbet, [UnveiledGallowsRequirment], False) #Shares effect with Gibbet
#buff
DeathDesignBuff = buff(1.1)
ArcaneCircleBuff = buff(1.03)