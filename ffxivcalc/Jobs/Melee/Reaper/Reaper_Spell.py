from ffxivcalc.Jobs.Base_Spell import buff, empty
from ffxivcalc.Jobs.Melee.Melee_Spell import ReaperSpell
Lock = 0

#Requirement

def SoulsowRequirement(Player, Spell):
    # This requirement will only serve to make the casting instant if the fight is not started
    if not Player.CurrentFight.FightStart:
        Spell.CastTime = 0
    return True, -1

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
    #input(Player.SoulReaverStack > 0)
    #input(Player.AvatarTimer == 0)
    return Player.SoulReaverStack > 0 and Player.AvatarTimer == 0, -1

def PlentifulHarvestRequirement(Player, Spell):

    #Will modify Spell's potency depending on ImmortalStack, will add 35 potency for each stack, for a max of 800
    #input(Player.ImmortalSacrificeStack)
    Spell.Potency += (Player.ImmortalSacrificeStack - 1) * 40 #Removing minimal requirement, which is 1 stack
    #input("Potency of plentiful is : " + str(Spell.Potency))

    return Player.ImmortalSacrificeStack > 0 and Player.BloodsownTimer == 0, Player.BloodsownTimer

def EnshroudRequirement(Player, Spell):
    #input(Player.EnshroudCD <= 0)
    #input(Player.ShroudGauge)
    return Player.EnshroudCD <= 0 and Player.ShroudGauge >= 50, Player.EnshroudCD


def VoidReapingRequirement(Player, Spell):
    return Player.AvatarTimer > 0 and Player.LemureGauge > 0, -1

def LemureSliceRequirement(Player, Spell):
    return Player.VoidShroudGauge > 1, -1

def CommunioRequirement(Player, Spell):
    return Player.LemureGauge > 0, -1

def UnveiledGibbetRequirement(Player, Spell):
    return Player.EnhancedGibbet, -1

def UnveiledGallowsRequirement(Player, Spell):
    return Player.EnhancedGallows, -1

def HellIngressRequirement(Player, Spell):
    return Player.HellIngressCD <= 0, Player.HellIngressCD

def ArcaneCrestRequirement(Player, Spell):
    return Player.ArcaneCrestCD <= 0, Player.ArcaneCrestCD

#Apply

def ApplyGrimReaping(Player, Enemy):
    Player.LemureGauge -= 1
    Player.VoidShroudGauge = min(5, Player.VoidShroudGauge + 1)

def ApplyGuillotine(Player, Enemy):
    Player.AddShroud(10)

def ApplyArcaneCrest(Player, Enemy):
    Player.ArcaneCrestCD = 30

def ApplySpinningScythe(Player, Enemy):
    Player.AddGauge(10)
    if not (SpinningScytheCombo in Player.EffectList) : Player.EffectList.append(SpinningScytheCombo)

def ApplyHellIngress(Player, Enemy):
    if not (HellIngressEffect in Player.EffectList):
        Player.EffectList.append(HellIngressEffect)
        Player.EffectCDList.append(HellIngressCheck)
    Player.HellIngressCD = 20
    Player.HellIngressTimer = 20

def ApplyUnveiledGibbet(Player, Enemy):
    Player.AddGauge(-50) #Removing 50 Soul gauge
    Player.SoulReaverStack = 1

    #Since SoulReaver stack are removed if any other ability is done, we will add an effect that will check for that
    Player.EffectList.append(SoulReaverEffect)

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
    Player.ImmortalSacrificeStack = 0


def ApplyGibbet(Player, Enemy):
    if not Player.EnhancedGallows : 
        Player.EffectList.append(GibbetEffect) #Buffs next Gallows
        Player.EffectCDList.append(GibbetCheck)
        Player.EnhancedGallows = True
        #input("Giving enhanced Gallows")
    Player.AddShroud(10) #Add 10 ShroudGauge
    Player.GibbetEffectTimer = 60
    Player.SoulReaverStack -= 1 #Removing a stack

def ApplyGallows(Player, Enemy):
    if not Player.EnhancedGibbet : 
        Player.EffectList.append(GallowsEffect) #Buff next Gibbet
        Player.EffectCDList.append(GallowsCheck)
        Player.EnhancedGibbet = True
        #input("Giving enhanced Gibbet")
    Player.AddShroud(10) #Add 10 Shroud Gauge
    Player.GallowsEffectTimer = 60
    Player.SoulReaverStack -= 1 #Removing a stack

