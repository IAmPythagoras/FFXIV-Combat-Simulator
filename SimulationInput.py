from Enemy import Enemy
from Fight import Fight

from Jobs.Base_Spell import Melee_AA, Ranged_AA, WaitAbility, Potion
from Jobs.Caster.Caster_Spell import *
from Jobs.Melee.Melee_Spell import *
from Jobs.Ranged.Ranged_Spell import *
from Jobs.Healer.Healer_Spell import *
from Jobs.Tank.Tank_Spell import *

#CASTER
from Jobs.Caster.Summoner.Summoner_Spell import *
from Jobs.Caster.Blackmage.BlackMage_Spell import * 
from Jobs.Caster.Redmage.Redmage_Spell import *
from Jobs.Caster.Summoner.Summoner_Player import *
from Jobs.Caster.Blackmage.BlackMage_Player import * 
from Jobs.Caster.Redmage.Redmage_Player import *

#HEALER
from Jobs.Healer.Sage.Sage_Spell import *
from Jobs.Healer.Scholar.Scholar_Spell import *
from Jobs.Healer.Whitemage.Whitemage_Spell import *
from Jobs.Healer.Astrologian.Astrologian_Spell import *
from Jobs.Healer.Sage.Sage_Player import *
from Jobs.Healer.Scholar.Scholar_Player import *
from Jobs.Healer.Whitemage.Whitemage_Player import *
from Jobs.Healer.Astrologian.Astrologian_Player import *

#RANGED
from Jobs.Ranged.Machinist.Machinist_Spell import *
from Jobs.Ranged.Bard.Bard_Spell import *
from Jobs.Ranged.Dancer.Dancer_Spell import *
from Jobs.Ranged.Machinist.Machinist_Player import *
from Jobs.Ranged.Bard.Bard_Player import *
from Jobs.Ranged.Dancer.Dancer_Player import *

#TANK
from Jobs.Tank.Gunbreaker.Gunbreaker_Spell import *
from Jobs.Tank.DarkKnight.DarkKnight_Spell import *
from Jobs.Tank.Warrior.Warrior_Spell import *
from Jobs.Tank.Paladin.Paladin_Spell import *
from Jobs.Tank.Gunbreaker.Gunbreaker_Player import *
from Jobs.Tank.DarkKnight.DarkKnight_Player import *
from Jobs.Tank.Warrior.Warrior_Player import *
from Jobs.Tank.Paladin.Paladin_Player import *

#MELEE
from Jobs.Melee.Samurai.Samurai_Spell import *
from Jobs.Melee.Ninja.Ninja_Spell import *
from Jobs.Melee.Dragoon.Dragoon_Spell import *
from Jobs.Melee.Reaper.Reaper_Spell import *
from Jobs.Melee.Monk.Monk_Spell import *
from Jobs.Melee.Samurai.Samurai_Player import *
from Jobs.Melee.Ninja.Ninja_Player import *
from Jobs.Melee.Dragoon.Dragoon_Player import *
from Jobs.Melee.Reaper.Reaper_Player import *
from Jobs.Melee.Monk.Monk_Player import *

