# -- coding: utf-8 --
"""
Created on Thu Jun 17 11:00:05 2022

@author: Bri
"""
import http.client, json 


def getAccessToken(conn, client_id, client_secret):
    payload = "grant_type=client_credentials&client_id=%s&client_secret=%s" % (client_id, client_secret)
    headers = {'content-type':"application/x-www-form-urlencoded"}
    conn.request("POST","/oauth/token", payload, headers)
    res = conn.getresponse()
    res_str = res.read().decode("utf-8")
    res_json = json.loads(res_str)
    return res_json["access_token"]

conn = http.client.HTTPSConnection("www.fflogs.com")
client_id = "9686da23-55d6-4f64-bd9d-40e2c64f8edf"
client_secret = "ioZontZKcMxZwc33K4zsWlMAPY5dfZKsuo3eSFXE"
access_token = getAccessToken(conn, client_id, client_secret)

payload = "{\"query\":\"query trio{\\n\\treportData {\\n\\t\\treport(code: \\\"RQwfx3vATFWGahJc\\\") {\\n\\t\\t\\tplayerDetails(fightIDs:8,endTime:999999999)\\n\\t\\t}\\n\\t\\t\\t\\n\\t}\\n}\",\"operationName\":\"trio\"}"

headers = {
    'Content-Type': "application/json",
    'Authorization': "Bearer %s" % access_token
    }

conn.request("POST", "/api/v2/client", payload, headers)

res = conn.getresponse()
data = res.read()
data_json = json.loads(data.decode("utf-8"))
#print(data_json["data"]["reportData"]["report"]["playerDetails"])
print(json.dumps(data_json["data"]["reportData"]["report"]["playerDetails"], indent=4, sort_keys=False))