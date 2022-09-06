import math
import matplotlib.pyplot as plt
import numpy as np


#Class
from Jobs.Caster.Caster_Player import Caster
from Jobs.Melee.Melee_Player import Melee
from Jobs.Ranged.Ranged_Player import Ranged
from Jobs.Tank.Tank_Player import Tank
from Jobs.Healer.Healer_Player import Healer

#Jobs
from Jobs.Caster.Blackmage.BlackMage_Player import BlackMage
from Jobs.Caster.Redmage.Redmage_Player import Redmage
from Jobs.Caster.Summoner.Summoner_Player import BigSummon, Summoner
from Jobs.Ranged.Bard.Bard_Player import Bard
from Jobs.Ranged.Dancer.Dancer_Player import Dancer

from Jobs.Tank.Paladin.Paladin_Player import Paladin
from Jobs.Tank.Gunbreaker.Gunbreaker_Player import Gunbreaker
from Jobs.Tank.Warrior.Warrior_Player import Warrior
from Jobs.Tank.DarkKnight.DarkKnight_Player import Esteem, DarkKnight

from Jobs.Ranged.Machinist.Machinist_Player import Queen, Machinist

from Jobs.Melee.Samurai.Samurai_Player import Samurai
from Jobs.Melee.Ninja.Ninja_Player import Ninja, Shadow
from Jobs.Melee.Dragoon.Dragoon_Player import Dragoon
from Jobs.Melee.Reaper.Reaper_Player import Reaper

from Jobs.Healer.Whitemage.Whitemage_Player import Whitemage
from Jobs.Healer.Scholar.Scholar_Player import Scholar
from Jobs.Healer.Astrologian.Astrologian_Player import Astrologian

class NoMoreAction(Exception):#Exception called if a spell fails to cast
    pass


#GCDReduction Effect

def GCDReductionEffect(Player, Spell):
    if Spell.GCD:
        Spell.CastTime *= Player.GCDReduction
        Spell.RecastTime *= Player.GCDReduction

def Normal(mean, std, x):#returns value from NormalDistribution
    if std == 0 : return 0
    return 1/(std * np.sqrt(2 * np.pi)) * np.exp(-1/2 * ((x-mean)/std)**2)


def AverageCritMult(Player, k):
    n = Player.NumberDamageSpell #Total number of damage Spell
    if n == 0 : return 0
    #k is the number of success, so the number of crit
    return ((k) * (1 + Player.CritMult)  + (n-k))/n #Average crit multiplier over the run, this can be seen as a fix bonus on the whole fight

