from ffxivcalc.Request.FFLogs_api import FFLogClientV2, get_fflog_events_dataframe
from ffxivcalc.Request.ffxivcalcViewTranslator import ffxiv_sim_view
from ffxivcalc.helperCode.helper_backend import RestoreFightObject
from ffxivcalc.Request import custom_columns
import os

os.environ["FFLOGS_CLIENT_ID"] = "9b8e6c18-39d6-4ae0-91c7-e9221e699769"
os.environ["FFLOGS_CLIENT_SECRET"] = "u0j8e1aIygCejB6HiBJFJcr0RB1MSIkVkLdgxDox"
client = FFLogClientV2()


it = client.stream_fight_events("RQwfx3vATFWGahJc")

# name, list
import logging
__logger__ = logging.getLogger("ffxivcalc") # root logger
level = logging.DEBUG
logging.basicConfig(format='[%(levelname)s] %(name)s : %(message)s',filename='ffxivcalc_log.log', encoding='utf-8',level=level)
__logger__.setLevel(level=level) 

for fight in it:
    df = get_fflog_events_dataframe(fight[1])
    view = ffxiv_sim_view(df)
    for fightView in view:
        data = fightView[1]
        fight = RestoreFightObject(data)
        fight.RequirementOn = False
        fight.SimulateFight(0.01, 500, True)