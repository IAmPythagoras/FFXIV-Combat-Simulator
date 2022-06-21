# -- coding: utf-8 --
"""
Created on Thu Jun 17 11:00:05 2022

@author: Bri
"""
from Jobs.Base_Spell import WaitAbility
from Jobs.Caster.Blackmage.BlackMage_Spell import BlackMageAbility
from Jobs.Caster.Caster_Spell import CasterAbility

#CASTER
from Jobs.Caster.Summoner.Summoner_Player import *
from Jobs.Caster.Blackmage.BlackMage_Player import * 
from Jobs.Caster.Redmage.Redmage_Player import *

#HEALER
from Jobs.Healer.Sage.Sage_Player import *
from Jobs.Healer.Scholar.Scholar_Player import *
from Jobs.Healer.Whitemage.Whitemage_Player import *
from Jobs.Healer.Astrologian.Astrologian_Player import *

#RANGED
from Jobs.Ranged.Machinist.Machinist_Player import *
from Jobs.Ranged.Bard.Bard_Player import *
from Jobs.Ranged.Dancer.Dancer_Player import *

#TANK
from Jobs.Tank.Gunbreaker.Gunbreaker_Player import *
from Jobs.Tank.DarkKnight.DarkKnight_Player import *
from Jobs.Tank.Warrior.Warrior_Player import *
from Jobs.Tank.Paladin.Paladin_Player import *

#MELEE
from Jobs.Melee.Samurai.Samurai_Player import *
from Jobs.Melee.Ninja.Ninja_Player import *
from Jobs.Melee.Dragoon.Dragoon_Player import *
from Jobs.Melee.Reaper.Reaper_Player import *

import http.client, json 

class ActionNotFound(Exception):#Exception called if a spell fails to cast
    pass

