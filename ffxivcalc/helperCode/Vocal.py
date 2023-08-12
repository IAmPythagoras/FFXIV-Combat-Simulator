"""
This module contains all function used to verbally show a simulation's result to the user
and all other functions used to process the information offered by the library.   
"""
import math
import numpy as np
import logging
import matplotlib.pyplot as plt
from ffxivcalc.helperCode.Progress import ProgressBar
from ffxivcalc.helperCode.helper_math import roundDown
logging.getLogger('matplotlib').setLevel(logging.INFO) # silencing matplotlib logger
logging.getLogger('PIL').setLevel(logging.INFO) # silencing PIL logger

from ffxivcalc.Jobs.PlayerEnum import JobEnum

def SimulateRuns(fight, n : int):
    """
    This function will simulate the fight with ZIPActions the given number of time and will
    generate the DPS distribution from it
    n (int) -> Number of times to run the random simulation
    """
    zipFightProgress = ProgressBar.init(n, "Computing DPS Dist")
    for i in range(n):
        fight.SimulateZIPFight()
        next(zipFightProgress)

    l = len(fight.PlayerList)
    fig, axs = plt.subplots((l // 4)+ (1 if l % 4 != 0 else 0), l if l < 4 else 4, constrained_layout=True) # DPS Crit distribution
    fig.suptitle("DPS Distribution (n = "+str(n)+" )")
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

        Percent = int(n/100)
        percentile = [10,25,50,75,90,95,99]
        index = 0
        curTotal = 0
        for key in data:
            curTotal += data[key]
            if curTotal > (Percent * percentile[index]) : 
                player.ZIPRunPercentile[str(percentile[index])] = key
                index += 1
            if index == len(percentile) : break

        x = []
        y = []
        title = "" if player.PlayerName == "" else player.PlayerName + " ID - " + str(player.playerID)
        for bar in data:
            x += [float(bar)]
            y += [player.DPSBar[bar]/n]
        if l == 1:
            axs.plot(x, y)
            axs.plot([player.TotalDamage/fight.TimeStamp,player.TotalDamage/fight.TimeStamp], [0, 0.01])
            axs.set_ylim(ymin=0)
            axs.set_title(title)
        elif l <= 4:
            axs[i].plot(x, y)
            axs[i].plot([player.TotalDamage/fight.TimeStamp,player.TotalDamage/fight.TimeStamp], [0, 0.01])
            axs[i].set_ylim(ymin=0)
            axs[i].set_title(title)
        else:
            axs[j][i].plot(x, y)
            axs[j][i].plot([player.TotalDamage/fight.TimeStamp,player.TotalDamage/fight.TimeStamp], [0, 0.01])
            axs[j][i].set_ylim(ymin=0)
            axs[j][i].set_title(title)
        i+=1
        if i == 4:
            i = 0
            j+=1
    return fig
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
    HPFig, HPaxs = plt.subplots(1,1, constrained_layout=True)

    HPaxs.set_ylabel("HP")
    HPaxs.set_xlabel("Time (s)")
    HPaxs.set_title("HP over time")
    HPaxs.spines["top"].set_alpha(0.0)
    HPaxs.spines["right"].set_alpha(0.0)
    HPaxs.set_facecolor("lightgrey")

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
        HPaxs.plot(player.HPGraph[0], player.HPGraph[1], color="green")
        HPaxs.set_ylim(ymin=0)
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

        # DPS Percentile if applies

        result_string += ("DPS Percentile" + str(player.ZIPRunPercentile) + "\n") if len(player.ZIPRunPercentile.keys()) > 0 else ""


        # Plot part

        job = JobEnum.name_for_id(player.JobEnum)

        
        if player.JobEnum == JobEnum.Bard : 
            result_string += (
            "Procs/Gauge result (Used/Expecte) : \n" +
            "Refulgent : " + str(round(player.UsedRefulgent,2)) + "/" + str(round(player.ExpectedRefulgent,2)) + 
            " Wanderer Repertoire : " + str(round(player.UsedTotalWandererRepertoire,2)) + "/" + str(round(player.ExpectedTotalWandererRepertoire,2)) +
            " RepertoireAdd : " + str(round(player.UsedRepertoireAdd,2)) + 
            "\nSoul Voice : " + str(round(player.UsedSoulVoiceGauge,2)) + "/" + str(round(player.ExpectedSoulVoiceGauge,2)) +
            " Soul BloodLetter Reduction : " + str(round(player.UsedBloodLetterReduction,2)) + "/" + str(round(player.ExpectedBloodLetterReduction,2))
                             )
        elif player.JobEnum == JobEnum.Dancer:
            result_string += (
            "Procs/Gauge result (Used/Expected) : \n" +
            "Silken Symettry : " + str(round(player.UsedSilkenSymettry,2)) + "/" + str(round(player.ExpectedSilkenSymettry,2)) + 
            " Silken Flow : " + str(round(player.UsedSilkenFlow,2)) + "/" + str(round(player.ExpectedSilkenFlow,2)) +
            "\nFourfold Feather : " + str(round(player.UsedFourfoldFeather,2)) + "/" + str(round(player.ExpectedFourfoldFeather,2)) +
            " Threefold Fan : " + str(round(player.UsedThreefoldFan,2)) + "/" + str(round(player.ExpectedThreefoldFan,2))
                             )
        elif player.JobEnum == JobEnum.RedMage:
            result_string += (
            "Procs/Gauge result (Used/Expected) : \n" +
            "Verfire : " + str(round(player.UsedVerfireProc,2)) + "/" + str(round(player.ExpectedVerfireProc,2)) + 
            " Verstone : " + str(round(player.UsedVerstoneProc,2)) + "/" + str(round(player.ExpectedVerstoneProc,2)) 
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

    return result_string, fig

