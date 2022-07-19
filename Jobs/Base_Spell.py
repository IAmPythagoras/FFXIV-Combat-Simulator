import copy

from Fight import ComputeDamage
import math
from Jobs.Caster.Summoner.Summoner_Player import BigSummon
from Jobs.Melee.Ninja.Ninja_Player import Shadow
from Jobs.Ranged.Machinist.Machinist_Player import Queen
from Jobs.Tank.DarkKnight.DarkKnight_Player import Esteem
Lock = 0.75

class FailedToCast(Exception):#Exception called if a spell fails to cast
    pass


class buff:
    def __init__(self, MultDPS):
        self.MultDPS = MultDPS #DPS multiplier of the buff


class Spell:
    #This class is any Spell, it will have some subclasses to take Job similar spell, etc.

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, Requirement):
        self.id = id
        self.GCD = GCD #True if GCD
        self.Potency = Potency
        self.ManaCost = ManaCost
        self.CastTime = CastTime
        self.RecastTime = RecastTime
        self.Effect = [Effect]
        self.Requirement = Requirement
        self.DPSBonus = 1

    def Cast(self, player, Enemy):
        #This function will cast the spell given by the Fight, it will apply whatever effects it has and do its potency

        #if self.GCD: 
        #    print("Spell is casted: " + str(self.id))
        #    input("timestamp : " + str(player.CurrentFight.TimeStamp) )

        tempSpell = copy.deepcopy(self)
        #Creating a tempSpell which will have its values changed according that what effect
        #the player and the enemy have
        #Will apply each effect the player currently has on the spell
        if self.id != -1: #id = -1 is WaitAbility, we don't want anything with that
            for Effect in player.EffectList:
                Effect(player, tempSpell)#Changes tempSpell
            for Effect in Enemy.EffectList:
                Effect(player, tempSpell)#Changes tempSpell
        #Checks if we meet the spell requirement
        ##input("out of effect")

        #Remove all effects that have to be removed

        for remove in player.EffectToRemove:
            player.EffectList.remove(remove) #Removing effect
        for add in player.EffectToAdd:
            player.EffectList.append(add)
        
        player.EffectToRemove = [] #Empty the remove list
        player.EffectToAdd = []
        ##input("id : " + str(self.id))
        for Requirement in tempSpell.Requirement:
            ##input("in requirement")
            ##input("tenchijind : " + str(player.TenChiJinTimer))
            ##input(Requirement.__name__)
            ableToCast, timeLeft = Requirement(player, tempSpell)
            if(not ableToCast) : #Requirements return both whether it can be casted and will take away whatever value needs to be reduced to cast
                ##input("timeleft : " + str(timeLeft))
                #Will check if timeLeft is within a margin, so we will just wait for it to come
                #timeLeft is the remaining time before the spell is available
                if timeLeft <= 5 and timeLeft > 0: #Limit of waiting for 1 sec
                    tempSpell = WaitAbility(timeLeft + 0.01)
                    player.ActionSet.insert(player.NextSpell, tempSpell)
                    return tempSpell #Makes the character wait
                    #Might remove some stuff tho, might have to check into that (for when effects are applied)
                


                print("Failed to cast the spell : " + str(self.id))
                print("The Requirement that failed was : " + str(Requirement.__name__))
                print("The timestamp is : " + str(player.CurrentFight.TimeStamp))
                raise FailedToCast("Failed to cast the spell")
        #Will make sure CastTime is at least Lock
        if tempSpell.id > 0 and tempSpell.CastTime < Lock : tempSpell.CastTime = 0.5 #id < 0 are special abilities like DOT, so we do not want them to be affected by that
        return tempSpell
        #Will put casting spell in player, and do damage/effect once the casting time is over


    def CastFinal(self, player, Enemy):
        ##print("##################################")
        ##print("Potency of spell: " + str(self.Potency))
        #if self.GCD: 
        #    input("Recast is  "+ str(self.RecastTime))

        
        for Effect in self.Effect:
            Effect(player, Enemy)#Put effects on Player and/or Enemy
        #This will include substracting the mana (it has been verified before that the mana was enough)
        
        ##print("Current MP: " + str(player.Mana))
        ##print("Current Blood: " + str(player.Blood))
        type = 0 #Default value for type
        if isinstance(self, DOTSpell): #Then dot
            #We have to figure out if its a physical dot or not
            if self.isPhysical: type = 2
            else: type = 1
        elif isinstance(self, Auto_Attack):
            type = 3   
        
        if self.Potency != 0 : minDamage,Damage= ComputeDamage(player, self.Potency, Enemy, self.DPSBonus, type, self)    #Damage computation
        else: minDamage, Damage = 0,0
        ##input("Damage : " + str(Damage))
        ##input("Damage from v1.0 " + str(ComputeDamageV2(player, self.Potency, 1, 1)))

        #input("Adding " + str(self.Potency) + " to player : " + str(player))

        if isinstance(player, Queen) or isinstance(player, Esteem) or isinstance(player, Shadow) or isinstance(player, BigSummon):
            player.Master.TotalPotency+= self.Potency
            player.Master.TotalDamage += Damage
            player.Master.TotalMinDamage += minDamage
        else:
            player.TotalPotency+= self.Potency
            player.TotalDamage += Damage
            player.TotalMinDamage += minDamage
        
        Enemy.TotalPotency+= self.Potency  #Adding Potency
        Enemy.TotalDamage += Damage #Adding Damage

        if self.id > 0 and Damage > 0: print("The action with id : " + str(self.id) + " did " + str(Damage) + " damage")


        #Will update the NextSpell of the player

        if (not (isinstance(self, DOTSpell))) : player.NextSpell+=1
        if (player.NextSpell == len(player.ActionSet)):#Checks if no more spell to do
            player.TrueLock = True

        return self

