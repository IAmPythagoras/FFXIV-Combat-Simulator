import math
from Enemy import Enemy
import matplotlib.pyplot as plt
from Player import DarkKnight, Machinist, Queen


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

            

            axs[0].plot(TimeStamp,player.DPSGraph, label=str(type(player)))
            axs[1].plot(TimeStamp,player.PotencyGraph, label=str(type(player)))
        
        print("The Enemy has received a total potency of: " + str(self.Enemy.TotalPotency))
        print("The Potency Per Second on the Enemy is: " + str(self.Enemy.TotalPotency/time))
        print("The Enemy's total DPS is " + str(self.Enemy.TotalDamage / time))
        axs[0].legend()
        axs[1].legend()
        axs[0].grid()
        axs[1].grid()
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
                    #print(player.DOTList)
                    #print(player)
                    #print("============")
                    for DOT in player.DOTList:
                        DOT.CheckDOT(player,self.Enemy, TimeUnit)
                for player in self.PlayerList:
                    #print(player.EffectCDList)
                    for CDCheck in player.EffectCDList:
                        CDCheck(player, self.Enemy)

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


            for Player in self.PlayerList:
                if isinstance(Player, DarkKnight):
                    Player.TotalPotency += Player.EsteemPointer.TotalPotency    #Adds every damage done by Esteem to the dark knight
                    self.PlayerList.remove(Player.EsteemPointer)
                elif isinstance(Player, Queen):
                    self.PlayerList.remove(Player)

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