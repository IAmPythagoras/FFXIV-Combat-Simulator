import math
from Enemy import Enemy
import matplotlib.pyplot as plt
import numpy as np

from Jobs.Caster.Blackmage.BlackMage_Player import BlackMage
from Jobs.Caster.Redmage.Redmage_Player import Redmage

from Jobs.Tank.Paladin.Paladin_Player import Paladin
from Jobs.Tank.Gunbreaker.Gunbreaker_Player import Gunbreaker
from Jobs.Tank.Warrior.Warrior_Player import Warrior
from Jobs.Tank.DarkKnight.DarkKnight_Player import Esteem, DarkKnight

from Jobs.Ranged.Machinist.Machinist_Player import Queen, Machinist

from Jobs.Melee.Samurai.Samurai_Player import Samurai
from Jobs.Melee.Ninja.Ninja_Player import Ninja

from Jobs.Healer.Whitemage.Whitemage_Player import Whitemage
from Jobs.Healer.Scholar.Scholar_Player import Scholar

class NoMoreAction(Exception):#Exception called if a spell fails to cast
    pass

class Fight:

    #This class will be the environment in which the fight happens. It will hold a list of players, an enemy, etc.
    # It will be called upon for when we want to start the simulation

    def __init__(self, PlayerList, Enemy):
        self.PlayerList = PlayerList
        self.Enemy = Enemy
        self.ShowGraph = True
        self.TimeStamp = 0
    def PrintResult(self, time, TimeStamp):

        fig, axs = plt.subplots(1, 2, constrained_layout=True)
        axs[0].set_ylabel("DPS")
        axs[0].set_xlabel("Time (s)")
        axs[0].set_title("DPS over time")
        axs[0].spines["top"].set_alpha(0.0)
        axs[0].spines["right"].set_alpha(0.0)
        axs[0].set_facecolor("lightgrey")
        axs[1].set_ylabel("PPS")
        axs[1].set_xlabel("Time (s)")
        axs[1].set_title("PPS over time")
        axs[1].spines["top"].set_alpha(0.0)
        axs[1].spines["right"].set_alpha(0.0)
        axs[1].set_facecolor("lightgrey")

        fig.suptitle("DPS and PPS values over time.")

        for player in self.PlayerList:
            print("The Total Potency done by player " + str(type(player)) + " was : " + str(player.TotalPotency))
            print("This same player had a Potency Per Second of: " + str(player.TotalPotency/time))
            print("This same Player had an average of " + str(player.TotalPotency/player.NextSpell) + " Potency/Spell")
            print("This same Player had an average of " + str(player.TotalPotency/(time/player.GCDTimer)) + " Potency/GCD")
            print("The DPS is : " + str(player.TotalDamage / time))
            print("=======================================================")

            #Plot part

            job = ""

            if isinstance(player, BlackMage) : job = "Blackmage"
            elif isinstance(player, Redmage) : job = "Redmage"
            elif isinstance(player, DarkKnight) : job = "DarkKnight"
            elif isinstance(player, Warrior) : job = "Warrior"
            elif isinstance(player, Paladin) : job = "Paladin"
            elif isinstance(player, Gunbreaker) : job = "Gunbreaker"
            elif isinstance(player, Machinist) : job = "Machinist"
            elif isinstance(player, Samurai) : job = "Samurai"
            elif isinstance(player, Ninja) : job = "Ninja"
            elif isinstance(player, Scholar) : job = "Scholar"
            elif isinstance(player, Whitemage) : job = "Whitemage"

            axs[0].plot(TimeStamp,player.DPSGraph, label=job)
            axs[1].plot(TimeStamp,player.PotencyGraph, label=job)
        
        print("The Enemy has received a total potency of: " + str(self.Enemy.TotalPotency))
        print("The Potency Per Second on the Enemy is: " + str(self.Enemy.TotalPotency/time))
        print("The Enemy's total DPS is " + str(self.Enemy.TotalDamage / time))
        axs[0].xaxis.grid(True)
        axs[1].xaxis.grid(True)
        axs[0].xaxis.set_ticks(np.arange(2.5, max(TimeStamp)+1, 2.5))
        axs[1].xaxis.set_ticks(np.arange(2.5, max(TimeStamp)+1, 2.5))
        axs[0].legend()
        axs[1].legend()
        if self.ShowGraph: plt.show()



    def SimulateFight(self, TimeUnit, TimeLimit, FightCD):
            #This function will Simulate the fight given the enemy and player list of this Fight
            #It will increment in TimeUnit up to a maximum of TimeLimit (there can be other reasons the Fight ends)
            #It will check weither a player can cast its NextSpell, and if it can it will call the relevant functions
            #However, no direct computation is done in this function, it simply orchestrates the whole thing
            self.TimeStamp = 0   #Keep track of the time
            start = False

            timeValue = []  #Used for graph

            while(self.TimeStamp <= TimeLimit):

                for player in self.PlayerList:
                    #print("MainStat : " + str(player.Stat["MainStat"]))
                    #Will first Check if the NextSpell is a GCD or not
                    if(not player.TrueLock):#If it is we do nothing
                        if(player.ActionSet[player.NextSpell].GCD):
                            #Is a GCD

                            #Have to check if the player can cast the spell
                            #So check if Animation Lock, if Casting or if GCDLock
                            if(not (player.oGCDLock or player.GCDLock or player.Casting)):
                                #If we in here, then we can cast the next spell
                                #print(player)
                                #input("is casting gcd at : " + str(self.TimeStamp))

                                player.CastingSpell = player.ActionSet[player.NextSpell].Cast(player, self.Enemy)#Cast the spell
                                #print("Spell with ID " + str(player.CastingSpell.id) + " has begun casting at " +  str(self.self.TimeStamp) )
                                #Locking the player

                                player.Casting = True
                                player.CastingLockTimer = player.CastingSpell.CastTime
                                player.GCDLock = True
                                player.GCDLockTimer = player.CastingSpell.RecastTime
                                player.CastingTarget = self.Enemy
                            #Else we do nothing since doing the nextspell is not currently possible


                        else:
                            #Is an oGCD
                            
                            if(not (player.oGCDLock or player.Casting)):
                                #Then we can cast the oGCD
                                player.CastingSpell = player.ActionSet[player.NextSpell].Cast(player, self.Enemy)
                                player.CastingSpell.CastFinal(player, self.Enemy)
                                player.oGCDLock = True
                                player.oGCDLockTimer = player.CastingSpell.CastTime
                                #print("oGCD with ID " + str(player.CastingSpell.id) + " has begun casting at " +  str(self.TimeStamp) )


                    


                #Will then let the enemy add the Dots damage

                for player in self.PlayerList:
                    #print(player)
                    #print("============")
                    for DOT in player.DOTList:
                        DOT.CheckDOT(player,self.Enemy, TimeUnit)
                for player in self.PlayerList:
                    #print(player.EffectCDList)
                    for CDCheck in player.EffectCDList:
                        CDCheck(player, self.Enemy)
                    for remove in player.EffectToRemove:
                        player.EffectCDList.remove(remove) #Removing relevant spell

                    player.EffectToRemove = []
                


                #We will now update any timer each player and the enemy has

                for player in self.PlayerList:
                    player.updateTimer(TimeUnit)
                    player.updateCD(TimeUnit)
                    player.updateLock() #Update the lock on the player to see if it's state changes


                CheckFinalLock = True
                for player in self.PlayerList:
                    CheckFinalLock = player.TrueLock and CheckFinalLock #If all player's TrueLock is true, then CheckFinalLock will be True

                if CheckFinalLock: 
                    print("The Fight finishes at: " + str(self.TimeStamp))
                    break

                
                if start:
                    #If the fight has started, will sample DPS values at certain time
                    if (self.TimeStamp%1 == 0.3 or self.TimeStamp%1 == 0.0 or self.TimeStamp%1 == 0.6 or self.TimeStamp%1 == 0.9) and self.TimeStamp >= 3:#last thing is to ensure no division by zero and also to have no spike at the begining
                        #Only sample each 1/2 second
                        timeValue+= [self.TimeStamp]
                        for Player in self.PlayerList:
                            Player.DPSGraph += [round(Player.TotalDamage/self.TimeStamp, 2)] #Rounding the value to 2 digits
                            Player.PotencyGraph += [round(Player.TotalPotency/self.TimeStamp, 2)]

                #update self.TimeStamp
                self.TimeStamp += TimeUnit
                self.TimeStamp = round(self.TimeStamp, 2)

                FightCD -= TimeUnit
                if FightCD <= 0 and not start:
                    self.TimeStamp = 0
                    start = True
                    #print("==========================================================================================")
                    #print("FIGHT START")
                    #print("==========================================================================================")

            

            #Post fight computations

            #print("LIST========================================================")

            remove = []

            for i in range(len(self.PlayerList)):  
                player = self.PlayerList[i]
                if isinstance(player, DarkKnight):
                    player.TotalPotency += player.EsteemPointer.TotalPotency    #Adds every damage done by Esteem to the dark knight
                if isinstance(player, Queen):
                    remove += [i]
                if isinstance(player, Esteem):
                    remove += [i]

            k = 0
            for i in remove:
                self.PlayerList.pop(i-k)
                k+=1
                

            self.PrintResult(self.TimeStamp, timeValue)
            