class Fight:

    #This class will be the environment in which the fight happens. It will hold a list of players, an enemy, etc.
    # It will be called upon for when we want to start the simulation

    def __init__(self, PlayerList, Enemy, ShowGraph):
        self.PlayerList = PlayerList
        self.Enemy = Enemy
        self.ShowGraph = ShowGraph
        self.TimeStamp = 0
        self.TeamCompositionBonus = 1



    def ComputeDPSDistribution(self, Player, fig, axs, job):

        #Graph data
        axs.set_ylabel("Percentage (%)")
        axs.set_xlabel("Expected DPS")
        axs.set_title(job + " DPS Distribution")
        axs.spines["top"].set_alpha(0.0)
        axs.spines["right"].set_alpha(0.0)
        axs.set_facecolor("lightgrey")
        #axs.yaxis.set_ticks(np.arange(0,15,1))




        #This function will return a distribution of DPS and chance of having certain DPS
        Player.DPS = Player.TotalMinDamage / self.TimeStamp #Computing DPS with no crit, expected DH
        Player.ExpectedDPS = Player.TotalDamage / self.TimeStamp #Expected DPS with crit

        n = Player.NumberDamageSpell #Number of spell that deals damage done by this player
        p = round((Player.ExpectedDPS/Player.DPS - 1)/Player.CritMult,3)

        #The value of p is found by using the fact that Player.DPS = DPS * ExpectedDHDamage, Player.ExpectedDPS = DPS * ExpectedDHDamage * ExpectedCritDamage
        #And ExpectedCritDamage = ( 1 + (CritMult * CritRate)), so we simply isolate CritRate. This will give an average Crit rate over the whole fight which will
        #take into account crit rate buffs throughout the fight
        decimal_mean = n*p #Number of expected crit (not an integer)
        mean = math.floor(decimal_mean) #Number of expected crit rounded down
        radius = math.ceil(n/2) #Radius we for which we will graph the distribution
        std = n*p * (1-p) #Standard deviation
        #The binomial distribution of enough trials can be approximated to N(np, np(1-p)) for big enough n, so we will simply approximate the distribution by this
        #Note that here n stands for the number of damage spell, and p is the averagecritrate of the player AverageCritRate = (CritRate + CritRateBonus)/time
        #We will salvage values from the normal distribution, then find the average crit multiplier by number of crits gotten. We will then multiply the computed DPS
        #by these multipliers to get DPS values for each chance
        #We will sample n/2 points on each side

        y_list = []
        expected_dps_list = [] #List of expected DPS
        resolution = 500 #Hardcoded value, represents how many points on the curve we take
        i = max(0, mean-radius) #Starting point
        j = mean + radius+1 #Upper limit
        h = (j - i)/resolution #Step to take
        x_list = np.linspace(i,j,resolution) #Evenly spaced out from i -> j with resolution number of points
        #It will be computed by computing an average crit multiplier, and then multiplying the DPS by that
        while i < j:
            next_point = Normal(decimal_mean, std, i) * 100000 / 10
            #input(next_point)
            y_list += [math.floor(next_point)/100]
            average_crit_mult = AverageCritMult(Player, i)
            expected_dps_list += [average_crit_mult * Player.DPS]
            i+= h




        #for i in range(max(0, mean - radius), mean + radius+1): #Here i is the number of success
         #   y_list += [math.floor(Normal(decimal_mean, std, i) * 1000) /10] #Sampling from the distribution
          #  average_crit_mult = AverageCritMult(Player, i)
           # expected_dps_list += [average_crit_mult * Player.DPS]


        high_crit_mult_list = []
        low_crit_mult_list = []
        for i in range(1,4): #This loop will create boundary for the empirical rules, it will do 1 to 3 std away from the mean
            high = decimal_mean + i*std
            low = decimal_mean - i*std
            high_crit_mult = AverageCritMult(Player, high)
            low_crit_mult = AverageCritMult(Player, low)
            high_crit_mult_list += [high_crit_mult * Player.DPS]
            low_crit_mult_list += [low_crit_mult * Player.DPS]
        #Even though low and high are not integers, the AverageCritMult is a continuous stricly increasing function, so we can use it on
        #non integer value to get an "in-between" value

        top_graph = max(y_list) * 1.3 #top of graph
        lab = "\u03BC = " + str(round(Player.ExpectedDPS,1)) + " \u03C3 = " + str(round(std,2))
        axs.plot(expected_dps_list, y_list,label=lab) #Distribution
        axs.plot([Player.ExpectedDPS,Player.ExpectedDPS], [0,top_graph], label="Expected DPS", linestyle="dashed") #Expected DPS
        #Plotting Empirical rule region
        axs.axvspan(max(expected_dps_list[0],low_crit_mult_list[2]), min(expected_dps_list[-1],high_crit_mult_list[2]), color="green") #99.7% empirical rule region, will most likely not appear in the graph
        axs.axvspan(max(expected_dps_list[0],low_crit_mult_list[1]), high_crit_mult_list[1], color="blue") #95% empirical rule region
        axs.axvspan(low_crit_mult_list[0], high_crit_mult_list[0], color="red") #68% empirical rule region


        axs.fill_between(expected_dps_list, y_list,top_graph, fc="lightgrey") #Used to cover the vertical regions from axvspan so they stop under the line of the distribution
        axs.margins(-0.0001) #margin arrangement
        axs.legend()


        





        #We now have values from the sample, so we will now change x_list into DPS value







    def PrintResult(self, time, TimeStamp):

        fig, axs = plt.subplots(1, 2, constrained_layout=True) #DPS and PPS graph
        fig2, axs2 = plt.subplots(2, 4, constrained_layout=True) #DPS Crit distribution
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

        i = 0 #Used as coordinate for DPS distribution graph
        j = 0

        for player in self.PlayerList:

            if player.TotalPotency == 0:
                PPS = 0
                DPS = 0
            else:
                PPS = player.TotalPotency / time
                DPS = player.TotalDamage / time

            print("The Total Potency done by player " + str(type(player)) + " was : " + str(player.TotalPotency))
            print("This same player had a Potency Per Second of: " + str(PPS))
            print("This same Player had an average of " + str(player.TotalPotency/player.NextSpell) + " Potency/Spell")
            print("This same Player had an average of " + str(PPS/player.GCDTimer) + " Potency/GCD")
            print("The DPS is : " + str(DPS))
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
            elif isinstance(player, Astrologian) : job = "Astrologian"
            elif isinstance(player, Summoner) : job = "Summoner"
            elif isinstance(player, Dragoon) : job = "Dragoon"
            elif isinstance(player, Reaper) : job = "Reaper"
            elif isinstance(player, Bard) : 
                job = "Bard"
                print("==================")
                print("Expected Vs Used values for bard")
                print("Expected Refulgent Proc : " + str(player.ExpectedRefulgent) + " Used Refulgent Proc : " + str(player.UsedRefulgent))
                print("Expected Wanderer Repertoire Proc : " + str(player.ExpectedTotalWandererRepertoire) + " Used Repertoire Proc : " + str(player.UsedTotalWandererRepertoire))
                print("RepertoireAdd : " + str(player.UsedRepertoireAdd))
                print("Expected Soul Voice Gauge : " + str(player.ExpectedSoulVoiceGauge) + " Used SoulVoiceGauge : " + str(player.UsedSoulVoiceGauge))
                print("Expected BloodLetterReduction : " + str(player.ExpectedBloodLetterReduction) + " Used BloodLetterReduction : " + str(player.UsedBloodLetterReduction))
                print("==================")
            elif isinstance(player, Dancer):
                job = "Dancer"
                print("==================")
                print("Expected Vs Used Proc for Dancer")
                print("Expected SilkenSymettry : " + str(player.ExpectedSilkenSymettry) + " Used SilkenSymettry : " + str(player.UsedSilkenSymettry) )
                print("Expected SilkenFlow : " + str(player.ExpectedSilkenFlow) + " Used SilkenFlow : " + str(player.UsedSilkenFlow) )
                print("Expected FourfoldFeather : " + str(player.ExpectedFourfoldFeather) + " Used FourfoldFeather : " + str(player.UsedFourfoldFeather) )
                print("Expected ThreefoldFan : " + str(player.ExpectedThreefoldFan) + " Used ThreefoldFan : " + str(player.UsedThreefoldFan) )
                print("==================")
            axs[0].plot(TimeStamp,player.DPSGraph, label=job)
            axs[1].plot(TimeStamp,player.PotencyGraph, label=job)

            if DPS != 0 : self.ComputeDPSDistribution(player, fig2, axs2[j][i], job)
            i+=1
            if i == 4:
                i = 0
                j+=1
        
        print("The Enemy has received a total potency of: " + str(self.Enemy.TotalPotency))
        print("The Potency Per Second on the Enemy is: " + str(self.Enemy.TotalPotency/time))
        print("The Enemy's total DPS is " + str(self.Enemy.TotalDamage / time))
        axs[0].xaxis.grid(True)
        axs[1].xaxis.grid(True)
        axs[0].xaxis.set_ticks(np.arange(0, max(TimeStamp)+1, 25))
        axs[1].xaxis.set_ticks(np.arange(0, max(TimeStamp)+1, 25))
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

            self.ComputeFunctions() #Compute all damage functions for the players


            #The first thing we will do is compute the TEAM composition DPS bonus
            #each class will give 1%
            # Tank, Healer, Caster, Ranged, Melee
            hasMelee = False
            hasCaster = False
            hasRanged = False
            hasTank = False
            hasHealer = False
            for player in self.PlayerList:
                if isinstance(player, Melee) : hasMelee = True
                elif isinstance(player, Caster) : hasCaster = True
                elif isinstance(player, Ranged) : hasRanged = True
                elif isinstance(player, Tank) : hasTank = True
                elif isinstance(player, Healer) : hasHealer = True

            if len(self.PlayerList) == 1 : self.TeamCompositionBonus = 1 #If only one player, there is not bonus
            else:
                if hasMelee: self.TeamCompositionBonus += 0.01
                if hasCaster: self.TeamCompositionBonus += 0.01
                if hasRanged: self.TeamCompositionBonus += 0.01
                if hasTank: self.TeamCompositionBonus += 0.01
                if hasHealer: self.TeamCompositionBonus += 0.01

            #Will first compute each player's GCD reduction value based on their Spell Speed or Skill Speed Value

            for Player in self.PlayerList:
                Player.GCDReduction = (1000 - (130 * (Player.Stat["SS"]-400) / 1900))/1000
                Player.EffectList.append(GCDReductionEffect)

            while(self.TimeStamp <= TimeLimit):

                for player in self.PlayerList:
                   # if player.ActionSet[player.NextSpell] == None : player.TrueLock = True #Locking the player if None
                    #Will first Check if the NextSpell is a GCD or not
                    if(not player.TrueLock):#If it is we do nothing
                        if (player.ActionSet[player.NextSpell].GCD):
                            #Is a GCD
                            #Have to check if the player can cast the spell
                            #So check if Animation Lock, if Casting or if GCDLock
                            if(not (player.oGCDLock or player.GCDLock or player.Casting)):
                                #if isinstance(player, Bard): input("Bard casts : " + str(player.ActionSet[player.NextSpell].id))

                                player.CastingSpell = player.ActionSet[player.NextSpell].Cast(player, self.Enemy)#Cast the spell
                                #Locking the player
                                #print(Player.CastingSpell.CastTime)
                                ##input(Player.CastingSpell.RecastTime)
                                player.Casting = True
                                player.CastingLockTimer = player.CastingSpell.CastTime
                                player.GCDLock = True
                                player.GCDLockTimer = player.CastingSpell.RecastTime
                                player.CastingTarget = self.Enemy
                            #Else we do nothing since doing the nextspell is not currently possible


                        else:
                            #Is an oGCD
                            #print("Spell with id : " + str(player.ActionSet[player.NextSpell].id))
                            ##input("is being casted at : " + str(self.TimeStamp))
                            
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
                        #print(DOT)
                        DOT.CheckDOT(player,self.Enemy, TimeUnit)
                for player in self.PlayerList:
                    #print(player.EffectCDList)
                    for CDCheck in player.EffectCDList:
                        CDCheck(player, self.Enemy)
                    for remove in player.EffectToRemove:
                        player.EffectCDList.remove(remove) #Removing relevant spell
                    for add in player.EffectToAdd:
                        player.EffectCDList.append(add)
                    player.EffectToRemove = []
                    player.EffectToAdd = []
                


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
                player = self.PlayerList[i] #Removing all instance of clones/summons from the fight
                if isinstance(player, Queen):
                    remove += [i]
                if isinstance(player, Esteem):
                    remove += [i]
                if isinstance(player, Shadow):
                    remove += [i]
                if isinstance(player, BigSummon):
                    remove += [i]

            k = 0
            for i in remove:
                self.PlayerList.pop(i-k)
                k+=1
                

            self.PrintResult(self.TimeStamp, timeValue)
            


    def ComputeFunctions(self):
        for Player in self.PlayerList:
            levelMod = 1900
            baseMain = 390  
            baseSub = 400#Level 90 LevelMod values

            JobMod = Player.JobMod #Level 90 jobmod value, specific to each job

            Player.f_WD = (Player.Stat["WD"]+math.floor(baseMain*JobMod/1000))/100
            Player.f_DET = math.floor(1000+math.floor(140*(Player.Stat["Det"]-baseMain)/levelMod))/1000#Determination damage
            if isinstance(Player, Tank) : Player.f_TEN = (1000+math.floor(100*(Player.Stat["Ten"]-baseSub)/levelMod))/1000 #Tenacity damage, 1 for non-tank player
            else : Player.f_TEN = 1 #if non-tank
            Player.f_SPD = (1000+math.floor(130*(Player.Stat["SS"]-baseSub)/levelMod))/1000 #Used only for dots
            Player.CritRate = math.floor((200*(Player.Stat["Crit"]-baseSub)/levelMod+50))/1000 #Crit rate in decimal
            Player.CritMult = (math.floor(200*(Player.Stat["Crit"]-baseSub)/levelMod+400))/1000 #Crit Damage multiplier
            Player.DHRate = math.floor(550*(Player.Stat["DH"]-baseSub)/levelMod)/1000 #DH rate in decimal

            #print("f_WD : " + str(Player.f_WD))
            #print("f_DET : " + str(Player.f_DET))
            #print("f_SPD : " + str(Player.f_SPD))
            #print("CritRate : " + str(Player.CritRate))
            #print("CritMult : " + str(Player.CritMult))
            #print("DHRate : " + str(Player.DHRate))
            #input("")


