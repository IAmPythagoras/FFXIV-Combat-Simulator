#########################################
########## DARK KNIGHT SKILLS ###########
#########################################
from Jobs.Base_Spell import DOTSpell, Potion, buff, empty
import copy
from Jobs.Tank.DarkKnight.DarkKnight_Player import Esteem
from Jobs.Tank.Tank_Spell import BigMit, DRKSkill
Lock = 0

#def DarksideEffect(Player, Spell):
 #   if Player.DarksideTimer > 0:
  #      Spell.Potency *= 1.10

#Requirements for each Skill and Ability.

def BloodRequirement(Player, Spell):
    #print("Delirium stacks: "+ str(Player.DeliriumStacks))
    if Player.DeliriumStacks > 0 and (Spell.id == Bloodspiller.id or Spell.id == Quietus.id):
        Spell.BloodCost = 0
        Player.DeliriumStacks -= 1
        return True, -1
    elif Player.Blood >= 50:
        Player.Blood -= 50
        return True, -1
    return True, -1

def EdgeShadowRequirement(Player, Spell):
    if Player.EdgeShadowCD <= 0 :
        if Player.DarkArts:
            Spell.ManaCost = 0
            Player.DarkArts = False
            return True, -1
        elif Player.Mana >= Spell.ManaCost:
            Player.Mana -= Spell.ManaCost
            return True, -1
        return True, -1
    return False, -1

def BloodWeaponRequirement(Player, Spell):
    return Player.BloodWeaponCD <= 0, Player.BloodWeaponCD

def DeliriumRequirement(Player, Spell):
    return Player.DeliriumCD <= 0, Player.DeliriumCD

def CarveSpitRequirement(Player, Spell):
    return Player.CarveSpitCD <= 0, Player.CarveSpitCD

def AbyssalDrainRequirement(Player, Spell):
    return Player.AbyssalDrainCD <= 0, Player.AbyssalDrainCD

def SaltedEarthRequirement(Player, Spell):
    return Player.SaltedEarthCD <= 0, Player.SaltedEarthCD

def SaltDarknessRequirement(Player, Spell):
    return Player.SaltedEarthTimer > 0, -1

def ShadowbringerRequirement(Player, Spell):
    return Player.DarksideTimer > 0 and Player.ShadowbringerCharges > 0, -1


def PlungeRequirement(Player, Spell):
    return Player.PlungeCharges > 0, Player.PlungeCD

def TBNRequirement(Player, Spell):
    if Player.Mana >= Spell.ManaCost:
        Player.Mana -= Spell.ManaCost
        return True, -1
    return True, -1

def LivingDeadRequirement(Player, Spell):
    return Player.LivingDeadCD <= 0, Player.LivingDeadCD

def DarkMindRequirement(Player, Spell):
    return Player.DarkMindCD <= 0, Player.DarkMindCD

def DarkMissionaryRequirement(Player, Spell):
    return Player.DarkMissionaryCD <= 0, Player.DarkMissionaryCD

def OblationRequirement(Player, Spell):
    return Player.OblationStack > 0, Player.OblationCD

#Effect functions that persist after action use

def BloodWeaponEffect(Player, Spell):
    #print("Blood Weapon active")
    if Spell.GCD:
        Player.Mana = min(Player.Mana + 600, 10000)
        Player.Blood = min(100, Player.Blood + 10)

def DeliriumEffect(Player, Spell):
    #print("Delirium active")
    if Spell.id == Bloodspiller.id:
        Player.Mana = min(Player.Mana + 200, 10000)
    elif Spell.id == Quietus.id:
        Player.Mana = min(Player.Mana + 500, 10000)

def HardSlashEffect(Player, Spell):
    if Spell.id == 2:
        Multiplier = Spell.Potency/120
        BonusDmg = 140 * Multiplier
        Spell.Potency += BonusDmg
        Player.Mana = min(Player.Mana + 600, 10000)
    if (Spell.id == SyphonStrike.id) or (Spell.id == Souleater.id) or (Spell.id == HardSlash.id):
        Player.EffectToRemove.append(HardSlashEffect)