def ComputeDamage(Player, DPS, EnemyBonus, SpellBonus):
    #This function will compute the DPS given the stats of a player

    levelMod = 1900
    baseMain = 390  
    baseSub = 400
    JobMod = 115

    MainStat = Player.Stat["MainStat"] * 1.05 #Assuming we have 5% bonus on stats due to team (could add code to compute it)

    Damage=math.floor(DPS*(Player.Stat["WD"]+math.floor(baseMain*JobMod/1000))*(100+math.floor((MainStat-baseMain)*195/baseMain))/100)

    Damage=math.floor(Damage*(1000+math.floor(140*(Player.Stat["Det"]-baseMain)/levelMod))/1000)#Determination damage

    Damage=math.floor(Damage*(1000+math.floor(100*(Player.Stat["Ten"]-baseSub)/levelMod))/1000)#Tenacity damage

    Damage=math.floor(Damage*(1000+math.floor(130*(Player.Stat["SS"]-baseSub)/levelMod))/1000/100)#Spell/Skill speed damage bonus

    Damage = math.floor(Player.MultDPSBonus * Damage * EnemyBonus * SpellBonus)

    CritRate = math.floor((200*(Player.Stat["Crit"]-baseSub)/levelMod+50))/1000

    CritDamage = (math.floor(200*(Player.Stat["Crit"]-baseSub)/levelMod+400))/1000

    DHRate = math.floor(550*(Player.Stat["DH"]-baseSub)/levelMod)/1000

    if Player.CurrentFight.Enemy.ChainStratagem: CritRate += 0.1    #If ChainStratagem is active, increase crit

    if isinstance(Player, Machinist): 
        #print(Player.ActionSet[Player.NextSpell])  #Then if machinist, has to check if direct crit guarantee
        if Player.ActionSet[Player.NextSpell].id != -1 and Player.ActionSet[Player.NextSpell].id != -2 and Player.Reassemble and Player.ActionSet[Player.NextSpell].WeaponSkill:    #Checks if reassemble is on and if its a weapon skill
            CritRate = 1
            DHRate = 1
            Player.Reassemble = False #Uses Reassemble       
    elif isinstance(Player, Warrior):
        if Player.InnerReleaseStack >= 1 and (Player.ActionSet[Player.NextSpell].id == 9 or Player.ActionSet[Player.NextSpell].id == 8):
            CritRate = 1#If inner release weaponskill
            DHRate = 1
            Player.InnerReleaseStack -= 1
    elif isinstance(Player, Samurai):
        if Player.DirectCrit:
            CritRate = 1
            DHRate = 1
            Player.DirectCrit = False

    return Damage * ((1+(DHRate/4))*(1+(CritRate*CritDamage)))
