"""
This file will contain model of return request from the API.
"""

from pydantic import BaseModel
from typing import List, Dict
class failedRequirementEventOut(BaseModel):
    timeStamp : float
    playerID : int
    requirementName : str
    additionalInfo : str
    fatal : bool

class fightInfoOut(BaseModel):
    fightDuration : float
    maxfightDuration : float
    fightname : str | None = "SimulatedFight"
    TeamCompositionBonus : float
    failedRequirementEventList : List[failedRequirementEventOut]
    Success : bool

class GraphInfoOut(BaseModel):
    value : float
    name : float

class PlayerInfoOut(BaseModel):
    JobName : str
    ExpectedDPS : float
    PotencyPerSecond : float
    TotalDamage : float
    TotalPotency : float
    numberOfGCD : int
    ProcInfo : Dict
    GraphInfoDPS : GraphInfoOut
    GraphInfoPPS : GraphInfoOut

class dataOut(BaseModel):
    fightInfo : fightInfoOut
    PlayerList : List[PlayerInfoOut]

class SimulateFightOut(BaseModel):
    data : dataOut
    class Config:
        orm_mode = True