def SyphonStrikeEffect(Player, Spell):
    if Spell.id == Souleater.id:
        Multiplier = Spell.Potency/120
        BonusDmg = 220 * Multiplier
        Spell.Potency += BonusDmg
        Player.Blood = min(100, Player.Blood + 20)
    if (Spell.id == SyphonStrike.id) or (Spell.id == Souleater.id) or (Spell.id == HardSlash.id):
        Player.EffectToRemove.append(SyphonStrikeEffect)

#Cooldown checks to remove effect and restore charges

def OblationStackCheck(Player, Spell):
    if Player.OblationCD <= 0:
        if Player.OblationStack == 1:
            Player.EffectToRemove.append(OblationStackCheck)
        else:
            Player.OblationCD = 60
        Player.OblationStack += 1

def BloodWeaponCheck(Player, Spell):
    if Player.BloodWeaponTimer <= 0 or Player.BloodWeaponStacks == 0:
        Player.EffectList.remove(BloodWeaponEffect)
        Player.EffectToRemove.append(BloodWeaponCheck)

def DeliriumCheck(Player, Spell):
    if Player.DeliriumTimer <= 0 or Player.DeliriumStacks == 0:
        Player.EffectList.remove(DeliriumEffect)
        Player.EffectToRemove.append(DeliriumCheck)

def SaltedEarthCheck(Player, Spell):
    if Player.SaltedEarthTimer <= 0:
        Player.DOTList.remove(Player.SaltedEarthDOT)
        Player.SaltedEarthDOT = None
        Player.SaltedEarthTimer = 0
        Player.EffectToRemove.append(SaltedEarthCheck)

def CheckShadowbringerCharge(Player, Enemy):
    if Player.ShadowbringerCD <= 0:
        if Player.ShadowbringerCharges == 0:
            Player.ShadowbringerCD = 30
        if Player.ShadowbringerCharges == 1:
            Player.EffectToRemove.append(CheckShadowbringerCharge)
        Player.ShadowbringerCharges +=1

def CheckPlungeCharge(Player, Enemy):
    if Player.PlungeCD <= 0:
        if Player.PlungeCharges == 0:
            Player.PlungeCD = 30
        if Player.PlungeCharges == 1:
            Player.EffectToRemove.append(CheckPlungeCharge)
        Player.PlungeCharges +=1

def UnleashCombo(Player, Spell):
    if Spell.id == StalwartSoul.id:
        Spell.Potency += 40
        Player.Blood = min(100, Player.Blood + 20)


#Apply effects that happen upon action use

def ApplyLivingDead(Player, Enemy):
    Player.LivingDeadCD = 300

def ApplyUnleash(Player, Spell):
    if not (UnleashCombo in Player.EffectList) : Player.EffectList.append(UnleashCombo)

def ApplyHardSlashEffect(Player, Spell):
    Player.EffectList.append(HardSlashEffect)

def ApplySyphonEffect(Player, Spell):
    Player.EffectList.append(SyphonStrikeEffect)

def ApplyBloodWeaponEffect(Player, Spell):
    Player.BloodWeaponCD = 60                     
    Player.EffectList.append(BloodWeaponEffect)
    Player.BloodWeaponStacks = 5
    Player.BloodWeaponTimer = 15
    Player.EffectCDList.append(BloodWeaponCheck)

def ApplyDeliriumEffect(Player, Spell):
    Player.DeliriumCD = 60
    Player.EffectList.append(DeliriumEffect)
    Player.DeliriumStacks = 3
    Player.DeliriumTimer = 30 
    Player.EffectCDList.append(DeliriumCheck)

def ApplyEdgeShadowEffect(Player, Spell):
    Player.DarksideTimer = min(60, Player.DarksideTimer + 30)
    if not (CheckEdgeShadow in Player.EffectCDList):
        Player.buffList.append(EdgeShadowBuff)
        Player.EffectCDList.append(CheckEdgeShadow)

def CheckEdgeShadow(Player, Enemy):
    if Player.DarksideTimer <= 0:
        Player.buffList.remove(EdgeShadowBuff)
        Player.EffectCDList.remove(CheckEdgeShadow)

