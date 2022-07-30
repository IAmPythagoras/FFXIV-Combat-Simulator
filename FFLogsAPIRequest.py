# -- coding: utf-8 --
"""
@author: Bri

The network/API request part of this code was made by a friend of mine called Brian.
I only did the code relevant to how we used the data, he did everything regarding
how to get the data. You can DM him on discord if you have questions : Bri-kun#6539

"""
from Jobs.Base_Spell import ApplyPotion, WaitAbility

#CASTER
from Jobs.Caster.Summoner.Summoner_Player import *
from Jobs.Caster.Blackmage.BlackMage_Player import * 
from Jobs.Caster.Redmage.Redmage_Player import *
from Jobs.Caster.Caster_Spell import CasterAbility
from Jobs.Caster.Blackmage.BlackMage_Spell import BlackMageAbility
from Jobs.Caster.Redmage.Redmage_Spell import RedMageAbility
from Jobs.Caster.Summoner.Summoner_Spell import SummonerAbility

#HEALER
from Jobs.Healer.Sage.Sage_Player import *
from Jobs.Healer.Scholar.Scholar_Player import *
from Jobs.Healer.Whitemage.Whitemage_Player import *
from Jobs.Healer.Astrologian.Astrologian_Player import *
from Jobs.Healer.Healer_Spell import HealerAbility
from Jobs.Healer.Sage.Sage_Spell import SageAbility
from Jobs.Healer.Astrologian.Astrologian_Spell import AstrologianAbility
from Jobs.Healer.Scholar.Scholar_Spell import ScholarAbility
from Jobs.Healer.Whitemage.Whitemage_Spell import WhiteMageAbility

#RANGED
from Jobs.Ranged.Machinist.Machinist_Player import *
from Jobs.Ranged.Bard.Bard_Player import *
from Jobs.Ranged.Dancer.Dancer_Player import *
from Jobs.Ranged.Ranged_Spell import BardSpell, RangedAbility
from Jobs.Ranged.Bard.Bard_Spell import BardAbility
from Jobs.Ranged.Machinist.Machinist_Spell import MachinistAbility
from Jobs.Ranged.Dancer.Dancer_Spell import DancerAbility

#TANK
from Jobs.Tank.Gunbreaker.Gunbreaker_Player import *
from Jobs.Tank.DarkKnight.DarkKnight_Player import *
from Jobs.Tank.Warrior.Warrior_Player import *
from Jobs.Tank.Paladin.Paladin_Player import *
from Jobs.Tank.Tank_Spell import TankAbility
from Jobs.Tank.Gunbreaker.Gunbreaker_Spell import GunbreakerAbility
from Jobs.Tank.DarkKnight.DarkKnight_Spell import DarkKnightAbility
from Jobs.Tank.Warrior.Warrior_Spell import WarriorAbility
from Jobs.Tank.Paladin.Paladin_Spell import PaladinAbility

#MELEE
from Jobs.Melee.Samurai.Samurai_Player import *
from Jobs.Melee.Ninja.Ninja_Player import *
from Jobs.Melee.Dragoon.Dragoon_Player import *
from Jobs.Melee.Reaper.Reaper_Player import *
from Jobs.Melee.Monk.Monk_Player import *
from Jobs.Melee.Melee_Spell import MeleeAbility
from Jobs.Melee.Samurai.Samurai_Spell import MeikyoCheck, MeikyoEffect, MeikyoStackCheck, SamuraiAbility
from Jobs.Melee.Ninja.Ninja_Spell import NinjaAbility
from Jobs.Melee.Dragoon.Dragoon_Spell import DragoonAbility
from Jobs.Melee.Reaper.Reaper_Spell import ReaperAbility
from Jobs.Melee.Monk.Monk_Spell import MonkAbility


import http.client, json 

class ActionNotFound(Exception):#Exception called if an action isn't found in the dictionnary
    pass
class JobNotFound(Exception):#Exception called if a Job isn't found
    pass

def getAccessToken(conn, client_id, client_secret):
    payload = "grant_type=client_credentials&client_id=%s&client_secret=%s" % (client_id, client_secret)
    headers = {'content-type':"application/x-www-form-urlencoded"}
    conn.request("POST","/oauth/token", payload, headers)
    res = conn.getresponse()
    res_str = res.read().decode("utf-8")
    res_json = json.loads(res_str)
    return res_json["access_token"]

