import os

from Enemy import Enemy
from Fight import Fight


from Jobs.Base_Spell import WaitAbility, Potion
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
    # Enter your own stats here. The default is the 6.2 Savage BiS found on the Balance. The default Tenacity for non-tank is 400.
    # These stats must include the bonus stats food gives.

    # Caster
    BLMStat = {"MainStat": 2945, "WD":126, "Det" : 1451, "Ten" : 400, "SS": 840, "Crit" : 2386, "DH" : 1307} # Stats for BlackMage
    RDMStat = {"MainStat": 2947, "WD":126, "Det" : 1548, "Ten" : 400, "SS": 495, "Crit" : 2397, "DH" : 1544} # Stats for RedMage
    SMNStat = {"MainStat": 2948, "WD":126, "Det" : 1451, "Ten" : 400, "SS": 544, "Crit" : 2436, "DH" : 1544} # Stats for Summoner

    # Healer
    SCHStat = {"MainStat": 2931, "WD":126, "Det" : 1750, "Ten" : 400, "SS": 1473, "Crit" : 2351, "DH" : 436} # Stats for Scholar
    WHMStat = {"MainStat": 2945, "WD":126, "Det" : 1792, "Ten" : 400, "SS": 839, "Crit" : 2313, "DH" : 904} # Stats for WhiteMage
    ASTStat = {"MainStat": 2949, "WD":126, "Det" : 1659, "Ten" : 400, "SS": 1473, "Crit" : 2280, "DH" : 436} # Stats for Astrologian
    SGEStat = {"MainStat": 2928, "WD":126, "Det" : 1859, "Ten" : 400, "SS": 827, "Crit" : 2312, "DH" : 1012} # Stats for Sage

    # Physical Ranged
    MCHStat = {"MainStat": 2937, "WD":126, "Det" : 1598, "Ten" : 400, "SS": 400, "Crit" : 2389, "DH" : 1592} # Stats for Machinist
    BRDStat = {"MainStat": 2949, "WD":126, "Det" : 1721, "Ten" : 400, "SS": 536, "Crit" : 2387, "DH" : 1340} # Stats for Bard
    DNCStat = {"MainStat": 2949, "WD":126, "Det" : 1721, "Ten" : 400, "SS": 536, "Crit" : 2387, "DH" : 1340} # Stats for Dancer
    
    # Melee
    NINStat = {"MainStat": 2921, "WD":126, "Det" : 1669, "Ten" : 400, "SS": 400, "Crit" : 2399, "DH" : 1511} # Stats for Ninja
    SAMStat = {"MainStat": 2937, "WD":126, "Det" : 1571, "Ten" : 400, "SS": 508, "Crit" : 2446, "DH" : 1459} # Stats for Samurai
    DRGStat = {"MainStat": 2949, "WD":126, "Det" : 1545, "Ten" : 400, "SS": 400, "Crit" : 2462, "DH" : 1577} # Stats for Dragoon
    MNKStat = {"MainStat": 3076, "WD":126, "Det" : 1546, "Ten" : 400, "SS": 769, "Crit" : 2490, "DH" : 1179} # Stats for Monk
    RPRStat = {"MainStat": 2946, "WD":126, "Det" : 1545, "Ten" : 400, "SS": 400, "Crit" : 2462, "DH" : 1577} # Stats for Reaper

    # Tank
    DRKStat = {"MainStat": 2910, "WD":126, "Det" : 1844, "Ten" : 751, "SS": 400, "Crit" : 2377, "DH" : 1012} # Stats for DarkKnight
    WARStat = {"MainStat": 2910, "WD":126, "Det" : 1844, "Ten" : 751, "SS": 400, "Crit" : 2377, "DH" : 1012} # Stats for Warrior
    PLDStat = {"MainStat": 2891, "WD":126, "Det" : 1883, "Ten" : 631, "SS": 650, "Crit" : 2352, "DH" : 868} # Stats for Paladin
    GNBStat = {"MainStat": 2891, "WD":126, "Det" : 1883, "Ten" : 631, "SS": 650, "Crit" : 2352, "DH" : 868} # Stats for Gunbreaker

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
    DRGOpener = []
    MNKOpener = []
    NINOpener = []
    RPROpener = []

    # Tank
    DRKOpener = []
    WAROpener = [Tomahawk, Infuriate,HeavySwing, Maim, Potion, StormEye, InnerRelease,InnerChaos, Upheaval, Onslaught, PrimalRend, Infuriate, InnerChaos, Onslaught, FellCleave, Onslaught, FellCleave, FellCleave, HeavySwing, Maim, StormPath, FellCleave, Infuriate, InnerChaos]
    PLDOpener = []
    GNBOpener = []


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

    PlayerList = [WARPlayer]

    Event.PlayerList = PlayerList

    # ===============================================================================================

    # Here you can change the final parameters to the simulation

    Countdown = 20 # Value of the countdown in seconds
    TimeLimit = 1000 # Time limit for the simulation in seconds. It will stop once this time has been reached (in simulation time)
    time_unit = 0.01 # Time unit or frame of the simulation. Smallest step the simulator will take between each iterations. It is advised to not change this value
    ShowGraph = True # Parameter to show (or not) the graph generated by the simulator.
    RequirementOn = True # Parameter that will enable or disable the requirement check for all actions. If False the simulator
                         # will not check if an action can be done

    # ===============================================================================================

    if SaveFight: #If we wish to save the fight

        os.system('CLS') #clearing HUD

        print(
        "===================== SAVE FIGHT IN CODE ====================="
        )
        filename = input("Enter the name you wish to save the fight as : ")

        SaveFight(Event, Countdown, TimeLimit, filename)
    else:
        Event.RequirementOn = RequirementOn
        Event.ShowGraph = ShowGraph
        Event.SimulateFight(time_unit, TimeLimit, Countdown)