def ApplyCarveSpitEffect(Player, Spell):
    Player.CarveSpitCD = 60
    Player.AbyssalDrainCD = 60
    Player.Mana = min(Player.Mana + 600, 10000)

def ApplyAbyssalDrainEffect(Player, Spell):
    Player.AbyssalDrainCD = 60
    Player.CarveSpitCD = 60

def ApplySaltedEarth(Player, Spell):
    Player.SaltedEarthCD = 90
    Player.SaltedEarthTimer = 15
    Player.SaltedEarthDOT = copy.deepcopy(SaltedEarthDOT)
    Player.DOTList.append(Player.SaltedEarthDOT)
    Player.EffectCDList.append(SaltedEarthCheck)

def ApplySaltDarknessEffect(Player, Spell):
    Player.SaltDarknessCD = 15

def SpendShadowbringer(Player, Spell):
    if Player.ShadowbringerCharges == 2 :
        Player.ShadowbringerCD = 60
    Player.ShadowbringerCharges -= 1
    Player.EffectCDList.append(CheckShadowbringerCharge)

def SummonLivingShadow(Player, Spell):
    Actions = [PDelay, PAbyssalDrain, PPlunge, PQuietus, PShadowbringer, PEdgeShadow, PBloodspiller, PCarveSpit]
    Pet = Esteem(2.5,Actions,[],[],Player.CurrentFight,Player)
    Player.CurrentFight.PlayerList.append(Pet)
    Player.EsteemPointer = Pet
    #print("Esteem enters the battlefield.")

def SpendPlunge(Player,Spell):
    if Player.PlungeCharges == 2 :
        Player.PlungeCD = 30
    Player.PlungeCharges -= 1
    Player.EffectCDList.append(CheckPlungeCharge)

def ApplyDarkArts(Player, Spell):
    Player.DarkArts = True

def ApplyDarkMind(Player, Spell):
    Player.DarkMindCD = 60

def ApplyDarkMissionary(Player, Enemy):
    Player.DarkMissionaryCD = 90

def ApplyOblation(Player, Enemy):
    if Player.OblationStack == 2:
        Player.EffectCDList.append(OblationStackCheck)
        Player.OblationCD = 60
    Player.OblationStack -= 1

#List of Weaponskills and Spells used by a Dark Knight Player.
DRKGCD = 2.5         #GCD speed
Lock = 0            #Fixed value for animation lock.

HardSlash = DRKSkill(3617, True, Lock, DRKGCD, 170, 0, 0, ApplyHardSlashEffect, [])
SyphonStrike = DRKSkill(3623, True, Lock, DRKGCD, 120, 0, 0, ApplySyphonEffect, [])
Souleater = DRKSkill(3632, True, Lock, DRKGCD, 120, 0, 0, empty, [])
Bloodspiller = DRKSkill(7392, True, Lock, DRKGCD, 500, 0, 50, empty, [BloodRequirement])
Quietus = DRKSkill(5, True, Lock, DRKGCD, 200, 0, 50, empty, [BloodRequirement])
Unmend = DRKSkill(3624, True, Lock, 2.50, 150, 0, 0, empty, [])

#List of Buffs used by a Dark Knight Player.

BloodWeapon = DRKSkill(3625, False, Lock, 0, 0, 0, 0, ApplyBloodWeaponEffect, [BloodWeaponRequirement])
Delirium = DRKSkill(7390, False, Lock, 0, 0, 0, 0, ApplyDeliriumEffect, [DeliriumRequirement])

#List of Abilities used by a Dark Knight Player.

