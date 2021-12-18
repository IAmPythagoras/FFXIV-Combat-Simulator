import math


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
            print("=======================================================")
        
        print("The Enemy has received a total potency of: " + str(self.Enemy.TotalPotency))
        print("The Potency Per Second on the Enemy is: " + str(self.Enemy.TotalPotency/time))



    def SimulateFight(self, TimeUnit, TimeLimit, FightCD):
            #This function will Simulate the fight given the enemy and player list of this Fight
            #It will increment in TimeUnit up to a maximum of TimeLimit (there can be other reasons the Fight ends)
            #It will check weither a player can cast its NextSpell, and if it can it will call the relevant functions
            #However, no direct computation is done in this function, it simply orchestrates the whole thing
            TimeStamp = 0   #Keep track of the time
            start = False
            while(TimeStamp <= TimeLimit):

                for player in self.PlayerList:
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
                    CheckFinalLock = player.TrueLock and CheckFinalLock

                if CheckFinalLock: 
                    print("The Fight finishes at: " + str(TimeStamp))
                    break


                #update timestamp
                #if(math.floor(TimeStamp*1000)%100 == 0) : print(str(TimeStamp))
                TimeStamp += TimeUnit


                FightCD -= TimeUnit
                if FightCD <= 0 and not start:
                    TimeStamp = 0
                    start = True
                    #print("==========================================================================================")
                    #print("FIGHT START")
                    #print("==========================================================================================")

            self.PrintResult(TimeStamp)
            