def ComputeDamage(Player, Potency, Enemy, SpellBonus, type, spellObj):

    #Still remains to change the f_MAIN_DAMAGE function for pets

    #The type input signifies what type of damage we are dealing with, since the computation will chance according to what
    #type of damage it is

    #type = 0 (Direct Damage), type = 1 (magical DOT), type = 2(physical DOT), type = 3 (Auto-attacks)

    #All relevant formulas were taken from https://finalfantasy.fandom.com/wiki/Final_Fantasy_XIV_attributes#Damage_and_healing_formulae ,
    #were given to me by javaJake#0001 on discord or were taken from the Allagan Studies discord server.
    #The formulas on the website assume a random function that will randomise the ouput. We instead compute the expected outcome.
    #Also thanks to whoever did the DPS computation code on the black mage gear comparison sheet : https://docs.google.com/spreadsheets/d/1t3EYSOPuMceqCFrU4WAbzSd4gbYi-J7YeMB36dNmaWM/edit#gid=654212594
    #It helped me a lot to understand better the DPS computation of this game
    #Also, note that this function is still in development, and so some of these formulas might be a bit off. Use at your own risk.
    #This function will compute the DPS given the stats of a player

    #THESE COMPUTATIONS ARE NOT COMPLETELY UP TO DATE FOR ENDWALKER AND SOME PARTS OF IT STILL WON'T COMPLETELY WORK.

    baseMain = 390  

    Enemy = Player.CurrentFight.Enemy #Enemy targetted


    if isinstance(Player, Queen) or isinstance(Player, Esteem) or isinstance(Player, Shadow) or isinstance(Player, BigSummon): MainStat = Player.Stat["MainStat"] #Summons do not receive bonus
    else: MainStat = math.floor(Player.Stat["MainStat"] * Player.CurrentFight.TeamCompositionBonus) #Scaling %bonus on mainstat
    #Computing values used throughout all computations
    if isinstance(Player, Tank) : f_MAIN_DMG = (100+math.floor((MainStat-baseMain)*156/baseMain))/100 #Tanks have a difference constant 
    else: f_MAIN_DMG = (100+math.floor((MainStat-baseMain)*195/baseMain))/100
    #These values are all already computed since they do not change
    f_WD = Player.f_WD
    f_DET = Player.f_DET
    f_TEN = Player.f_TEN
    f_SPD = Player.f_SPD
    CritRate = (Player.CritRate)
    CritMult = Player.CritMult
    DHRate = Player.DHRate

    if Enemy.ChainStratagem: CritRate += 0.1    #If ChainStratagem is active, increase crit rate

    if Enemy.WanderingMinuet: CritRate += 0.02 #If WanderingMinuet is active, increase crit rate

    if Enemy.BattleVoice: DHRate += 0.2 #If BattleVoice is active, increase DHRate


    DHRate += Player.DHRateBonus #Adding Bonus
    CritRate += Player.CritRateBonus #Adding bonus
    #if CritRate - save  > 0.22 : input("HEY " + str(CritRate) + " : " + str(Player))
    """
    print("Current Buffs are " + str(Player.DHRateBonus) + " : " + str(Player.CritRateBonus))
    totalbuff = 1
    for buffs in Player.buffList: 
        totalbuff *= buffs.MultDPS
    for buffs in Enemy.buffList:
        totalbuff *= buffs.MultDPS
    print("DPS BUFF : " + str(totalbuff))
    """


    #We will check if the ability is an assured crit and/ord DH, in which case we will have to buff the damage
    #Depending on the buffs the player is currently receiving

    auto_crit = False
    auto_DH = False
    CritRateBonus = CritRate #Saving value for later use if necessary
    DHRateBonus = DHRate #Saving value for later use if necessary

    if type == 0: #Making sure its not an AA or DOT
        if isinstance(Player, Machinist): 
            #Then if machinist, has to check if direct crit guarantee
            if Player.ActionSet[Player.NextSpell].id != -1 and Player.ActionSet[Player.NextSpell].id != -2 and Player.Reassemble and Player.ActionSet[Player.NextSpell].Weaponskill:    #Checks if reassemble is on and if its a weapon skill
                CritRate = 1
                DHRate = 1
                Player.Reassemble = False #Uses Reassemble    
                auto_crit = True
                auto_DH = True   
        elif isinstance(Player, Warrior):
            if Player.InnerReleaseStack >= 1 and (Player.NextSpell < len(Player.ActionSet)) and (Player.ActionSet[Player.NextSpell].id == 9 or Player.ActionSet[Player.NextSpell].id == 8 or Player.ActionSet[Player.NextSpell].id == 10):
                CritRate = 1#If inner release weaponskill
                DHRate = 1
                Player.InnerReleaseStack -= 1
                auto_crit = True
                auto_DH = True
        elif isinstance(Player, Samurai):
            if Player.DirectCrit:
                CritRate = 1
                DHRate = 1
                Player.DirectCrit = False
                auto_crit = True
                auto_DH = True
        elif isinstance(Player, Dancer):
            if Player.NextDirectCrit:
                CritRate = 1
                DHRate = 1
                Player.NextDirectCrit = False
                auto_crit = True
                auto_DH = True
        elif isinstance(Player, Dragoon):
            if Player.NextCrit and Player.ActionSet[Player.NextSpell].Weaponskill: #If next crit and weaponskill
                CritRate = 1
                Player.NextCrit = False
                auto_crit = True


    if type == 0: #Type 0 is direct damage
        Damage = math.floor(math.floor(math.floor(math.floor(Potency * f_MAIN_DMG * f_DET) * f_TEN ) *f_WD) * Player.Trait) #Player.Trait is trait DPS bonus
        Damage = math.floor(Damage * SpellBonus)
        Player.NumberDamageSpell += 1
        Player.CritRateHistory += [CritRate]
    elif type == 1 : #Type 1 is magical DOT
        Damage = math.floor(math.floor(math.floor(math.floor(math.floor(math.floor(Potency * f_WD) * f_MAIN_DMG) * f_SPD) * f_DET) * f_TEN) * Player.Trait) + 1
        
        if not spellObj.onceThroughFlag:#If we haven't gotten through with this DOT once, we have to snapshot the buffs

            if Enemy.ChainStratagem: spellObj.CritBonus += 0.1    #If ChainStratagem is active, increase crit rate
            if Enemy.WanderingMinuet: spellObj.CritBonus += 0.02 #If WanderingMinuet is active, increase crit rate
            if Enemy.BattleVoice: spellObj.DHBonus += 0.2 #If WanderingMinuet is active, increase DHRate
            spellObj.DHBonus += Player.DHRateBonus #Adding Bonus
            spellObj.CritBonus += Player.CritRateBonus #Adding bonus

            for buffs in Player.buffList: 
                spellObj.MultBonus += [buffs] #Adding buff to DOT
            for buffs in Enemy.buffList:
                spellObj.MultBonus += [buffs] #Adding buff to DOT

            #Now the DOT has completely snapshot all possible buff. So we save those
            #and never come back here

            spellObj.onceThroughFlag = True #set flag to True, so never snapshot again

    elif type == 2: #Physical DOT
        Damage = math.floor(math.floor(math.floor(math.floor(math.floor(Potency * f_MAIN_DMG * f_DET) * f_TEN) * f_SPD) * f_WD) * Player.Trait) +1
    
        if not spellObj.onceThroughFlag:#If we haven't gotten through with this DOT once, we have to snapshot the buffs

            if Enemy.ChainStratagem: spellObj.CritBonus += 0.1    #If ChainStratagem is active, increase crit rate
            if Enemy.WanderingMinuet: spellObj.CritBonus += 0.02 #If WanderingMinuet is active, increase crit rate
            if Enemy.BattleVoice: spellObj.DHBonus += 0.2 #If WanderingMinuet is active, increase DHRate
            spellObj.DHBonus += Player.DHRateBonus #Adding Bonus
            spellObj.CritBonus += Player.CritRateBonus #Adding bonus

            for buffs in Player.buffList: 
                spellObj.MultBonus += [buffs] #Adding buff to DOT
            for buffs in Enemy.buffList:
                spellObj.MultBonus += [buffs] #Adding buff to DOT

            #Now the DOT has completely snapshot all possible buff. So we save those
            #and never come back here

            spellObj.onceThroughFlag = True #set flag to True, so never snapshot again

    elif type == 3: #Auto-attacks
        Damage = math.floor(math.floor(math.floor(Potency * f_MAIN_DMG * f_DET) * f_TEN) * f_SPD)
        Damage = math.floor(math.floor(Damage * math.floor(f_WD * (Player.Delay/3) *100 )/100) * Player.Trait)
    #Now applying buffs

    if type == 0 or type == 3: #If Action or AA, then we apply the current buffs
        for buffs in Player.buffList: 
            Damage = math.floor(Damage * buffs.MultDPS) #Multiplying all buffs
        for buffs in Enemy.buffList:
            Damage = math.floor(Damage * buffs.MultDPS) #Multiplying all buffs
    else: #if type is 1 or 2, then its a DOT, so we have to use the snapshotted buffs
        for buffs in spellObj.MultBonus:
            Damage = math.floor(Damage * buffs.MultDPS)
    """
    if math.floor(math.floor(Damage * (1 + roundDown(CritRate * CritMult, 3)) ) * (1 + roundDown((DHRate * 0.25), 2))) > 100000 : 
        print("WOWOWOW HIGH DAMAGE : " + str(math.floor(math.floor(Damage * (1 + roundDown(CritRate * CritMult, 3)) ) * (1 + roundDown((DHRate * 0.25), 2)))))
        print(spellObj)
        print(DHRate)
        print(Player.DHRate)
        print(Player.CritRate)
        print(CritRate)
        print("Damage : " + str(Damage))
        print("DH Damage : " + str(math.floor(Damage * ( 1 + roundDown((DHRate * 0.25), 2)))))
        print("Crit damage : " + str(math.floor(Damage * (1 + roundDown(CritRate * CritMult, 3)) )))
        x = 1
        for buffs in Player.buffList: 
            input("buff : " + str(buffs.MultDPS))
            x *= buffs.MultDPS
            input("x " + str(x))
        print("ONTO BOSS")
        for buffs in Enemy.buffList:
            input("buff : " + str(buffs.MultDPS))
            x *= buffs.MultDPS
            input("x " + str(x))
        input(spellObj.id)
        """