def getAbilityList(client_id, client_secret, fightID, fightNumber):

    def lookup_abilityID(actionID, targetID, sourceID, targetEnemy, targetSelf, isHeal):
        #Will first get the job of the sourceID so we know in what dictionnary to search for

        def lookup(JobDict, ClassDict):
            if not (int(actionID) in JobDict.keys()): #if not in, then the action is in the ClassDict
                if not (int(actionID) in ClassDict.keys()):
                    #if job_name == "Warrior" : input("Missing action : " + str(actionID))
                    return WaitAbility(0) #Currently at none so we can debug
                    raise ActionNotFound #Did not find action
                return ClassDict[int(actionID)] #Class actions do not have the possibility to target other allies, so we assume itll target an enemy


            if callable(JobDict[int(actionID)]): #If the action is a function
                return JobDict[int(actionID)](player_list[str(targetID)]["job_object"])
            return JobDict[int(actionID)] #Else return object
            """
            if targetEnemy or targetSelf or targetID == -1 or isHeal: 
                return JobDict[int(actionID)]
            else: 
                if int(actionID) == 7388 or int(actionID) == 7393 or int(actionID) == 25754 or int(actionID) == 24296: return JobDict[int(actionID)] #Edge case for TBN/Oblation/ShakeItOff
                return JobDict[int(actionID)](player_list[str(targetID)]["job_object"]) #Otherwise it returns that
            #we assume to be a function with one input as the object of the target
             """
        job_name = player_list[str(sourceID)]["job"] #getting job name

        #Will now go through all possible job and find what action is being used based on the ID. If the ID is not right, it will
        #raise an ActionNotFoundError. And if the job's name does not exist it will raise a JobNotFoundError
        if job_name == "BlackMage" :#Caster
            return lookup(BlackMageAbility, CasterAbility)
        elif job_name == "RedMage":
            return lookup(RedMageAbility, CasterAbility)
        elif job_name == "Summoner":
            return lookup(SummonerAbility, CasterAbility)
        elif job_name == "Dancer":#Ranged
            return lookup(DancerAbility, RangedAbility)
        elif job_name == "Machinist":
            return lookup(MachinistAbility, RangedAbility)
        elif job_name == "Bard":
            return lookup(BardAbility, RangedAbility)
        elif job_name == "Warrior":#Tank
            return lookup(WarriorAbility, TankAbility)
        elif job_name == "Gunbreaker":
            return lookup(GunbreakerAbility, TankAbility)
        elif job_name == "DarkKnight":
            return lookup(DarkKnightAbility, TankAbility)
        elif job_name == "Paladin":
            return lookup(PaladinAbility, TankAbility)
        elif job_name == "WhiteMage":#Healer
            return lookup(WhiteMageAbility, HealerAbility)
        elif job_name == "Scholar":
            return lookup(ScholarAbility, HealerAbility)
        elif job_name == "Sage":
            return lookup(SageAbility, HealerAbility)
        elif job_name == "Astrologian":
            return lookup(AstrologianAbility, HealerAbility)
        elif job_name == "Samurai":#Melee
            return lookup(SamuraiAbility, MeleeAbility)
        elif job_name == "Reaper":
            return lookup(ReaperAbility, MeleeAbility)
        elif job_name == "Ninja":
            return lookup(NinjaAbility, MeleeAbility)
        elif job_name == "Monk":
            return lookup(MonkAbility, MeleeAbility)
        elif job_name == "Dragoon":
            return lookup(DragoonAbility, MeleeAbility)

        raise JobNotFound #If we get here, then we have not found the job in question
        #This should not happen, and if it does it means we either have a serious problem or the names aren't correct


    conn = http.client.HTTPSConnection("www.fflogs.com")
    access_token = getAccessToken(conn, client_id, client_secret)

    payload = "{\"query\":\"query trio{\\n\\treportData {\\n\\t\\treport(code: \\\"" + fightID + "\\\") {\\n\\t\\t\\tplayerDetails(fightIDs:" + fightNumber +",endTime:999999999),\\n\\t\\t\\tfights(fightIDs:8){\\n\\t\\t\\t\\tenemyNPCs{\\n\\t\\t\\t\\t\\tid\\n\\t\\t\\t\\t}\\n\\t\\t\\t\\tstartTime\\n\\t\\t\\t}\\n\\t\\t}\\n\\t\\t\\t\\n\\t}\\n}\",\"operationName\":\"trio\"}"

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer %s" % access_token
        }

    conn.request("POST", "/api/v2/client", payload, headers)

    res = conn.getresponse()
    data = res.read()
    data_json = json.loads(data.decode("utf-8"))

    #Getting Player's Class, ids and name

    player_data = data_json["data"]["reportData"]["report"]["playerDetails"]["data"]["playerDetails"]
    enemy_data = data_json["data"]["reportData"]["report"]["fights"][0]["enemyNPCs"]
    #Mix of dictionnary and array with relevant information
    #The goal of this request and the following code is to parse the JSON file into relevant information
    player_list = {} #Dict which will have all a list of players with their ids, role and name
    enemy_list = [] #List with all ids of enemies in the fight
    relative_timestamp_zero = int(data_json["data"]["reportData"]["report"]["fights"][0]["startTime"]) #relative 0 of the report

    for enemy in enemy_data:
        enemy_list += [enemy["id"]] #Getting the enemies id so we can identifiate who an enemy is not targeted by an action

    for player_class in player_data: #player_data is a dictionnary with key "healers", "DPS", "tanks"
        for player in player_data[player_class]:

            #Will check what job the player is so we can create a player object of the relevant job

            job_name = player["type"]
            job_object = None

            if player_class == "healers":
                if job_name == "Sage" : job_object = Sage(2.5, [], [], [], None, {})
                elif job_name == "Scholar" : job_object = Scholar(2.5, [], [], [], None, {})
                elif job_name == "WhiteMage" : job_object = Whitemage(2.5, [], [], [], None, {})
                elif job_name == "Astrologian" : job_object = Astrologian(2.5, [], [], [], None, {})
            elif player_class == "tanks":
                if job_name == "Warrior" : job_object = Warrior(2.5, [], [], [], None, {})
                elif job_name == "DarkKnight" : job_object = DarkKnight(2.5, [], [], [], None, {})
                elif job_name == "Paladin" : job_object = Paladin(2.5, [], [], [], None, {})
                elif job_name == "Gunbreaker" : job_object = Gunbreaker(2.5, [], [], [], None, {})
            else: #Is a DPS
                #Caster
                if job_name == "BlackMage" : job_object = BlackMage(2.5, [], [], [], None, {})
                elif job_name == "RedMage" : job_object = Redmage(2.5, [], [], [], None, {})
                elif job_name == "Summoner" : job_object = Summoner(2.5, [], [], [], None, {})
                #Ranged
                elif job_name == "Dancer" : job_object = Dancer(2.5, [], [], [], None, {})
                elif job_name == "Machinist" : job_object = Machinist(2.5, [], [], [], None, {})
                elif job_name == "Bard" : job_object = Bard(2.5, [], [], [], None, {})
                #melee
                elif job_name == "Reaper" : job_object = Reaper(2.5, [], [], [], None, {})
                #elif job_name == "Monk" : job_object = Machinist(2.5, [], [], [], None, {}) #Monk is not yet implemented
                elif job_name == "Dragoon" : job_object = Dragoon(2.5, [], [], [], None, {})
                elif job_name == "Ninja" : job_object = Ninja(2.5, [], [], [], None, {})
                elif job_name == "Samurai" : job_object = Samurai(2.5, [], [], [], None, {})
                
                

            player_list[str(player["id"])] = {"name" : player["name"], "job" : job_name, "job_object" : job_object} #Adding new Key
            #We can access the information using the player's id

    



    #2nd request will look at all prepull actions done by the players

    payload = "{\"query\":\"query trio{\\n\\treportData {\\n\\t\\treport(code: \\\""+fightID+"\\\") {\\n\\t\\t\\ttitle,\\n\\t\\t\\tendTime,\\n\\t\\t\\tevents(\\n\\t\\t\\t\\tendTime:1649370483952,\\n\\t\\t\\t\\tfightIDs:"+fightNumber+",\\n\\t\\t\\t\\tincludeResources: false,\\n\\t\\t\\t\\tfilterExpression:\\\"type = 'combatantinfo'\\\"\\n\\t\\t\\t){data\\n\\t\\t\\t}\\n\\t\\t\\t\\n\\t\\t}\\n\\t}\\n}\",\"operationName\":\"trio\"}"
    conn.request("POST", "/api/v2/client", payload, headers)

    res = conn.getresponse()
    data = res.read()
    data_json = json.loads(data.decode("utf-8"))

    combatantinfo_list = data_json["data"]["reportData"]["report"]["events"]["data"] #Array of combatantinfo

    for info in combatantinfo_list:
        sourceID = str(info["sourceID"])
        player_obj = player_list[sourceID]["job_object"]
        auras = info["auras"]
        for aura in auras: #Going through all buffs in the player
            #We will look for a selection of buffs that are important. We will assume
            #the optimal scenario. So if we use a potion, we will assume its right before the fight begins
            if aura["name"] == "SharpCast":
                #SharpCast for BLM.
                player_obj.SharpCast = True
            elif aura["name"] == "Soulsow":
                player_obj.Soulsow = True
            elif aura["name"] == "Medicated":
                #Potion
                def PrepullPotion(Player, Enemy):
                    ApplyPotion(Player, Enemy)
                    Player.EffectToRemove.append(PrepullPotion)
                player_obj.EffectList.append(PrepullPotion) #Adding this effect that will automatically apply the potion
                #on the first go through of the sim
                player_obj.PotionTimer = 27 #Assume we loose a bit on it
            elif aura["name"] == "Meikyo Shisui":
                player_obj.EffectCDList.append(MeikyoStackCheck)
                player_obj.MeikyoCD = 46
                player_obj.MeikyoStack -= 1
                player_obj.EffectList.append(MeikyoEffect)
                player_obj.EffectCDList.append(MeikyoCheck) #Could be a problem if do it before finishing 3 weaponskills
                player_obj.Meikyo = 3





    #Third request will fetch all the abilities done in the fight and make an array associated with each player's ID

    payload = "{\"query\":\"query trio{\\n    reportData {\\n        report(code: \\\""+fightID+"\\\") {\\n\\t\\t\\t\\tendTime,\\n            events(\\n\\t\\t\\t\\t\\t\\t\\tfightIDs:"+fightNumber+",\\n\\t\\t\\t\\t\\t\\t\\tendTime:99999999999999,\\n\\t\\t\\t\\t\\t\\t\\tincludeResources:false,\\n\\t\\t\\t\\t\\t\\t\\tfilterExpression:\\\"type = 'cast' OR type = 'begincast' OR type = 'calculateddamage' OR type = 'applybuff' or type = 'calculatedheal'\\\",\\n\\t\\t\\t\\t\\t\\t\\tlimit:10000\\n\\t\\t\\t\\t\\t\\t\\t\\n\\t\\t\\t\\t\\t\\t){data}\\n        }\\n\\n    }\\n}\",\"operationName\":\"trio\"}"
    conn.request("POST", "/api/v2/client", payload, headers)

    res = conn.getresponse()
    data = res.read()
    data_json = json.loads(data.decode("utf-8"))

    action_list = data_json["data"]["reportData"]["report"]["events"]["data"] #Array of all actions done


    class action_object():
        def __init__(self, action_id, timestamp, type, targetID, sourceID):
            self.action_id = action_id #actionID
            self.timestamp = timestamp #relative timestamp
            self.type = type
            self.targetID = targetID
            self.targetEnemy = targetID in enemy_list #if the targetID is one of the enemy ID, then we are targeting an enemy.
            self.targetSelf = targetID == sourceID #if the action targets the player casting it
            self.isHeal = type == "calculatedheal"
            #If we are not, we will have to do some more stuff later on.

        def isequal(self, action): #This checks if two consecutive actions are equivalent. 
            return self.action_id == action.action_id and self.timestamp == action.timestamp and self.type == action.type

        def __str__(self):
            return "action_id : " + str(self.action_id) + " type : " + self.type + " timestamp : " + str(self.timestamp/1000)

    action_dict = {} #Each player can be found using their id, and each key has an array of all done actions in order. Each entry in the array is an action_object

    #Will first initialize all key in the action_dict to be all empty arrays with key equal to player's ID

    for key in player_list:
        action_dict[key] = [] #Initializing each array
    #print(action_dict.keys())
    for action in action_list:
        #Will parse each action so each player has a list of all done action
        #input(action["sourceID"] + 1)
        if str(action["sourceID"]) in action_dict.keys(): #Making sure the sourceID is a player
            #input("hey")
            rel_timestamp = action["timestamp"] - relative_timestamp_zero
            action_dict[str(action["sourceID"])] += [action_object(action["abilityGameID"], rel_timestamp, action["type"], action["targetID"], action["sourceID"])]#Will be assumed to be damaging spell

    #Will now go through each player and build their action set
    for player in action_dict:
        player_action_list = [] #will contain the action list that we have to give to the sim for the player
        #player is each player's id
        wait_timestamp = 0 #timestamp value of an action so we can compare it to the next action to add WaitAbility
        raw_action_list = action_dict[str(player)] #list of action_object object
        wait_flag = False #a flag that is set to true if we have to add a WaitAbility() in the player_action_list
        wait_cast = False #a flag that is set to true if we are waiting for the next cast type
        wait_calculateddamage = False #a flag that is set to true if we are waiting for calculated damage
        is_casted = False #flag that is set to true if the spell is casted (the server has a shorter casting time cuz why not) so have to play around that
        is_heal = False #flag that is set to true if the spell is a healing spell
        previous_action = action_object(0, 0, "", 0, 0)

        #Edge case flags
        in_barrage = False #Flag that is set to true if we are looking for the barrage pattern (for bard)
        once_through = False #A flag to know if we have gone through barrage once
        calculated_damage_couter = 0 #A counter to know how much calculated damage we have seen

        wait_potion = False #Flag to know if we wait one cycle for a tincture

        for action in raw_action_list:
            #will check the type since we have to do different stuff in accordance to what it is


            if not previous_action.isequal(action): #Checks if this new action is the same, if it is we skip it
                previous_action = action


                if wait_flag: #If the flag is True, we have to add a WaitAbility
                    wait_time = (action.timestamp - wait_timestamp)
                    if wait_time >=500: #otherwise animation lock
                        #player_action_list.append(WaitAbility(max(0,(wait_time))/ 1000)) #Dividing by 1000 since time in milisecond
                        wait_flag = False #reset
                        wait_timestamp = 0 #reset

                next_action = lookup_abilityID(action.action_id, action.targetID, player, action.targetEnemy, action.targetSelf, action.isHeal) #returns the action object of the specified spell
                
                if is_heal:
                    #If this flag is set to true, we wait until we do not have type = 'calculatedheal'
                    if type != 'calculatedheal':
                        is_heal = False


                if in_barrage:
                    #If barrage was the last ability, then we need to wait for 3 calculated damage in a row
                    #We will first check if the action is a weaponskill, which is required for barrage to work
                    #This is so if we do an oGCD after barrage, it still works
                    if once_through:
                        calculated_damage_couter += 1 #We do nothing
                        #input("here 2")
                    elif isinstance(next_action, BardSpell) and next_action.Weaponskill:
                        #If we get here, we have to wait for 1 cast and  3 calculated damage
                        #We will still let the action go through the selection, but for the next time we will intercept it here
                        once_through = True
                        calculated_damage_couter = 0
                        #input("here 1")
                    if calculated_damage_couter == 3: #If we have seen two other (for a total of 3)
                        #Then we are done with this edge case, so we reset all flags and counters
                        calculated_damage_couter = 0
                        once_through = False
                        in_barrage = False
                        #input("here 3")
                #We will check for edge cases so we do not have to worry about them
                elif action.action_id == 107: #Bard barrage
                    #It will follow with 1 cast and 3 calculated damage since it actually use 3 of the next weaponskill
                    #But the sim only needs to know which weaponskill is done after, so we will filter it
                    in_barrage = True #Setting flag to true]
                    #input("Detected barrage")
                elif action.action_id == 1000049: #Tincture
                    player_action_list.append(next_action)
                    wait_potion = True
                    wait_flag = True
                    wait_timestamp = action.timestamp



                if not is_heal and calculated_damage_couter < 1 and not wait_potion: #No edge cases. Just proceed normally
                    if not wait_cast and not wait_calculateddamage:
                        if action.type == "begincast":#If begining cast, we simply add the spell to the list
                            player_action_list.append(next_action)
                            wait_cast = True #set flag to true
                            is_casted = True #says the action is a casted action
                            #if isinstance(next_action, BardSpell) : input("Adding : " + str(next_action.id))
                        elif action.type == "cast":
                            if next_action != None: player_action_list.append(next_action)
                            wait_calculateddamage = True
                            wait_flag = True
                            wait_timestamp = action.timestamp
                            #if isinstance(next_action, BardSpell) : input("Adding : " + str(next_action.id))
                        elif action.type == "calculateddamage":#insta cast, so we want to add but also check how long until next action. Calculated damage might also be right after a "cast", so we want to have
                            #it such that it can detect if it is an "insta-cast" or the damage from a casted action (which will affect how we add it to the action_list)
                            player_action_list.append(next_action)
                            wait_flag = True #We have to add a WaitAbility, so we will check this time and next action's timestamp and add a relevant WaitAbility
                            wait_timestamp = action.timestamp
                            #if isinstance(next_action, BardSpell) : input("Adding : " + str(next_action.id))
                        elif action.type == "calculatedhealing":
                            #same as calculateddamage, but since its a healing, we want to make sure we do not add the action
                            #for each player it hits (if it is an AOE heal)
                            player_action_list.append(next_action)
                            wait_flag = True #We have to add a WaitAbility, so we will check this time and next action's timestamp and add a relevant WaitAbility
                            wait_timestamp = action.timestamp
                            is_heal = True
                    elif wait_cast:
                        #Waiting for a cast
                        if action.type == "cast":
                            wait_cast = False
                            wait_calculateddamage = True
                    elif wait_calculateddamage:
                        if action.type == "calculateddamage" or action.type == "applybuff":
                            wait_calculateddamage = False
                            wait_flag = True #Waiting on next action
                            if is_casted: 
                                wait_timestamp = 500 + action.timestamp
                                is_casted = False
                            else:wait_timestamp = action.timestamp
                        elif action.type == "calculateddamage": #Same as calculateddamage, but with heal check
                            wait_calculateddamage = False
                            wait_flag = True #Waiting on next action
                            if is_casted: 
                                wait_timestamp = 500 + action.timestamp
                                is_casted = False
                            else:wait_timestamp = action.timestamp
                            is_heal = True
                        elif action.type == "cast":
                            if next_action != None: 
                                player_action_list.append(next_action)

                wait_potion = False #We have waited for the potion

        action_dict[player] = player_action_list
    return action_dict, player_list
    #action_dict is a dictionnary with a list of actions done by each player. Accessible by using their IDs
    #player_list is a dictionnary with relevant information to all players. Accessible by using their IDs
