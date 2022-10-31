"""
This file will contain the API module fastAPI. It is the file to launch if you
want to run the API.
"""

from fastapi import FastAPI
from ObjectInModel import SimulateFightIn
from ObjectOutModel import SimulateFightOut
from library import SimulateFightAPIHelper
from fastapi.responses import JSONResponse

# Make sure you have uvicorn installed and run the command
# python -m uvicorn API:app
# in the folder where API.py is located to run the API

app = FastAPI() # Creating api instance

@app.post("/SimulateFight")#, response_model=SimulateFightOut
def GetSimulateFight(info : SimulateFightIn):
    return SimulateFightAPIHelper(info.dict())