#crit = (1 + status_effect_rate * cdmg bonus)
#dh = ( 1 + status_effect_rate * 0.25)

    #Here I am returning both the damage assuming no crit and expected dh_rate and the damage with expected dh_rate and crit_rate.
    #I am also adding all buffs before sending it

    
    if auto_crit and auto_DH: #If both 
        auto_crit_bonus = (1 + roundDown(CritRateBonus * CritMult, 3)) #Auto_crit bonus if buffed
        auto_dh_bonus = (1 + roundDown(DHRateBonus * 0.25, 2)) #Auto_DH bonus if buffed
        non_crit_dh_expected, dh_crit_expected = math.floor(math.floor(Damage * (1 + roundDown(CritRate * CritMult, 3)) ) * (1 + roundDown((DHRate * 0.25), 2))), math.floor(math.floor(Damage * (1 + roundDown((CritRate * CritMult), 3)) ) * (1 + roundDown((DHRate * 0.25), 2)))
        return math.floor(math.floor(non_crit_dh_expected * auto_crit_bonus) * auto_dh_bonus), math.floor(math.floor(dh_crit_expected * auto_crit_bonus) * auto_dh_bonus)
    elif auto_crit: #If sure to crit, add crit to min expected damage
        auto_crit_bonus = (1 + roundDown(CritRateBonus * CritMult, 3)) #Auto_crit bonus if buffed
        non_crit_dh_expected, dh_crit_expected = math.floor(math.floor(Damage * (1 + roundDown(CritRate * CritMult, 3)) ) * (1 + roundDown((DHRate * 0.25), 2))), math.floor(math.floor(Damage * (1 + roundDown((CritRate * CritMult), 3)) ) * (1 + roundDown((DHRate * 0.25), 2))) #If we have auto crit, we return full damage
        return math.floor(non_crit_dh_expected * auto_crit_bonus), math.floor(dh_crit_expected * auto_crit_bonus) 
    else:#No auto_crit or auto_DH
        non_crit_dh_expected, dh_crit_expected = math.floor(Damage * ( 1 + roundDown((DHRate * 0.25), 2))), math.floor(math.floor(Damage * (1 + roundDown((CritRate * CritMult), 3)) ) * (1 + roundDown((DHRate * 0.25), 2))) #Non crit expected damage, expected damage with crit
        return non_crit_dh_expected , dh_crit_expected

