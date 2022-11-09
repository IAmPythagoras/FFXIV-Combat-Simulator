"""
This file will contain all BaseModel as class for the different request we can give to the API.
This follows the fastAPI model : https://fastapi.tiangolo.com/tutorial/body/
"""

from pydantic import BaseModel
from typing import List
# defining class that will be expected. This will let fastAPI do data validation

class fightInfoIn(BaseModel):
    fightDuration : float
    time_unit : float
    ShowGraph : bool
    RequirementOn : bool
    IgnoreMana : bool

class statIn(BaseModel):
    MainStat : int
    WD : int
    Det : int
    Ten : int
    SS : int
    Crit : int
    DH : int

class actionIn(BaseModel):
    actionName : str
    waitTime : float | None = None

class PlayerInfoIn(BaseModel):
    JobName : str
    playerID : int
    stat : statIn
    etro_gearset_url : str | None = ""
    Auras : List[str]
    actionList : List[actionIn]

class dataIn(BaseModel):
    fightInfo : fightInfoIn
    PlayerList : List[PlayerInfoIn]

class RequestParamIn(BaseModel):
    GraphInfo : bool
    ProcInfo : bool
    failedRequirementEvent : bool


class SimulateFightIn(BaseModel):
    data : dataIn # Fight's data
    RequestParam : RequestParamIn # Parameter of request such as if the user wants graph info, etc.
    class Config:
        orm_mode = True