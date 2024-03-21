from ffxivcalc.Jobs.Base_Spell import WaitAbility
from ffxivcalc.Jobs.ActionEnum import name_for_id
#CASTER

from ffxivcalc.Jobs.Caster.Caster_Spell import CasterAbility
from ffxivcalc.Jobs.Caster.Blackmage.BlackMage_Spell import BlackMageAbility
from ffxivcalc.Jobs.Caster.Redmage.Redmage_Spell import RedMageAbility
from ffxivcalc.Jobs.Caster.Summoner.Summoner_Spell import SummonerAbility

#HEALER
from ffxivcalc.Jobs.Healer.Healer_Spell import HealerAbility
from ffxivcalc.Jobs.Healer.Sage.Sage_Spell import SageAbility
from ffxivcalc.Jobs.Healer.Astrologian.Astrologian_Spell import AstrologianAbility
from ffxivcalc.Jobs.Healer.Scholar.Scholar_Spell import ScholarAbility
from ffxivcalc.Jobs.Healer.Whitemage.Whitemage_Spell import WhiteMageAbility
from ffxivcalc.Jobs.Melee.Monk.Monk_Spell import MonkAbility

#RANGED
from ffxivcalc.Jobs.Ranged.Ranged_Spell import BardSpell, RangedAbility
from ffxivcalc.Jobs.Ranged.Bard.Bard_Spell import BardAbility
from ffxivcalc.Jobs.Ranged.Machinist.Machinist_Spell import MachinistAbility
from ffxivcalc.Jobs.Ranged.Dancer.Dancer_Spell import DancerAbility

#TANK
from ffxivcalc.Jobs.Tank.Tank_Spell import TankAbility
from ffxivcalc.Jobs.Tank.Gunbreaker.Gunbreaker_Spell import GunbreakerAbility
from ffxivcalc.Jobs.Tank.DarkKnight.DarkKnight_Spell import DarkKnightAbility
from ffxivcalc.Jobs.Tank.Warrior.Warrior_Spell import WarriorAbility
from ffxivcalc.Jobs.Tank.Paladin.Paladin_Spell import PaladinAbility

#MELEE
from ffxivcalc.Jobs.Melee.Melee_Spell import MeleeAbility
from ffxivcalc.Jobs.Melee.Samurai.Samurai_Spell import SamuraiAbility
from ffxivcalc.Jobs.Melee.Ninja.Ninja_Spell import NinjaAbility
from ffxivcalc.Jobs.Melee.Dragoon.Dragoon_Spell import DragoonAbility
from ffxivcalc.Jobs.Melee.Reaper.Reaper_Spell import ReaperAbility

from ffxivcalc.helperCode.exceptions import ActionNotFound, JobNotFound, InvalidTarget

import logging
main_logging = logging.getLogger("ffxivcalc")
lookUpAbilityId_logging = main_logging.getChild("lookUpAbilityId")

def lookup_abilityID(actionID, targetID, sourceID, player_list):
    """
    This function will translate an actionID into a Spell object of the relevant action that the simulator can use.
    actionID : int -> ID of the action in the game
    targetID : int -> ID of the target. Can be player or Enemy.
    sourceID : int -> ID of the player casting the action.
    player_list : dict -> dict of all players with some information.
    """
    #Will first get the job of the sourceID so we know in what dictionnary to search for

    def lookup(JobDict, ClassDict, job_name):
        """
        This function actually looks up the relevant dictionnary of the Job to find the Spell object.
        JobDict : dict -> dictionnary with keys being IDs and mapping to the Spell object (only for Job actions)
        ClassDict : dict -> same as JobDict, but for Class actions
        """
        if not (int(actionID) in JobDict.keys()): #if not in, then the action is in the ClassDict
            if not (int(actionID) in ClassDict.keys()):
                log_str = "Action Not found , Job : " + job_name + " , ActionId : " + str(actionID) + " , targetID : " + str(targetID) + " , sourceID : " + str(sourceID)
                lookUpAbilityId_logging.warning(log_str)
                lookUpAbilityId_logging.warning("Since action was not found defaulting to WaitAbility(0).")
                return WaitAbility(0) #Currently at none so we can debug
                raise ActionNotFound #Did not find action
            if callable(ClassDict[int(actionID)]): #If the action is a function
                if (not (str(targetID) in player_list.keys())):
                    player_obj = player_list[sourceID]["job_object"]
                    raise InvalidTarget(name_for_id(actionID, player_obj.ClassAction, player_obj.JobAction), player_obj, None,True, targetID)
                return ClassDict[int(actionID)](player_list[str(targetID)]["job_object"])
            return ClassDict[int(actionID)] #Class actions do not have the possibility to target other allies, so we assume itll target an enemy

        if callable(JobDict[int(actionID)]): #If the action is a function
            if (not (str(targetID) in player_list.keys())):
                player_obj = player_list[sourceID]["job_object"]
                raise InvalidTarget(name_for_id(actionID, player_obj.ClassAction, player_obj.JobAction), player_obj, None,True, targetID)
            return JobDict[int(actionID)](player_list[str(targetID)]["job_object"])
        return JobDict[int(actionID)] #Else return object

    job_name = player_list[str(sourceID)]["job"] #getting job name

    #Will now go through all possible job and find what action is being used based on the ID. If the ID is not right, it will
    #raise an ActionNotFoundError. And if the job's name does not exist it will raise a JobNotFoundError
    if job_name == "BlackMage" :#Caster
        return lookup(BlackMageAbility, CasterAbility,job_name)
    elif job_name == "RedMage":
        return lookup(RedMageAbility, CasterAbility,job_name)
    elif job_name == "Summoner":
        return lookup(SummonerAbility, CasterAbility,job_name)
    elif job_name == "Dancer":#Ranged
        return lookup(DancerAbility, RangedAbility,job_name)
    elif job_name == "Machinist":
        return lookup(MachinistAbility, RangedAbility,job_name)
    elif job_name == "Bard":
        return lookup(BardAbility, RangedAbility,job_name)
    elif job_name == "Warrior":#Tank
        return lookup(WarriorAbility, TankAbility,job_name)
    elif job_name == "Gunbreaker":
        return lookup(GunbreakerAbility, TankAbility,job_name)
    elif job_name == "DarkKnight":
        return lookup(DarkKnightAbility, TankAbility,job_name)
    elif job_name == "Paladin":
        return lookup(PaladinAbility, TankAbility,job_name)
    elif job_name == "WhiteMage":#Healer
        return lookup(WhiteMageAbility, HealerAbility,job_name)
    elif job_name == "Scholar":
        return lookup(ScholarAbility, HealerAbility,job_name)
    elif job_name == "Sage":
        return lookup(SageAbility, HealerAbility,job_name)
    elif job_name == "Astrologian":
        return lookup(AstrologianAbility, HealerAbility,job_name)
    elif job_name == "Samurai":#Melee
        return lookup(SamuraiAbility, MeleeAbility,job_name)
    elif job_name == "Reaper":
        return lookup(ReaperAbility, MeleeAbility,job_name)
    elif job_name == "Ninja":
        return lookup(NinjaAbility, MeleeAbility,job_name)
    elif job_name == "Monk":
        return lookup(MonkAbility, MeleeAbility,job_name)
    elif job_name == "Dragoon":
        return lookup(DragoonAbility, MeleeAbility,job_name)

    lookUpAbilityId_logging.critical("Job name not found : " + job_name)

    raise JobNotFound #If we get here, then we have not found the job in question
    #This should not happen, and if it does it means we either have a serious problem or the names aren't correct