def roundDown(x, precision):
    return math.floor(x * 10**precision)/10**precision
    #Imagine not having a built in function to rounddown floats :x

"""
#Original ComputeDamage function

def ComputeDamageV2(Player, DPS, EnemyBonus, SpellBonus):
    #This function will compute the DPS given the stats of a player

    levelMod = 1900
    baseMain = 390  
    baseSub = 400
    JobMod = Player.JobMod

    MainStat = Player.Stat["MainStat"] * Player.CurrentFight.TeamCompositionBonus #Scaling %bonus

    Damage=math.floor(DPS*(Player.Stat["WD"]+math.floor(baseMain*JobMod/1000))*(100+math.floor((MainStat-baseMain)*195/baseMain))/100)

    Damage=math.floor(Damage*(1000+math.floor(140*(Player.Stat["Det"]-baseMain)/levelMod))/1000)#Determination damage

    Damage=math.floor(Damage*(1000+math.floor(100*(Player.Stat["Ten"]-baseSub)/levelMod))/1000)#Tenacity damage

    Damage=math.floor(Damage*(1000+math.floor(130*(Player.Stat["SS"]-baseSub)/levelMod))/1000)#Spell/Skill speed damage bonus, only on DOT

    Damage = math.floor(Damage * EnemyBonus * SpellBonus)
    ##input("Damage inside v1.0 : " + str(Damage))

    CritRate = math.floor((200*(Player.Stat["Crit"]-baseSub)/levelMod+50))/1000

    CritMult = (math.floor(200*(Player.Stat["Crit"]-baseSub)/levelMod+400))/1000

    DHRate = math.floor(550*(Player.Stat["DH"]-baseSub)/levelMod)/1000

    if Player.CurrentFight.Enemy.ChainStratagem: CritRate += 0.1    #If ChainStratagem is active, increase crit

    if Player.CurrentFight.Enemy.WanderingMinuet: CritRate += 0.02 #If WanderingMinuet is active, increase crit

    if Player.CurrentFight.Enemy.BattleVoice: DHRate += 0.2 #If WanderingMinuet is active, increase crit


    

    DHRate += Player.DHRateBonus #Adding Bonus
    CritRate += Player.CritRateBonus #Adding bonus

    if isinstance(Player, Machinist): 
        #print(Player.ActionSet[Player.NextSpell])  #Then if machinist, has to check if direct crit guarantee
        if Player.ActionSet[Player.NextSpell].id != -1 and Player.ActionSet[Player.NextSpell].id != -2 and Player.Reassemble and Player.ActionSet[Player.NextSpell].Weaponskill:    #Checks if reassemble is on and if its a weapon skill
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
    elif isinstance(Player, Dancer):
        if Player.NextDirectCrit:
            CritRate = 1
            DHRate = 1
            Player.NextDirectCrit = False
    elif isinstance(Player, Dragoon):
        if Player.NextCrit and Player.ActionSet[Player.NextSpell].Weaponskill: #If next crit and weaponskill
            CritRate = 1
            Player.NextCrit = False

    return round(Damage * ((1+(DHRate/4))*(1+(CritRate*CritMult)))/100, 2)

    // Pulled from Orinx's Gear Comparison Sheet with slight modifications
function Damage(Potency, WD, JobMod, MainStat,Det, Crit, DH,SS,TEN, hasBrd, hasDrg, hasSch, hasDnc, classNum) {
  
  MainStat=Math.floor(MainStat*(1+0.01*classNum));
  var Damage=Math.floor(Potency*(WD+Math.floor(baseMain*JobMod/1000))*(100+Math.floor((MainStat-baseMain)*195/baseMain))/100);
  Damage=Math.floor(Damage*(1000+Math.floor(140*(Det-baseMain)/levelMod))/1000);
  Damage=Math.floor(Damage*(1000+Math.floor(100*(TEN-baseSub)/levelMod))/1000);
  Damage=Math.floor(Damage*(1000+Math.floor(130*(SS-baseSub)/levelMod))/1000/100);
  Damage=Math.floor(Damage*magicAndMend)
  Damage=Math.floor(Damage*enochian)
  var CritMult=CalcCritMult(Crit)
  var CritRate=CalcCritRate(Crit) + (hasDrg ? battleLitanyAvg : 0) + (hasSch ? chainStratAvg : 0) + (hasDnc ? devilmentAvg : 0) + (hasBrd ? brdCritAvg : 0);
  var DHRate=CalcDHRate(DH) + (hasBrd ? battleVoiceAvg + brdDhAvg : 0) + (hasDnc ? devilmentAvg : 0);
  return Damage * ((1+(DHRate/4))*(1+(CritRate*CritMult)))                                                                                                                               
}

"""