"""
This file will contain class and functions regarding handling when an action cannot be casted.
"""

class failedRequirementEvent:
    """
    This class will be object created when a requirement isn't met. It will contain information regarding the failure.
    """

    def __init__(self, timeStamp : float, playerID : int, requirementName : str, additionalInfo : str, fatal : bool):
        """
        timeStamp : float -> time at which the requirement failed
        playerID : int -> ID of the player that failed the requirement
        requirementName : str -> name of the requirement
        additionalInfo : str -> additional information relating to the requirement. Might be empty
        fatal : bool -> true if this requirement made the simulator stop
        """
        self.timeStamp = timeStamp
        self.playerID = playerID
        self.requirementName = requirementName
        self.additionalInfo = additionalInfo
        self.fatal = fatal