#Function to test timing
def test(client_id,client_secret):
    conn = http.client.HTTPSConnection("www.fflogs.com")
    access_token = getAccessToken(conn, client_id, client_secret)
    actionID = 7

    payload = "{\"query\":\"query trio{\\n\\treportData {\\n\\t\\treport(code: \\\"RQwfx3vATFWGahJc\\\") {\\n\\t\\t\\ttitle,\\n\\t\\t\\tendTime,\\n\\t\\t\\tevents(\\n\\t\\t\\t\\tendTime:1651557651925,\\n\\t\\t\\t\\tfightIDs:8,\\n\\t\\t\\t\\tincludeResources: false,\\n\\t\\t\\t\\tfilterExpression:\\\"ability.ID = " + str(actionID) +"\\\"\\n\\t\\t\\t){data\\n\\t\\t\\t}\\n\\t\\t\\t\\n\\t\\t}\\n\\t}\\n}\",\"operationName\":\"trio\"}"
    
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer %s" % access_token
        }

    conn.request("POST", "/api/v2/client", payload, headers)

    res = conn.getresponse()
    data = res.read()
    data_json = json.loads(data.decode("utf-8"))

    data = data_json["data"]["reportData"]["report"]["events"]["data"]
    wait_cast = False
    wait_calculated = False
    for event in data:

        if event["type"] == "cast" and event["sourceID"] == 56: input("Applying fire 4 at : " + str((event["timestamp"] - 14825136)/1000))

        if event["type"] == "begincast": 
             begin_time = event["timestamp"]
             wait_cast = True
        elif event["type"] == "cast" and wait_cast:
             end_time = event["timestamp"]
             input("Fire 4 had a casttime of " + str((end_time - begin_time)/1000))
             wait_calculated = True
             wait_cast = False
        elif wait_calculated and event["type"] == "calculateddamage":
             wait_calculated = False

#client_id = "9686da23-55d6-4f64-bd9d-40e2c64f8edf" #Put your own client_id and client_secret obtained from FFLogs
#client_secret = "ioZontZKcMxZwc33K4zsWlMAPY5dfZKsuo3eSFXE"
#test(client_id, client_secret)
#getAbilityList(client_id, client_secret)