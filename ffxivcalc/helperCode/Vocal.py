"""
This module contains all function used to verbally show a simulation's result to the user
and all other functions used to process the information offered by the library.   
"""
import math
import numpy as np
import logging
import matplotlib.pyplot as plt
logging.getLogger('matplotlib').setLevel(logging.INFO) # silencing matplotlib logger
logging.getLogger('PIL').setLevel(logging.INFO) # silencing PIL logger

from ffxivcalc.Jobs.PlayerEnum import JobEnum

# Functions related to computing and plotting graph of DPS distribution

def Normal(mean, std, x):# returns value from NormalDistribution
    if std == 0 : return 0
    return 1/(std * np.sqrt(2 * np.pi)) * np.exp(-1/2 * ((x-mean)/std)**2)

def AverageCritMult(Player, k):
    n = Player.NumberDamageSpell # Total number of damage Spell
    if n == 0 : return 0
    # k is the number of success, so the number of crit
    return ((k) * (1 + Player.CritMult)  + (n-k))/n # Average crit multiplier over the run, this can be seen as a fix bonus on the whole fight

def ComputeDPSDistribution(self, Player, fig, axs, job):
    # THIS WHOLE PART HAS BEEN SHOWN TO NOT BE ACCURATE AND IS NOT FIXED AS OF NOW
    # USE AT YOUR OWN RISK

    # Graph data
    axs.set_ylabel("Percentage (%)")
    axs.set_xlabel("Expected DPS")
    axs.set_title(job + " DPS Distribution")
    axs.spines["top"].set_alpha(0.0)
    axs.spines["right"].set_alpha(0.0)
    axs.set_facecolor("lightgrey")
    # axs.yaxis.set_ticks(np.arange(0,15,1))




    # This function will return a distribution of DPS and chance of having certain DPS
    Player.DPS = Player.TotalMinDamage / self.TimeStamp # Computing DPS with no crit, expected DH
    Player.ExpectedDPS = Player.TotalDamage / self.TimeStamp # Expected DPS with crit

    n = Player.NumberDamageSpell # Number of spell that deals damage done by this player
    p = round((Player.ExpectedDPS/Player.DPS - 1)/Player.CritMult,3)

    # The value of p is found by using the fact that Player.DPS = DPS * ExpectedDHDamage, Player.ExpectedDPS = DPS * ExpectedDHDamage * ExpectedCritDamage
    # And ExpectedCritDamage = ( 1 + (CritMult * CritRate)), so we simply isolate CritRate. This will give an average Crit rate over the whole fight which will
    # take into account crit rate buffs throughout the fight
    decimal_mean = n*p # Number of expected crit (not an integer)
    mean = math.floor(decimal_mean) # Number of expected crit rounded down
    radius = math.ceil(n/2) # Radius we for which we will graph the distribution
    std = n*p * (1-p) # Standard deviation
    # The binomial distribution of enough trials can be approximated to N(np, np(1-p)) for big enough n, so we will simply approximate the distribution by this
    # Note that here n stands for the number of damage spell, and p is the averagecritrate of the player AverageCritRate = (CritRate + CritRateBonus)/time
    # We will salvage values from the normal distribution, then find the average crit multiplier by number of crits gotten. We will then multiply the computed DPS
    # by these multipliers to get DPS values for each chance
    # We will sample n/2 points on each side

    y_list = []
    expected_dps_list = [] # List of expected DPS
    resolution = 500 # Hardcoded value, represents how many points on the curve we take
    i = max(0, mean-radius) # Starting point
    j = mean + radius+1 # Upper limit
    h = (j - i)/resolution # Step to take
    x_list = np.linspace(i,j,resolution) # Evenly spaced out from i -> j with resolution number of points
    # It will be computed by computing an average crit multiplier, and then multiplying the DPS by that
    while i < j:
        next_point = Normal(decimal_mean, std, i) * 100000 / 10
        # input(next_point)
        y_list += [math.floor(next_point)/100]
        average_crit_mult = AverageCritMult(Player, i)
        expected_dps_list += [average_crit_mult * Player.DPS]
        i+= h


    high_crit_mult_list = []
    low_crit_mult_list = []
    for i in range(1,4): # This loop will create boundary for the empirical rules, it will do 1 to 3 std away from the mean
        high = decimal_mean + i*std
        low = decimal_mean - i*std
        high_crit_mult = AverageCritMult(Player, high)
        low_crit_mult = AverageCritMult(Player, low)
        high_crit_mult_list += [high_crit_mult * Player.DPS]
        low_crit_mult_list += [low_crit_mult * Player.DPS]
    # Even though low and high are not integers, the AverageCritMult is a continuous stricly increasing function, so we can use it on
    # non integer value to get an "in-between" value

    top_graph = max(y_list) * 1.3 # top of graph
    lab = "\u03BC = " + str(round(Player.ExpectedDPS,1)) + " \u03C3 = " + str(round(std,2))
    axs.plot(expected_dps_list, y_list,label=lab) # Distribution
    axs.plot([Player.ExpectedDPS,Player.ExpectedDPS], [0,top_graph], label="Expected DPS", linestyle="dashed") # Expected DPS
    # Plotting Empirical rule region
    axs.axvspan(max(expected_dps_list[0],low_crit_mult_list[2]), min(expected_dps_list[-1],high_crit_mult_list[2]), color="green") # 99.7% empirical rule region, will most likely not appear in the graph
    axs.axvspan(max(expected_dps_list[0],low_crit_mult_list[1]), high_crit_mult_list[1], color="blue") # 95% empirical rule region
    axs.axvspan(low_crit_mult_list[0], high_crit_mult_list[0], color="red") # 68% empirical rule region


    axs.fill_between(expected_dps_list, y_list,top_graph, fc="lightgrey") # Used to cover the vertical regions from axvspan so they stop under the line of the distribution
    axs.margins(-0.0001) # margin arrangement
    axs.legend()