def getAbilityList(client_id, client_secret):
    def lookup_abilityID(actionID, targetID, sourceID): #not yet implemented
        #Will first get the job of the sourceID so we know in what dictionnary to search for

        job_name = player_list[str(sourceID)]["job"] #getting job name
        if job_name == "BlackMage" :
            if not (int(actionID) in BlackMageAbility.keys()): #if not in, then the action is in CasterAbility
                if not (int(actionID) in CasterAbility.keys()):
                    #input("ID of action not found is : " + str(actionID))
                    return None
                    #raise ActionNotFound #Did not find action
                return CasterAbility[int(actionID)]
            return BlackMageAbility[int(actionID)]

        return None


    def getAccessToken(conn, client_id, client_secret):
        payload = "grant_type=client_credentials&client_id=%s&client_secret=%s" % (client_id, client_secret)
        headers = {'content-type':"application/x-www-form-urlencoded"}
        conn.request("POST","/oauth/token", payload, headers)
        res = conn.getresponse()
        res_str = res.read().decode("utf-8")
        res_json = json.loads(res_str)
        return res_json["access_token"]

    conn = http.client.HTTPSConnection("www.fflogs.com")
    access_token = getAccessToken(conn, client_id, client_secret)

    payload = "{\"query\":\"query trio{\\n    reportData {\\n        report(code: \\\"RQwfx3vATFWGahJc\\\") {\\n            playerDetails(fightIDs:8,endTime:999999999)\\n        }\\n\\n    }\\n}\",\"operationName\":\"trio\"}"

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer %s" % access_token
        }

    conn.request("POST", "/api/v2/client", payload, headers)

    res = conn.getresponse()
    data = res.read()
    data_json = json.loads(data.decode("utf-8"))
    #print(data_json["data"]["reportData"]["report"]["playerDetails"])
    #print(json.dumps(data_json["data"]["reportData"]["report"]["playerDetails"]["data"]["playerDetails"], indent=4, sort_keys=False))


    #Getting Player's Class, ids and name

    player_data = data_json["data"]["reportData"]["report"]["playerDetails"]["data"]["playerDetails"]
    #Mix of dictionnary and array with relevant information
    #The goal of this request and the following code is to parse the JSON file into relevant information

    player_list = {} #Dict which will have all a list of players with their ids, role and name

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
                elif job_name == "Summoner" : job_object = Summoner(2.5, [], [], [], None, {})
                #melee
                elif job_name == "Reaper" : job_object = Reaper(2.5, [], [], [], None, {})
                #elif job_name == "Monk" : job_object = Machinist(2.5, [], [], [], None, {}) #Monk is not yet implemented
                elif job_name == "Dragoon" : job_object = Dragoon(2.5, [], [], [], None, {})
                elif job_name == "Ninja" : job_object = Ninja(2.5, [], [], [], None, {})
                elif job_name == "Samurai" : job_object = Samurai(2.5, [], [], [], None, {})
                
                

            player_list[str(player["id"])] = {"name" : player["name"], "job" : player["type"], "job_object" : job_object} #Adding new Key
            #We can access the information using the player's id


    #Second request will fetch all the abilities done in the fight and make an array associated with each player's ID

    payload = "{\"query\":\"query trio{\\n    reportData {\\n        report(code: \\\"RQwfx3vATFWGahJc\\\") {\\n\\t\\t\\t\\tendTime,\\n            events(\\n\\t\\t\\t\\t\\t\\t\\tfightIDs:8,\\n\\t\\t\\t\\t\\t\\t\\tendTime:99999999999999,\\n\\t\\t\\t\\t\\t\\t\\tincludeResources:false,\\n\\t\\t\\t\\t\\t\\t\\tfilterExpression:\\\"type = 'cast' OR type = 'begincast' OR type = 'calculateddamage' OR type = 'applybuff'\\\",\\n\\t\\t\\t\\t\\t\\t\\tlimit:10000\\n\\t\\t\\t\\t\\t\\t\\t\\n\\t\\t\\t\\t\\t\\t){data}\\n        }\\n\\n    }\\n}\",\"operationName\":\"trio\"}"
    conn.request("POST", "/api/v2/client", payload, headers)

    res = conn.getresponse()
    data = res.read()
    data_json = json.loads(data.decode("utf-8"))

    #print(json.dumps(data_json["data"], indent=4, sort_keys=False))
    action_list = data_json["data"]["reportData"]["report"]["events"]["data"] #Array of all actions done
    relative_timestamp_zero = data_json["data"]["reportData"]["report"]["events"]["data"][0]["timestamp"] #value in millisecond of the first damaging ability done in the fight, this will be the relative 0

    class action_object():
        def __init__(self, action_id, timestamp, type, targetID):
            self.action_id = action_id #actionID
            self.timestamp = timestamp #relative timestamp
            self.type = type
            self.targetID = targetID

        def __str__(self):
            return "action_id : " + str(self.action_id) + " type : " + self.type

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
            action_dict[str(action["sourceID"])] += [action_object(action["abilityGameID"], rel_timestamp, action["type"], action["targetID"])]#Will be assumed to be damaging spell

    #Will now go through each player and build their action set
    #input(action_list)
    #input(action_dict)


    for player in action_dict:
        player_action_list = [] #will contain the action list that we have to give to the sim for the player
        #player is each player's id
        raw_action_list = action_dict[str(player)] #list of action_object object

        wait_flag = False #a flag that is set to true if we have to add a WaitAbility() in the player_action_list
        wait_timestamp = 0 #timestamp value of an action so we can compare it to the next action to add WaitAbility
        wait_cast = False #a flag that is set to true if we are waiting for the next cast type
        wait_calculateddamage = False #a flag that is set to true if we are waiting for calculated damage
        for action in raw_action_list:
            #will check the type since we have to do different stuff in accordance to what it is



            if wait_flag: #If the flag is True, we have to add a WaitAbility
                #if player == "1" : input("Waiting for : " + str((action.timestamp - wait_timestamp)))
                wait_time = (action.timestamp - wait_timestamp)
                if wait_time >= 100:
                    player_action_list.append(WaitAbility(wait_time/ 1000)) #Dividing by 1000 since time in milisecond
                wait_flag = False #reset
                wait_timestamp = 0 #reset

            next_action = lookup_abilityID(action.action_id, action.targetID, player) #returns the action object of the specified spell NOT YET IMPLEMENTED
            #if player == "1" : 
                #input(action)
            if not wait_cast and not wait_calculateddamage:
                if action.type == "begincast":#If begining cast, we simply add the spell to the list
                    #if player == "1" : print("adding")
                    wait_cast = True #set flag to true
                    player_action_list.append(next_action)
                elif action.type == "calculateddamage":#insta cast, so we want to add but also check how long until next action. Calculated damage might also be right after a "cast", so we want to have
                    #it such that it can detect if it is an "insta-cast" or the damage from a casted action (which will affect how we add it to the action_list)
                    #if player == "1" : print("adding")
                    player_action_list.append(next_action)
                    wait_flag = True #We have to add a WaitAbility, so we will check this time and next action's timestamp and add a relevant WaitAbility
                    wait_timestamp = action.timestamp
            elif wait_cast:
                #Waiting for a cast
                if action.type == "cast":
                    wait_flag = True #We have to add a WaitAbility, so we will check this time and next action's timestamp and add a relevant WaitAbility
                    wait_timestamp = action.timestamp
                    wait_cast = False
                    wait_calculateddamage = True
                elif action.type == "applybuff" :
                    pass #not yet implemented
            elif wait_calculateddamage:
                if action.type == "calculateddamage":
                    wait_calculateddamage = False



        action_dict[player] = player_action_list

    return action_dict["1"] #just for testing purposes