"""
    // Pulled from Orinx's Gear Comparison Sheet with slight modifications
function Damage(Potency, WD, JobMod, MainStat,Det, Crit, DH,SS,TEN, hasBrd, hasDrg, hasSch, hasDnc, classNum) {
  
  MainStat=Math.floor(MainStat*(1+0.01*classNum));
  var Damage=Math.floor(Potency*(WD+Math.floor(baseMain*JobMod/1000))*(100+Math.floor((MainStat-baseMain)*195/baseMain))/100);
  Damage=Math.floor(Damage*(1000+Math.floor(140*(Det-baseMain)/levelMod))/1000);
  Damage=Math.floor(Damage*(1000+Math.floor(100*(TEN-baseSub)/levelMod))/1000);
  Damage=Math.floor(Damage*(1000+Math.floor(130*(SS-baseSub)/levelMod))/1000/100);
  Damage=Math.floor(Damage*magicAndMend)
  Damage=Math.floor(Damage*enochian)
  var CritDamage=CalcCritDamage(Crit)
  var CritRate=CalcCritRate(Crit) + (hasDrg ? battleLitanyAvg : 0) + (hasSch ? chainStratAvg : 0) + (hasDnc ? devilmentAvg : 0) + (hasBrd ? brdCritAvg : 0);
  var DHRate=CalcDHRate(DH) + (hasBrd ? battleVoiceAvg + brdDhAvg : 0) + (hasDnc ? devilmentAvg : 0);
  return Damage * ((1+(DHRate/4))*(1+(CritRate*CritDamage)))                                                                                                                               
}

"""