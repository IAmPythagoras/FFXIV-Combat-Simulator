import math
from Enemy import Enemy

from Player import DarkKnight


class NoMoreAction(Exception):#Exception called if a spell fails to cast
    pass

class Fight:

    #This class will be the environment in which the fight happens. It will hold a list of players, an enemy, etc.
    # It will be called upon for when we want to start the simulation

    def __init__(self, PlayerList, Enemy):
        self.PlayerList = PlayerList
        self.Enemy = Enemy

    def PrintResult(self, time):

        for player in self.PlayerList:
            print("The Total Potency done by player " + str(type(player)) + " was : " + str(player.TotalPotency))
            print("This same player had a Potency Per Second of: " + str(player.TotalPotency/time))
            print("This same Player had an average of " + str(player.TotalPotency/player.NextSpell) + " Potency/Spell")
            print("This same Player had an average of " + str(player.TotalPotency/(time/player.GCDTimer)) + " Potency/GCD")
            print("The DPS is : " + str(player.TotalDamage / time))
            print("=======================================================")
        
        print("The Enemy has received a total potency of: " + str(self.Enemy.TotalPotency))
        print("The Potency Per Second on the Enemy is: " + str(self.Enemy.TotalPotency/time))
        print("The Enemy's total DPS is " + str(self.Enemy.TotalDamage / time))



    def SimulateFight(self, TimeUnit, TimeLimit, FightCD):
            #This function will Simulate the fight given the enemy and player list of this Fight
            #It will increment in TimeUnit up to a maximum of TimeLimit (there can be other reasons the Fight ends)
            #It will check weither a player can cast its NextSpell, and if it can it will call the relevant functions
            #However, no direct computation is done in this function, it simply orchestrates the whole thing
            TimeStamp = 0   #Keep track of the time
            start = False
            while(TimeStamp <= TimeLimit):

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
                                #print("Spell with ID " + str(player.CastingSpell.id) + " has begun casting at " +  str(TimeStamp) )
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
                                #print("oGCD with ID " + str(player.CastingSpell.id) + " has begun casting at " +  str(TimeStamp) )


                    


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
                    print("The Fight finishes at: " + str(TimeStamp))
                    break


                #update timestamp
                TimeStamp += TimeUnit


                FightCD -= TimeUnit
                if FightCD <= 0 and not start:
                    TimeStamp = 0
                    start = True
                    #print("==========================================================================================")
                    #print("FIGHT START")
                    #print("==========================================================================================")

            

            #Post fight computations


            for Player in self.PlayerList:
                if isinstance(Player, DarkKnight):
                    Player.TotalPotency += Player.EsteemPointer.TotalPotency    #Adds every damage done by Esteem to the dark knight
                    self.PlayerList.remove(Player.EsteemPointer)

            self.PrintResult(TimeStamp)
            





def ComputeDamage(Player, DPS, EnemyBonus):
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

    #This is only for Black mage 

    Damage = math.floor(Player.MultDPSBonus * Damage * EnemyBonus)

    CritRate = math.floor((200*(Player.Stat["Crit"]-baseSub)/levelMod+50))/1000
    CritDamage = (math.floor(200*(Player.Stat["Crit"]-baseSub)/levelMod+400))/1000

    DHRate = math.floor(550*(Player.Stat["DH"]-baseSub)/levelMod)/1000

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