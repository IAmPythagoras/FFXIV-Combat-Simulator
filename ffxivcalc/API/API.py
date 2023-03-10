"""
This file will contain the API module fastAPI. It is the file to launch if you
want to run the API.
"""

from fastapi import FastAPI
from ffxivcalc.API.Model.ObjectInModel import SimulateFightIn
from ffxivcalc.API.Model.ObjectOutModel import SimulateFightOut
from ffxivcalc.API.library import SimulateFightAPIHelper

# Make sure you have uvicorn installed and run the command
# python -m uvicorn API:app
# in the folder where API.py is located to run the API. Add --reload if you want the API to restart
# for every detected changes in the code.
# Then go to HOSTING_ADRESS/docs and you can tryout the different functionallities

app = FastAPI() # Creating api instance

@app.post("/SimulateFight", response_model=SimulateFightOut)
def GetSimulateFight(info : SimulateFightIn):
    """
    This API functionality lets someone ask for a simulation of a given fight.
    The API will request a JSON file with the correct format and will return the fight's
    results using as a schema SimulateFightOut.

    Args:\n
        info (SimulateFightIn): JSON file containing the fight's parameters.

    Returns:\n
        JSON : JSON file with the SimulateFightOut schema.
    """

    returnData = SimulateFightAPIHelper(info.dict())

    return returnData