def ExecuteMemoryCode(SaveFight):
    # This part of the code will execute whatever rotation is written here. It will be called from TUI.

    Dummy = Enemy()
    Event = Fight([], Dummy, False)


    # ===============================================================================================
    # You don't need to to worry about anything above this point

    # Stat Sheet
    # Enter your own stats here. The default is the 6.2 Savage BiS. The default Tenacity for non-tank is 400.
    # These stats must include the bonus gotten from food.

    # Caster
    BLMStat = {"MainStat": 2571, "WD":120, "Det" : 1752, "Ten" : 400, "SS": 758, "Crit" : 2287, "DH" : 965} # Stats for BlackMage
    RDMStat = {"MainStat": 2563, "WD":120, "Det" : 1669, "Ten" : 400, "SS": 400, "Crit" : 2348, "DH" : 1340} # Stats for RedMage
    SMNStat = {"MainStat": 2575, "WD":120, "Det" : 1688, "Ten" : 400, "SS": 489, "Crit" : 2296, "DH" : 1289} # Stats for Summoner

    # Healer
    SCHStat = {"MainStat": 2560, "WD":120, "Det" : 1951, "Ten" : 400, "SS": 944, "Crit" : 2277, "DH" : 616} # Stats for Scholar
    WHMStat = {"MainStat": 2571, "WD":120, "Det" : 1830, "Ten" : 400, "SS": 489, "Crit" : 2301, "DH" : 940} # Stats for WhiteMage
    ASTStat = {"MainStat": 2560, "WD":120, "Det" : 1951, "Ten" : 400, "SS": 716, "Crit" : 2277, "DH" : 844} # Stats for Astrologian
    SGEStat = {"MainStat": 2563, "WD":120, "Det" : 1953, "Ten" : 400, "SS": 656, "Crit" : 2244, "DH" : 904} # Stats for Sage

    # Physical Ranged
    MCHStat = {"MainStat": 2572, "WD":120, "Det" : 1615, "Ten" : 400, "SS": 400, "Crit" : 2121, "DH" : 1626} # Stats for Machinist
    BRDStat = {"MainStat": 2575, "WD":120, "Det" : 1381, "Ten" : 400, "SS": 479, "Crit" : 2229, "DH" : 1662} # Stats for Bard
    DNCStat = {"MainStat": 2575, "WD":120, "Det" : 1453, "Ten" : 400, "SS": 549, "Crit" : 2283, "DH" : 1477} # Stats for Dancer
    
    # Melee
    NINStat = {"MainStat": 2555, "WD":120, "Det" : 1749, "Ten" : 400, "SS": 400, "Crit" : 2283, "DH" : 1330} # Stats for Ninja
    SAMStat = {"MainStat": 2563, "WD":120, "Det" : 1654, "Ten" : 400, "SS": 579, "Crit" : 2310, "DH" : 1217} # Stats for Samurai
    DRGStat = {"MainStat": 2575, "WD":120, "Det" : 1846, "Ten" : 400, "SS": 400, "Crit" : 2281, "DH" : 1235} # Stats for Dragoon
    MNKStat = {"MainStat": 3076, "WD":126, "Det" : 1546, "Ten" : 400, "SS": 769, "Crit" : 2490, "DH" : 1179} # Stats for Monk
    RPRStat = {"MainStat": 2575, "WD":120, "Det" : 1846, "Ten" : 400, "SS": 400, "Crit" : 2281, "DH" : 1235} # Stats for Reaper

    # Tank
    DRKStat = {"MainStat": 2521, "WD":120, "Det" : 1680, "Ten" : 539, "SS": 650, "Crit" : 2343, "DH" : 976} # Stats for DarkKnight
    WARStat = {"MainStat": 2521, "WD":120, "Det" : 2130, "Ten" : 1018, "SS": 400, "Crit" : 2240, "DH" : 400} # Stats for Warrior
    PLDStat = {"MainStat": 2502, "WD":120, "Det" : 1680, "Ten" : 527, "SS": 650, "Crit" : 2319, "DH" : 1012} # Stats for Paladin
    GNBStat = {"MainStat": 2517, "WD":120, "Det" : 1612, "Ten" : 527, "SS": 950, "Crit" : 2205, "DH" : 868} # Stats for Gunbreaker

    # ===============================================================================================

    # Here the player objects are being initialized. You do not need to change anything here.
    # Note that if you want to simulate with two players of the same Jobs you will need to create another Player Object here.
    # You can simply copy the objet's __init__ and change the name. 

    # Caster player object
    BLMPlayer = BlackMage(2.5, [], [], [EnochianEffect, ElementalEffect], Event, BLMStat)
    RDMPlayer = Redmage(2.5, [], [], [DualCastEffect], Event, RDMStat)
    SMNPlayer = Summoner(2.5, [], [], [], Event, SMNStat)

    # Healer player object
    SCHPlayer = Scholar(2.5, [], [], [], Event, SCHStat)
    WHMPlayer = Whitemage(2.5, [], [], [], Event, WHMStat)
    SGEPlayer = Sage(2.5, [], [], [], Event, SGEStat)
    ASTPlayer = Astrologian(2.5, [], [], [], Event, ASTStat)

    # Physical Ranged
    MCHPlayer = Machinist(2.5, [], [], [], Event, MCHStat)
    BRDPlayer = Bard(2.5, [], [], [SongEffect], Event, BRDStat)
    DNCPlayer = Dancer(2.5, [], [], [EspritEffect], Event, DNCStat)
    
    # Melee
    NINPlayer = Ninja(2.5, [], [], [], Event, NINStat)
    SAMPlayer = Samurai(2.5, [], [], [], Event, SAMStat)
    DRGPlayer = Dragoon(2.5, [], [], [], Event, DRGStat)
    RPRPlayer = Reaper(2.5, [], [], [], Event, RPRStat)
    MNKPlayer = Monk(2.5, [], [], [ComboEffect,FormlessStackCheck], Event, MNKStat)

    # Tank
    DRKPlayer = DarkKnight(2.5, [], [], [], Event, DRKStat)
    WARPlayer = Warrior(2.5, [], [], [SurgingTempestEffect], Event, WARStat)
    PLDPlayer = Paladin(2.5, [], [], [], Event, PLDStat)
    GNBPlayer = Gunbreaker(2.5, [], [], [], Event, GNBStat)


    # ===============================================================================================

    # Here you can enter the action list you want the simulator to simulate. If you want to simulate a BlackMage go to the respective list, in that case you would write in BLMOpener\
    # Note that this action list also includes the prepull. So use the function WaitAbility() so the player starts doing damage as the fight starts and not earlier as the simulator
    # will not start earlier if someone pulls early.
    # Note that if you are simulating with more than 1 per job you will need to create a new list of actions.

    # Refer to page (ADD PAGE NUMBERS) for more information.

    # Caster
    BLMOpener = []
    SMNOpener = []
    RDMOpener = []
    
    # Healer
    SCHOpener = []
    WHMOpener = []
    ASTOpener = []
    SGEOpener = []

    # Physical Ranged
    BRDOpener = []
    MCHOpener = []
    DNCOpener = []

    # Melee
    SAMOpener = []
    GNBOpener = []
    DRGOpener = []
    MNKOpener = []
    NINOpener = []

    # Tank
    DRKOpener = []
    WAROpener = []
    PLDOpener = []
    RPROpener = []


    # ===============================================================================================

    # Here we are linking the earlier created action list to the player object. You should not have to change anything here except if you are trying to simulate
    # with more than 1 player per job. In which case you will need to link the earlier created object and the earlier created action list.

    # Caster
    BLMPlayer.ActionSet = BLMOpener
    RDMPlayer.ActionSet = RDMOpener
    SMNPlayer.ActionSet = SMNOpener

    # Healer
    SCHPlayer.ActionSet = SCHOpener
    WHMPlayer.ActionSet = WHMOpener
    ASTPlayer.ActionSet = ASTOpener
    SGEPlayer.ActionSet = SGEOpener

    # Physical Ranged
    MCHPlayer.ActionSet = MCHOpener
    BRDPlayer.ActionSet = BRDOpener
    DNCPlayer.ActionSet = DNCOpener

    # Melee
    NINPlayer.ActionSet = NINOpener
    SAMPlayer.ActionSet = SAMOpener
    DRGPlayer.ActionSet = DRGOpener
    RPRPlayer.ActionSet = RPROpener
    MNKPlayer.ActionSet = MNKOpener

    #Tank
    DRKPlayer.ActionSet = DRKOpener
    WARPlayer.ActionSet = WAROpener
    PLDPlayer.ActionSet = PLDOpener
    GNBPlayer.ActionSet = GNBOpener

    # ===============================================================================================

    # Here you will put into this list all the players you wish to simulate.
    # Note that the limit is not 8, you can put as much as you want.
    # Furthemore the simulator will compute the bonus 5% if it applies.
    # So if you want to simulate the BlackMage and a RedMage, you would do: 
    # PlayerList = [BLMPlayer, RDMPlayer]

    PlayerList = []

    Event.PlayerList = PlayerList

    # ===============================================================================================

    # Here you can change the final parameters to the simulation

    Countdown = 20 # Value of the countdown in seconds
    TimeLimit = 1000 # Time limit for the simulation in seconds. It will stop once this time has been reached (in simulation time)
    time_unit = 0.01 # Time unit or frame of the simulation. Smallest step the simulator will take between each iterations. It is advised to not change this value
    ShowGraph = True # Parameter to show (or not) the graph generated by the simulator.

    # ===============================================================================================

    if SaveFight: #If we wish to save the fight
        pass
    else:
        Event.ShowGraph = ShowGraph
        Event.SimulateFight(time_unit, TimeLimit, Countdown)


