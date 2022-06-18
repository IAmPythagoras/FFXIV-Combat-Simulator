# -- coding: utf-8 --
"""
Created on Thu Jun 17 11:00:05 2022

@author: Bri
"""

from Jobs.Base_Spell import WaitAbility

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

def lookup_abilityID(actionID, targetID): #not yet implemented
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
client_id = "" #Put in your own client_id and client_secret for now
client_secret = ""
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

payload = "{\"query\":\"query trio{\\n    reportData {\\n        report(code: \\\"RQwfx3vATFWGahJc\\\") {\\n\\t\\t\\t\\tendTime,\\n            events(\\n\\t\\t\\t\\t\\t\\t\\tfightIDs:8,\\n\\t\\t\\t\\t\\t\\t\\tendTime:1652499259666,\\n\\t\\t\\t\\t\\t\\t\\tincludeResources:false,\\n\\t\\t\\t\\t\\t\\t\\tfilterExpression:\\\"type = 'cast' OR type = 'begincast' OR type = 'calculateddamage' OR type = 'applybuff' OR type = 'damage'\\\"\\n\\t\\t\\t\\t\\t\\t\\t\\n\\t\\t\\t\\t\\t\\t){data}\\n        }\\n\\n    }\\n}\",\"operationName\":\"trio\"}"
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

action_dict = {} #Each player can be found using their id, and each key has an array of all done actions in order. Each entry in the array is an action_object

#Will first initialize all key in the action_dict to be all empty arrays with key equal to player's ID

for key in player_list:
    action_dict[key] = [] #Initializing each array

for action in action_list:
    #Will parse each action so each player has a list of all done action
    if action["sourceID"] in action_dict.keys(): #Making sure the sourceID is a player
        rel_timestamp = action["timestamp"] - relative_timestamp_zero
        action_dict[str(action["sourceID"])] += [action_object(action["abilityGameID"], rel_timestamp, action["type"], action["targetID"])]#Will be assumed to be damaging spell

#Will now go through each player and build their action set

for player in action_dict:
    player_action_list = [] #will contain the action list that we have to give to the sim for the player
    #player is each player's id
    raw_action_list = action_dict[player] #list of action_object object

    wait_flag = False #a flag that is set to true if we have to add a WaitAbility() in the player_action_list
    wait_timestamp = 0 #timestamp value of an action so we can compare it to the next action to add WaitAbility

    for action in raw_action_list:
        #will check the type since we have to do different stuff in accordance to what it is


        if wait_flag: #If the flag is True, we have to add a WaitAbility
            player_action_list.append(WaitAbility(action.timestamp - wait_timestamp))
            wait_flag = False #reset
            wait_timestamp = 0 #reset

        next_action = lookup_abilityID(action.action_id, action.targetID) #returns the action object of the specified spell NOT YET IMPLEMENTED
        if action.type == "begincast":#If begining cast, we simply add the spell to the list
            player_action_list.append(next_action)
        elif action.type == "damage" or action.type == "applybuff":#insta cast, so we want to add but also check how long until next action
            player_action_list.append(next_action)
            wait_flag = True #We have to add a WaitAbility, so we will check this time and next action's timestamp and add a relevant WaitAbility
            wait_timestamp = action.timestamp
        elif action.type == "cast":
            wait_flag = True #We have to add a WaitAbility, so we will check this time and next action's timestamp and add a relevant WaitAbility
            wait_timestamp = action.timestamp
    