def ApplyBloodStalk(Player, Enemy):
    Player.AddGauge(-50) #Removing 50 Soul Gauge
    Player.SoulReaverStack = 1 #Reset to 1
    #Since SoulReaver stack are removed if any other ability is done, we will add an effect that will check for that
    Player.EffectList.append(SoulReaverEffect)


def ApplyGluttony(Player, Enemy):
    Player.AddGauge(-50) #Removing 50 Soul Gauge
    Player.GluttonyCD = 60
    Player.SoulReaverStack += 2
    #Since SoulReaver stack are removed if any other ability is done, we will add an effect that will check for that
    Player.EffectList.append(SoulReaverEffect)


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
            Player.ImmortalSacrificeStack = min(8, Player.ImmortalSacrificeStack + 1)#Giving one stack
            Target.EffectToRemove.append(CircleOfSacrificeEffet)
            Target.EffectCDList.remove(CircleOfSacrificeCheck) #Removing check and effect, since max of 1 per player

    def CircleOfSacrificeCheck(Target, Enemy):
        if Player.CircleOfSacrificeTimer <= 0: #If no more time, we remove
            Target.EffectList.remove(CircleOfSacrificeEffet)
            Target.EffectToRemove.append(CircleOfSacrificeCheck)

    for player in Player.CurrentFight.PlayerList:
        #input("Given effect to : " + str(player))
        player.EffectList.append(CircleOfSacrificeEffet) #Giving the effect to all players in the fight
        player.EffectCDList.append(CircleOfSacrificeCheck)

    

def ApplySoulSlice(Player, Enemy):
    Player.AddGauge(50) #Adding 50 SoulGauge
    if Player.SoulSliceStack == 2: #If max stack, we add check
        Player.EffectCDList.append(SoulSliceStackCheck)
        Player.SoulSliceCD = 30
    Player.SoulSliceStack -= 1

def ApplyShadowOfDeath(Player, Enemy):
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

def SpinningScytheCombo(Player, Spell):
    if Spell.id == NightmareScythe.id:
        Spell.Potency += 60
        Player.AddGauge(10)
        Player.EffectToRemove.append(SpinningScytheCombo)

def HellIngressEffect(Player, Spell):
    if Spell.id == Harpe.id:
        Spell.CastTime = Lock #Insta Cast
        Player.HellIngressTimer = 0

def SoulReaverEffect(Player, Spell):
    #Will check if Spell is Gibbet or Gallows, if it is not we will remove SoulReaverStack
    if Spell.GCD and Spell.id != Gibbet.id and Spell.id != Gallows.id:
        #If not, we remove SoulReaverStack
        Player.SoulReaverStack = 0

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
        #input("Buffing Gallows")
        Spell.Potency += 60
        Player.GibbetEffectTimer = 0
        Player.EnhancedGallows = False

def GallowsEffect(Player, Spell):
    if Spell.id == Gibbet.id:
        #input("Buffing Gibbet")
        Spell.Potency += 60
        Player.GallowsEffectTimer = 0
        Player.EnhancedGibbet = False

#check

def HellIngressCheck(Player, Enemy):
    if Player.HellIngressTimer <= 0:
        Player.EffectList.remove(HellIngressEffect)
        Player.EffectToRemove.append(HellIngressCheck)

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
        #input("Removing enhanced gallows")

def GallowsCheck(Player, Enemy):
    if Player.GallowsEffectTimer <= 0:
        Player.EffectList.remove(GallowsEffect)
        Player.EffectToRemove.append(GallowsCheck)
        #input("Removing enhanced gibbet")

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
Slice = ReaperSpell(24373, True, Lock, 2.5, 300, ApplySlice, [], True, type = 2)
WaxingSlice = ReaperSpell(24374, True, Lock, 2.5, 140, empty, [], True, type = 2)
InfernalSlice = ReaperSpell(24375, True, Lock, 2.5, 140, empty, [], True, type = 2)