EdgeShadow = DRKSkill(16470, False, Lock, 0, 460, 3000, 0, ApplyEdgeShadowEffect, [EdgeShadowRequirement])
FloodShadow = DRKSkill(10, False, Lock, 0, 160, 3000, 0, ApplyEdgeShadowEffect, [EdgeShadowRequirement])
CarveSpit = DRKSkill(3643, False, Lock, 0, 510, 0, 0, ApplyCarveSpitEffect, [CarveSpitRequirement])
AbyssalDrain = DRKSkill(12, False, Lock, 0, 150, 0, 0, ApplyAbyssalDrainEffect, [AbyssalDrainRequirement])
SaltedEarth = DRKSkill(3639, False, Lock, 0, 50, 0, 0, ApplySaltedEarth, [SaltedEarthRequirement]) #Ground target DOT, ticks once upon placement.
SaltedEarthDOT = DOTSpell(14, 50, True)
SaltDarkness = DRKSkill(25755, False, Lock, 0, 500, 0, 0, empty, [SaltDarknessRequirement])
Shadowbringer = DRKSkill(25757, False, Lock, 0, 600, 0, 0, SpendShadowbringer, [ShadowbringerRequirement])
LivingShadow = DRKSkill(16472, False, Lock, 0, 0, 0, 50, SummonLivingShadow, [BloodRequirement])
Plunge = DRKSkill(3640, False, Lock, 0, 150, 0, 0, SpendPlunge, [PlungeRequirement])

TBN = DRKSkill(7393, False, Lock, 0, 0, 3000, 0, ApplyDarkArts, [TBNRequirement])     #Simply makes the next EdgeShadow free for now.

#AOE GCD
Unleash = DRKSkill(20, True, 0, 2.5, 120, 0, 0, ApplyUnleash, [])
StalwartSoul = DRKSkill(21, True, 0, 2.5, 100, 0, 0, empty, [])
#List of Abilities performed by Living Shadow.

PAbyssalDrain = DRKSkill(22, True, 0.5, 2.5, 300, 0, 0, empty, [])
PPlunge = DRKSkill(23, True, 0.5, 2.5, 300, 0, 0, empty, [])
PQuietus = DRKSkill(24, True, 0.5, 2.5, 300, 0, 0, empty, [])
PShadowbringer = DRKSkill(25, True, 0.5, 2.5, 450, 0, 0, empty, [])
PEdgeShadow = DRKSkill(26, True, 0.5, 2.5, 300, 0, 0, empty, [])
PBloodspiller = DRKSkill(27, True, 0.5, 2.5, 300, 0, 0, empty, [])
PCarveSpit = DRKSkill(28, True, 0.5, 2.5, 300, 0, 0, empty, [])
PDelay = DRKSkill(29, True, 0, 4.50, 0, 0, 0, empty, [])    #6s animation before it starts attacking.

#Mit
LivingDead = DRKSkill(3638, False, 0, 0, 0, 0, 0, ApplyLivingDead, [LivingDeadRequirement])
DarkMind = DRKSkill(3634, False, 0, 0, 0, 0, 0, ApplyDarkMind, [DarkMindRequirement])
DarkMissionary = DRKSkill(16471, False, 0, 0, 0, 0, 0, ApplyDarkMissionary, [DarkMissionaryRequirement])
Oblation = DRKSkill(25754, False, 0, 0, 0, 0, 0, ApplyOblation, [OblationRequirement])
#buff
EdgeShadowBuff = buff(1.1)

# Maps Ability IDs from FFlogs to Skill objects
# Not exhaustive: If an ability is missing, check log for id and add it into the mapping.
DarkKnightAbility = {
    3617: HardSlash,
    3623: SyphonStrike,
    3624: Unmend,
    3625: BloodWeapon,
    3632: Souleater,
    3634: DarkMind,
    3636: BigMit,
    3638: LivingDead,
    3639: SaltedEarth,
    3640: Plunge,
    3643: CarveSpit,
    7390: Delirium,
    7392: Bloodspiller,
    7393: TBN,
    16470: EdgeShadow,
    16471: DarkMissionary,
    16472: LivingShadow,
    #17904: PAbyssalDrain,
    #17905: PPlunge,
    #17906: PQuietus,
    #17908: PEdgeShadow,
    #17909: PBloodspiller,
    #17915: PCarveSpit,
    #25881: PShadowbringer,
    25754: Oblation,
    25755: SaltDarkness,
    25757: Shadowbringer,
    34590541: Potion  # This is assumed to be strength pot grade 6
}