def ApplyMelee_AA(Player, Enemy):
    Player.DOTList.append(copy.deepcopy(Melee_AADOT))

def ApplyRanged_AA(Player, Enemy):
    Player.DOTList.append(copy.deepcopy(Ranged_AADOT))

def ApplyQueen_AA(Player, Enemy):
    Player.DOTList.append(copy.deepcopy(Queen_AADOT))

Melee_AA = Spell(-30, False, 0, 0, 0, 0, ApplyMelee_AA, [])
Ranged_AA = Spell(-30, False, 0, 0, 0, 0, ApplyRanged_AA, [])
Queen_AA = Spell(-30, False, 0, 0, 0, 0, ApplyQueen_AA, [])


#Function to generate Waiting

def ManaRequirement(player, Spell):
    ##print("Total mana : " + str(player.Mana))
    #input("Spell mana cost " + str(Spell.ManaCost))
    if player.Mana >= Spell.ManaCost :
        player.Mana -= Spell.ManaCost   #ManaRequirement is the only Requirement that actually removes Ressources
        return True, -1
    return True, -1

def empty(Player, Enemy):
    pass

def WaitAbility(time):
    return Spell(-1, False, time, time, 0, 0, empty, [])

def ApplyPotion(Player, Enemy):
    Player.Stat["MainStat"] = min(math.floor(Player.Stat["MainStat"] * 1.1), Player.Stat["MainStat"] + 189)
    Player.PotionTimer = 30

    Player.EffectCDList.append(PotionCheck)

def PotionCheck(Player, Enemy):
    if Player.PotionTimer <= 0:
        ##input("removing potion")
        Player.Stat["MainStat"] /= 1.1
        Player.EffectCDList.remove(PotionCheck)


class DOTSpell(Spell):
    #Represents DOT
    def __init__(self, id, Potency, isPhysical):
        super().__init__(id, False, 0, 0, Potency,  0, empty, [])
        #Note that here Potency is the potency of the dot, not of the ability
        self.DOTTimer = 0   #This represents the timer of the dot, and it will apply at each 3 seconds
        self.isPhysical = isPhysical #True if physical dot, false if magical dot

        #This part will keep in memory the buffs when the DOT is applied.
        self.CritBonus = 0
        self.DHBonus = 0
        self.MultBonus = []
        self.onceThroughFlag = False #This flag will be set to True once the DOT damage has been through damage computation once
        #so we can snapshot the buffs only once
        #Note that AAs do not snapshot buffs, but in the code they will still have these fields

    def CheckDOT(self, Player, Enemy, TimeUnit):
        ##print("The dot Timer is :  " + str(self.DOTTimer))
        if(self.DOTTimer <= 0):
            #Apply DOT
            tempSpell  = self.Cast(Player, Enemy)#Cast the DOT
            ##print(self.id)
            ##print("Timestamp is : " + str(Player.CurrentFight.TimeStamp))
            #input("applying dot with potency : " + str(tempSpell.Potency))
            tempSpell.CastFinal(Player, Enemy)
            self.DOTTimer = 3
        else:
            #input("updating : " + str(self.id))
            self.DOTTimer = max(0, self.DOTTimer-TimeUnit)


class Auto_Attack(DOTSpell):
    #DOT specifically used for auto attack
    def __init__(self, id, Ranged):
        if Ranged : super().__init__(id, 100, True)
        else: super().__init__(id, 110, True)

        self.DOTTimer = 23 #The timer is intentionally set at a longer time, so it won't go off before the countdown is over

class Queen_Auto(Auto_Attack):

    def __init__(self, id, Ranged):
        super().__init__(id, Ranged)
        self.Weaponskill = False
        self.DOTTimer = 0 #Since we need to attack as it spawns

class Melee_Auto(Auto_Attack):

    def __init__(self, id, Ranged):
        super().__init__(id, Ranged)
        self.Weaponskill = False

class Ranged_Auto(Auto_Attack):

    def __init__(self, id, Ranged):
        super().__init__(id, Ranged)
        self.Weaponskill = False


Melee_AADOT = Melee_Auto(-22, False)
Ranged_AADOT = Ranged_Auto(-23, True)
Queen_AADOT = Queen_Auto(-24, False)

Potion = Spell(-2, False, 1, 1, 0, 0, ApplyPotion, [])