#Other GCD
Soulsow = ReaperSpell(24387, True, 5, 2.5, 0, ApplySoulsow, [SoulsowRequirement], False, type = 1)
HarvestMoon = ReaperSpell(24388, True, Lock, 2.5, 600, ApplyHarvestMoon, [HarvestMoonRequirement], False, type = 1)
Harpe = ReaperSpell(24386, True, 1.3, 2.5, 300, empty, [], False, type = 1)
ShadowOfDeath = ReaperSpell(24378, True, Lock, 2.5, 300, ApplyShadowOfDeath, [], True, type = 2)
SoulSlice = ReaperSpell(24380, True, Lock, 2.5, 460, ApplySoulSlice, [SoulSliceRequirement], True, type = 2)
Gibbet = ReaperSpell(24382, True, Lock, 2.5, 460, ApplyGibbet, [GibbetRequirement], True, type = 2)
Gallows = ReaperSpell(24383, True, Lock, 2.5, 460, ApplyGallows, [GibbetRequirement], True, type = 2) #shares same requirement as Gibbet
PlentifulHarvest = ReaperSpell(24385, True, Lock, 2.5, 720, ApplyPlentifulHarvest, [PlentifulHarvestRequirement], True, type = 2)
VoidReaping = ReaperSpell(24395, True, Lock, 1.5, 460, ApplyVoidReaping, [VoidReapingRequirement], True, type = 2)
CrossReaping = ReaperSpell(24396, True, Lock, 1.5, 460, ApplyCrossReaping, [VoidReapingRequirement], True, type = 2) #Same Requriement as VoidReaping
Communio = ReaperSpell(24398, True, 1.3, 2.5, 1100, ApplyCommunio, [CommunioRequirement], False, type = 1)

#oGCD
ArcaneCircle = ReaperSpell(24405, False, Lock, 0, 0, ApplyArcaneCircle, [ArcaneCircleRequirement], False)
Gluttony = ReaperSpell(24393, False, Lock, 0, 500, ApplyGluttony, [GluttonyRequirement], False)
Enshroud = ReaperSpell(24394, False, Lock, 0, 0, ApplyEnshroud, [EnshroudRequirement], False)
LemureSlice = ReaperSpell(24399, False, Lock, 0, 220, ApplyLemureSlice, [LemureSliceRequirement], False)
BloodStalk = ReaperSpell(24389, False, Lock, 0, 340, ApplyBloodStalk, [BloodStalkRequirement], False)
UnveiledGibbet = ReaperSpell(24390, False, Lock, 0, 400, ApplyUnveiledGibbet, [UnveiledGibbetRequirement], False)
UnveiledGallows = ReaperSpell(24391, False, Lock, 0, 400, ApplyUnveiledGibbet, [UnveiledGallowsRequirement], False) #Shares effect with Gibbet
HellIngress = ReaperSpell(24402, False, Lock, 0, 0, ApplyHellIngress, [HellIngressRequirement], False)
ArcaneCrest = ReaperSpell(24404, False, 0, 0, 0, ApplyArcaneCrest, [ArcaneCrestRequirement], False)
#AOE GCD
SpinningScythe = ReaperSpell(24376, True, 0, 2.5, 140, ApplySpinningScythe, [], True, type = 2)
NightmareScythe = ReaperSpell(24377, True, 0, 2.5, 120, empty, [], True, type = 2)
WhorlOfDeath = ReaperSpell(24379, True, 0, 2.5, 100, ApplyShadowOfDeath, [], False, type = 2)
Guillotine = ReaperSpell(24384, False, 0, 0, 200, ApplyGuillotine, [GibbetRequirement], True, type = 2) #AOE version of Gallows/Gibbet
#AOE oGCD
GrimSwathe = ReaperSpell(24392, False, 0, 0, 140, ApplyBloodStalk, [BloodStalkRequirement], False) #AOE version of bloodstalk
SoulScythe = ReaperSpell(24381, False, 0, 0, 180, ApplySoulSlice, [SoulSliceRequirement], False) #AOE version of SoulSlice
GrimReaping = ReaperSpell(24397, True, 0, 2.5,200, ApplyGrimReaping, [VoidReapingRequirement], False)
LemureScythe = ReaperSpell(24400, False, 0, 0, 100, ApplyLemureSlice, [LemureSliceRequirement], False) #AOE version of Lemure Slice
#buff
DeathDesignBuff = buff(1.1)
ArcaneCircleBuff = buff(1.03)

ReaperAbility = {
24373 : Slice,
24374 : WaxingSlice,
24375 : InfernalSlice,
24378 : ShadowOfDeath,
24380 : SoulSlice,
24382 : Gibbet,
24383 : Gallows,
24376 : SpinningScythe,
24377 : NightmareScythe,
24379 : WhorlOfDeath,
24381 : SoulScythe,
24384 : Guillotine,
24389 : BloodStalk,
24390 : UnveiledGibbet,
24391 : UnveiledGallows,
24392 : GrimSwathe,
24393 : Gluttony,
24387 : Soulsow,
24388 : HarvestMoon,
24385 : PlentifulHarvest,
24394 : Enshroud,
24395 : VoidReaping,
24396 : CrossReaping,
24397 : GrimReaping,
24399 : LemureSlice,
24400 : LemureScythe,
24398 : Communio,
24404 : ArcaneCrest,
24405 : ArcaneCircle,
24402 : HellIngress,
24401 : HellIngress,
24386 : Harpe
}