def SimulateRuns(fight, n : int):
    """
    This function will simulate the fight with ZIPActions the given number of time and will
    generate the DPS distribution from it
    n (int) -> Number of times to run the random simulation
    """

    for i in range(n):
        fight.SimulateZIPFight()
    fig, axs = plt.subplots(2, 4, constrained_layout=True) # DPS Crit distribution
    i = 0 # Used as coordinate for DPS distribution graph
    j = 0

    for player in fight.PlayerList:
        for runs in player.ZIPDPSRun:
            if str(runs) in player.DPSBar.keys():
                player.DPSBar[str(runs)] += 1
            else:
                player.DPSBar[str(runs)] = 1

        # ordering dict
        keys = list(player.DPSBar.keys())
        keys.sort()
        data = {i : player.DPSBar[i] for i in keys}


        x = []
        y = []
        for bar in data:
            x += [float(bar)]
            y += [player.DPSBar[bar]/n]
        axs[i][j].plot(x, y)
        if len(fight.PlayerList) <= 8:
            i+=1
            if i == 4:
                i = 0
                j+=1
    plt.show()

# Functions to print out all the results and plot DPS/PPS graph

def PrintResult(self, time : float, TimeStamp, PPSGraph : bool = True) -> str:
    """
    This function puts the result in a string that it will return which can then be printed
    self : Fight -> Fight we want the result of to be printed
    time : float -> final timestamp of the simulation
    TimeStamp : List[float] -> list of all timestamp where the DPS was saved in memory. Used to generate the graphs
    PPSGraph : bool -> If want the PPS graph next to the DPS graph
    """

    result_string = "The Fight finishes at: " + str(time) + "\n========================\n" 
    fig, axs = plt.subplots(1, 2 if PPSGraph else 1, constrained_layout=True) # DPS and PPS graph
    if PPSGraph:
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
    else:
        axs.set_ylabel("DPS")
        axs.set_xlabel("Time (s)")
        axs.set_title("DPS over time")
        axs.spines["top"].set_alpha(0.0)
        axs.spines["right"].set_alpha(0.0)
        axs.set_facecolor("lightgrey")

    fig.suptitle("Damage over time.")

    i = 0 # Used as coordinate for DPS distribution graph
    j = 0

    for player in self.PlayerList:

        if time == 0: time = 1 # This is only so we don't have division by 0 error

        if player.TotalPotency == 0:
            PPS = 0
            DPS = 0
        else:
            PPS = player.TotalPotency / time
            DPS = player.TotalDamage / time
        
        result_string += (
            "Results for " + str(JobEnum.name_for_id(player.JobEnum)) + ("" if player.PlayerName == "" else " " + player.PlayerName) + " ID - " + str(player.playerID) + " :\n" + 
            "DPS : " + str(round(DPS,2)) + 
            " PPS : " + str(round(PPS,2)) + 
            " TP : " + str(round(player.TotalPotency,2)) + 
            " GCD : " + str(player.GCDCounter) + "\n"
        )


        # Plot part

        job = JobEnum.name_for_id(player.JobEnum)

        
        if player.JobEnum == JobEnum.Bard : 
            result_string += (
            "Procs/Gauge result (Used/Expected) : \n" +
            "Refulgent : " + str(round(player.ExpectedRefulgent,2)) + "/" + str(round(player.UsedRefulgent,2)) + 
            " Wanderer Repertoire : " + str(round(player.ExpectedTotalWandererRepertoire,2)) + "/" + str(round(player.UsedTotalWandererRepertoire,2)) +
            " RepertoireAdd : " + str(round(player.UsedRepertoireAdd,2)) + 
            "\nSoul Voice : " + str(round(player.ExpectedSoulVoiceGauge,2)) + "/" + str(round(player.UsedSoulVoiceGauge,2)) +
            " Soul BloodLetter Reduction : " + str(round(player.ExpectedBloodLetterReduction,2)) + "/" + str(round(player.UsedBloodLetterReduction,2))
                             )
        elif player.JobEnum == JobEnum.Dancer:
            result_string += (
            "Procs/Gauge result (Used/Expected) : \n" +
            "Silken Symettry : " + str(round(player.ExpectedSilkenSymettry,2)) + "/" + str(round(player.UsedSilkenSymettry,2)) + 
            " Silken Flow : " + str(round(player.ExpectedSilkenFlow,2)) + "/" + str(round(player.UsedSilkenFlow,2)) +
            "\nFourfold Feather : " + str(round(player.ExpectedFourfoldFeather,2)) + "/" + str(round(player.UsedFourfoldFeather,2)) +
            " Threefold Fan : " + str(round(player.ExpectedThreefoldFan,2)) + "/" + str(round(player.UsedThreefoldFan,2))
                             )
        elif player.JobEnum == JobEnum.RedMage:
            result_string += (
            "Procs/Gauge result (Used/Expected) : \n" +
            "Verfire : " + str(round(player.ExpectedVerfireProc,2)) + "/" + str(round(player.UsedVerfireProc,2)) + 
            " Verstone : " + str(round(player.ExpectedVerstoneProc,2)) + "/" + str(round(player.UsedVerstoneProc,2)) 
                             )


        result_string += "\n=================\n"

        job_label = job + ("" if player.PlayerName == "" else (" " + player.PlayerName)) + " ID - " + str(player.playerID)
        if PPSGraph:
            axs[0].plot(TimeStamp,player.DPSGraph, label=job_label)
            axs[1].plot(TimeStamp,player.PotencyGraph, label=job_label)
        else:
            axs.plot(TimeStamp,player.DPSGraph, label=job_label)

        #if len(self.PlayerList) <= 8:
        #    if DPS != 0 : ComputeDPSDistribution(self, player, fig2, axs2[j][i], job)
        #    i+=1
        #    if i == 4:
        #        i = 0
        #        j+=1
    result_string += (
        "Total DPS : " + str(round(self.Enemy.TotalDamage / time, 2) if time != 0 else "0" ) + "\t" +
        "Total PPS : " + str(round(self.Enemy.TotalPotency/time,2) if time != 0 else "0" ) + "\t" +
        "Total Potency : " + str(round(self.Enemy.TotalPotency,2))
    )
    if PPSGraph: 
        axs[0].xaxis.grid(True)
        axs[1].xaxis.grid(True)
    else:
        axs.legend()
        
    if len(TimeStamp) == 0: # If for some reason Fight ended before 3 second TimeStamp is empty and we need to do an edge case to avoid a crash
        # Note that however the plot will be empty since no damage has been sampled
        if PPSGraph: 
            axs[0].xaxis.set_ticks(np.arange(0, 4, 25))
            axs[1].xaxis.set_ticks(np.arange(0, 4, 25))
        else:
            axs.xaxis.set_ticks(np.arange(0, 4, 25))
    else:
        if PPSGraph: 
            axs[0].xaxis.set_ticks(np.arange(0, max(TimeStamp)+1, 25))
            axs[1].xaxis.set_ticks(np.arange(0, max(TimeStamp)+1, 25))
        else:
            axs.xaxis.set_ticks(np.arange(0, max(TimeStamp)+1, 25))

    if PPSGraph: 
        axs[0].legend()
        axs[1].legend()
    else:
        axs.legend()
    
    if self.ShowGraph: plt.show()

    return result_string, fig